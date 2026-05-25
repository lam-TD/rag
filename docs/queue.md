# RabbitMQ: Bản chất, đánh đổi và khi nào nên dùng

> Tài liệu nội bộ — dành cho team trước khi refactor luồng RabbitMQ trong dự án RAG ingestion.
> Mục tiêu: hiểu **tại sao** dùng RabbitMQ, **khi nào** nên dùng, **khi nào** không, và những đánh đổi đi kèm — trước khi bàn đến việc viết code.

-----

## Mục lục

1. [Vấn đề: Tại sao cần RabbitMQ?](#1-vấn-đề-tại-sao-cần-rabbitmq)
1. [4 tính chất cốt lõi (qua ví dụ quán phở)](#2-4-tính-chất-cốt-lõi-qua-ví-dụ-quán-phở)
1. [Cái giá phải trả khi dùng RabbitMQ](#3-cái-giá-phải-trả-khi-dùng-rabbitmq)
1. [Checklist quyết định: Dùng hay không dùng?](#4-checklist-quyết-định-dùng-hay-không-dùng)
1. [So sánh với các giải pháp khác](#5-so-sánh-với-các-giải-pháp-khác)
1. [Các concept RabbitMQ cần biết khi refactor](#6-các-concept-rabbitmq-cần-biết-khi-refactor)
1. [Tóm tắt 1 trang](#7-tóm-tắt-1-trang)

-----

## 1. Vấn đề: Tại sao cần RabbitMQ?

Hãy hình dung luồng RAG ingestion **không có** RabbitMQ — chỉ thuần HTTP đồng bộ (synchronous):

```
User → POST /upload (file PDF 50MB) → FastAPI:
   1. Lưu file
   2. Parse PDF (10s)
   3. Chunking (5s)
   4. Gọi OpenAI embedding API (30s)
   5. Lưu vào vector DB (5s)
   → Trả response 200 OK
```

User phải chờ **~50 giây** cho 1 request. Vấn đề lộ ra ngay khi gặp các tình huống thực tế:

### Vấn đề 1: Mạng user rớt giữa chừng

- Server vẫn đang xử lý nhưng user **không biết** kết quả
- User retry → file bị xử lý **2 lần** → tốn tiền embedding, dữ liệu trùng lặp
- → Cần tách **nhận đơn hàng** và **xử lý đơn hàng** thành 2 việc khác nhau

### Vấn đề 2: 10 user cùng upload

- FastAPI có số worker hữu hạn (ví dụ 4 uvicorn workers)
- Mỗi request mất 50s → 6 user sau bị **block**, timeout
- Phần lớn 50s là **chờ I/O** (chờ OpenAI, chờ DB) → CPU rảnh nhưng worker vẫn bị “giữ chỗ”
- → Cần một nơi **xếp hàng** công việc

### Vấn đề 3: OpenAI API chậm bất thường

- Một API chậm kéo cả HTTP request chậm theo
- HTTP timeout (30-60s) kill request → công việc làm dở **mất luôn**
- → Công việc dài hạn **không nên gắn** vào vòng đời HTTP request

### Vấn đề 4: Restart server khi đang xử lý dở

- Restart = mất hết file đang xử lý
- Không có cách nào biết “đã làm đến đâu” để làm lại
- → Công việc cần được **lưu trữ bền vững (persistent)**

### → Tổng hợp 4 vấn đề thành 4 yêu cầu

1. **Tách rời** việc nhận và xử lý (decoupling)
1. **Xếp hàng** công việc khi có nhiều request cùng lúc (buffering)
1. **Không gắn** với vòng đời HTTP request (asynchronous)
1. **Bền vững**, không mất khi server chết (durability)

→ Đây chính là định nghĩa của một **Message Queue**. RabbitMQ là một implementation phổ biến.

-----

## 2. 4 tính chất cốt lõi (qua ví dụ quán phở)

Để dễ nhớ, hãy hình dung một **quán phở Hà Nội buổi sáng**:

- **Khách hàng** = user upload file
- **Thu ngân** = FastAPI nhận request
- **Đầu bếp** = worker xử lý file
- **Dây kẹp giấy order** = RabbitMQ queue

### Tính chất 1: Decoupling (Tách rời)

**Cách KHÔNG decouple:** Khách gọi món → thu ngân đích thân vào bếp nấu → bưng ra → mới nhận khách tiếp theo. Vô lý.

**Cách decouple:** Thu ngân ghi order vào **giấy**, kẹp lên dây. Đầu bếp tự lấy giấy xuống nấu. Hai người **không cần biết nhau, không cần chờ nhau**.

→ **Ý nghĩa với RAG:** FastAPI chỉ lo nhận file và ghi “đơn hàng”. Worker lo nấu (parse, embed). Hai bên độc lập, có thể deploy riêng, scale riêng.

### Tính chất 2: Buffering (Xếp hàng đệm)

**Tình huống:** 8h sáng, 20 khách ùa vào cùng lúc. Bếp chỉ có 2 đầu bếp.

- **Không có dây:** khách 3-20 đứng chờ ngoài cửa, bỏ đi.
- **Có dây:** 20 order treo trên dây, khách yên tâm về chỗ ngồi.

→ Dây kẹp giấy đóng vai trò **bộ đệm**, hấp thụ những lúc đông đột biến.

**Ý nghĩa với RAG:** 100 user upload cùng lúc cũng không sao. Queue giữ hết. Worker nhẩn nha xử lý từng cái.

### Tính chất 3: Asynchronous (Bất đồng bộ)

- **Synchronous** = khách đứng chờ ngay tại quầy đến khi tô phở xong mới đi ngồi.
- **Asynchronous** = khách order xong, được phát **số thẻ**, đi ngồi. Phở xong, loa gọi số.

→ Khách không bị “khóa chân” ở quầy.

**Ý nghĩa với RAG:** User upload xong nhận về `task_id`, đóng tab cũng được. Lát sau quay lại check trạng thái. Không phải nhìn spinner xoay 50 giây.

### Tính chất 4: Durability (Bền vững)

**Tình huống:** Đang giờ cao điểm, mất điện 5 phút.

- Order ghi **trong đầu**: mất điện → quên hết → khách chửi.
- Order ghi **ra giấy** kẹp lên dây: mất điện → giấy vẫn còn đó → có điện lại tiếp tục nấu.

→ “Ghi ra giấy” = lưu xuống đĩa cứng. Đây là **durability**.

**Ý nghĩa với RAG:** Server crash, deploy version mới, mất điện datacenter — message vẫn nằm an toàn trong RabbitMQ. Worker bật lên lại là tiếp tục xử lý.

### Bảng tổng kết

|Tính chất     |Quán phở                       |RAG project                      |
|--------------|-------------------------------|---------------------------------|
|**Decoupling**|Thu ngân ≠ đầu bếp             |FastAPI ≠ worker                 |
|**Buffering** |Dây kẹp giấy order             |Queue chứa file chờ xử lý        |
|**Async**     |Khách đi ngồi, không đứng chờ  |User đóng tab, không chờ spinner |
|**Durability**|Giấy không bay mất khi cúp điện|Message không mất khi server chết|

-----

## 3. Cái giá phải trả khi dùng RabbitMQ

RabbitMQ không miễn phí. Đây là những đánh đổi (trade-offs) bạn phải chấp nhận:

### 3.1. Thêm một service phải vận hành

Trước: chỉ có FastAPI + DB.
Sau: thêm RabbitMQ. Service này phải **luôn sống**. Nó chết → toàn bộ ingestion chết.

→ Phải monitor, backup, update, có thể cần chạy **cluster** để HA (High Availability).

### 3.2. Debug khó hơn nhiều

- Trước: bug → 1 stack trace.
- Sau: bug có thể nằm ở **producer** (FastAPI publish), **broker** (RabbitMQ), hoặc **consumer** (worker). Lỗi là một chuỗi sự kiện rời rạc qua nhiều process.

### 3.3. Phải nghĩ về những tình huống “kỳ quặc”

Những câu hỏi này trước đây không tồn tại, giờ bạn phải có câu trả lời:

|Tình huống thực tế                                     |Concept RabbitMQ cần biết           |
|-------------------------------------------------------|------------------------------------|
|Worker xử lý lỗi → vứt message đi hay làm lại? Mấy lần?|**Retry + max retries**             |
|Cùng 1 message bị gửi 2 lần                            |**Idempotency** (phía consumer)     |
|Worker crash giữa chừng → message mất luôn?            |**Acknowledgment** (ack/nack)       |
|Queue đầy nghẹt 10,000 message                         |**Queue length limit, backpressure**|
|Một message lỗi liên tục làm worker crash              |**Dead Letter Queue (DLQ)**         |

### 3.4. Tốn tài nguyên

Mỗi message phải ghi xuống đĩa (để durable), truyền qua network. Với dự án nhỏ → lợi bất cập hại.

### 3.5. Learning curve

Cả team phải hiểu: exchange, queue, binding, routing key, ack, prefetch, DLQ… Mỗi concept là một thứ phải học, phải nhớ, phải dạy người mới.

-----

## 4. Checklist quyết định: Dùng hay không dùng?

### ✅ Nên dùng RabbitMQ khi *ít nhất một* điều sau đúng:

- [ ] Tác vụ chạy **lâu** (> vài giây) và không thể bắt user chờ
- [ ] Có **đột biến traffic** (lúc đông lúc vắng)
- [ ] Cần **scale worker độc lập** với web server
- [ ] Cần **không mất việc** khi service crash
- [ ] Có **nhiều loại consumer** cùng xử lý 1 sự kiện (ví dụ: file upload → vừa embed, vừa gửi email, vừa log analytics)
- [ ] Cần **routing phức tạp** (1 message đến nhiều nơi theo luật)

### ❌ KHÔNG nên dùng khi:

- [ ] Tác vụ **nhanh** (< 1s), trả về ngay được
- [ ] **Traffic thấp và đều**, server hiện tại thừa sức
- [ ] Project **nhỏ, 1-2 dev**, không có DevOps
- [ ] Cần **kết quả ngay lập tức** để trả về user (queue là sai công cụ)
- [ ] **Đã có giải pháp đơn giản hơn** đủ dùng

### Câu hỏi tự đánh giá cho dự án của bạn

Trước khi refactor, team cần trả lời chung:

1. **Quy mô:** Dự án xử lý bao nhiêu file/ngày? 10? 1,000? 100,000?
1. **Đã đau gì chưa:** Có lý do cụ thể nào cần refactor? (User phàn nàn chậm? File bị mất? Server quá tải? Hay chỉ “code cũ lộn xộn muốn dọn”?)
1. **Team:** Có ai vận hành RabbitMQ không, hay chỉ 1-2 người dev?
1. **SLA:** Mất 1 file có nghiêm trọng không? Trễ 5 phút có sao không?

→ Trả lời xong, sẽ biết hướng refactor đúng: **giữ RabbitMQ và làm tốt hơn**, hay **đơn giản hóa, có khi bỏ luôn**. Refactor tốt là dám **bỏ thứ không cần**.

-----

## 5. So sánh với các giải pháp khác

Đừng nhảy thẳng vào RabbitMQ. Cân nhắc các giải pháp đơn giản hơn:

|Giải pháp                                 |Ưu điểm                                               |Nhược điểm                                                         |Phù hợp khi                                       |
|------------------------------------------|------------------------------------------------------|-------------------------------------------------------------------|--------------------------------------------------|
|**FastAPI `BackgroundTasks`**             |Đơn giản nhất, không thêm service                     |Mất job khi server restart, không scale, không retry, không monitor|POC, nội bộ, < 10 job/ngày                        |
|**Celery + Redis**                        |Setup nhanh, ecosystem Python tốt, đủ cho 80% use case|Redis ít bền vững hơn (dù có AOF persistence), routing đơn giản    |Hầu hết web app vừa và nhỏ                        |
|**DB làm queue** (bảng `tasks` với status)|Không thêm service mới, dùng DB sẵn có, dễ debug      |Throughput thấp (polling), không scale tốt                         |Job ít, ưu tiên đơn giản                          |
|**RabbitMQ**                              |Routing mạnh, durability tốt, guarantee cao           |Vận hành phức tạp, learning curve                                  |Throughput cao, cần routing phức tạp, hệ thống lớn|
|**Cloud-managed** (AWS SQS, GCP Pub/Sub)  |Không phải vận hành, scale auto                       |Vendor lock-in, tốn tiền theo message                              |Team không có DevOps, lên cloud                   |

### Khi nào RabbitMQ thực sự xứng đáng?

Khi bạn cần *đồng thời*:

- **Routing phức tạp** (fanout, topic-based, header-based)
- **Throughput cao** (hàng nghìn msg/giây trở lên)
- **Delivery guarantee mạnh** (at-least-once, không mất message)
- Team **có người vận hành** được nó

Nếu chỉ cần “chạy job nền” → **Celery + Redis** thường đủ và nhẹ hơn nhiều.

-----

## 6. Các concept RabbitMQ cần biết khi refactor

Phần này là “vocab cơ bản” để team đọc code và tài liệu RabbitMQ không bị lạc.

### 6.1. Các thành phần chính

- **Producer:** bên gửi message (trong dự án: FastAPI khi nhận file upload)
- **Consumer:** bên nhận và xử lý message (worker ingestion)
- **Broker:** chính là RabbitMQ server
- **Message:** đơn vị dữ liệu được gửi qua queue (thường là JSON: `{file_id, path, user_id, ...}`)
- **Queue:** hàng đợi chứa message chờ xử lý
- **Exchange:** “bưu điện” định tuyến message đến queue nào (theo routing key)
- **Binding:** quy tắc nối exchange với queue

```
Producer → Exchange → (binding) → Queue → Consumer
```

### 6.2. Các cơ chế bắt buộc phải nắm

|Concept                               |Ý nghĩa                                             |Tại sao cần                                                                           |
|--------------------------------------|----------------------------------------------------|--------------------------------------------------------------------------------------|
|**Acknowledgment (ack/nack)**         |Consumer báo cho RabbitMQ “đã xử lý xong” hoặc “lỗi”|Nếu không ack → worker crash giữa chừng → message tự động quay lại queue, không bị mất|
|**Durable queue + Persistent message**|Queue và message được ghi xuống đĩa                 |Sống sót qua restart RabbitMQ                                                         |
|**Prefetch (QoS)**                    |Giới hạn số message mỗi worker được “giữ” cùng lúc  |Tránh 1 worker ôm hết job, các worker khác chết đói                                   |
|**Dead Letter Queue (DLQ)**           |Queue phụ chứa các message lỗi/hết retry            |Cô lập “poison message”, debug sau, không làm tắc nghẽn queue chính                   |
|**Idempotency**                       |Cùng 1 message xử lý nhiều lần vẫn cho cùng kết quả |RabbitMQ guarantee at-least-once, nên message có thể đến 2 lần — code phải chịu được  |
|**Retry policy**                      |Số lần thử lại + thời gian chờ giữa các lần         |Lỗi tạm thời (API timeout) cần retry; lỗi vĩnh viễn (file hỏng) thì đi thẳng DLQ      |

### 6.3. Sai lầm thường gặp khi refactor

1. **Không bật `durable` cho queue và `persistent` cho message** → mất hết khi RabbitMQ restart.
1. **Auto-ack thay vì manual ack** → worker chết = message bay mất.
1. **Không set `prefetch_count`** → 1 worker ôm hết queue.
1. **Không có DLQ** → 1 message lỗi loop vô hạn, log đầy disk.
1. **Consumer không idempotent** → message gửi lại = ghi DB trùng.
1. **Không monitor queue depth** → queue âm thầm phình to đến khi RabbitMQ OOM.
1. **Connection per message** thay vì connection pool + channel → quá tải broker.

-----

## 7. Tóm tắt 1 trang

### RabbitMQ là gì?

Một **message broker** — đứng giữa producer và consumer, đóng vai trò “dây kẹp giấy order” trong quán phở.

### Giải quyết 4 vấn đề:

1. **Decoupling** — tách FastAPI và worker
1. **Buffering** — hấp thụ traffic đột biến
1. **Async** — user không phải chờ
1. **Durability** — không mất việc khi crash

### Đánh đổi:

- Thêm 1 service phải vận hành
- Debug khó hơn (3 chỗ có thể lỗi)
- Phải xử lý: retry, ack, DLQ, idempotency, backpressure
- Tốn tài nguyên + learning curve

### Khi nào dùng:

- Tác vụ chậm (> vài giây)
- Traffic đột biến
- Cần guarantee không mất việc
- Cần scale worker riêng

### Khi nào KHÔNG dùng:

- Tác vụ nhanh
- Traffic thấp và đều
- Team nhỏ, không có DevOps
- BackgroundTasks/Celery đủ rồi

### Quy tắc vàng:

> **Độ phức tạp của công cụ phải tương xứng với vấn đề cần giải quyết.**
> Đừng dùng RabbitMQ chỉ vì “nó nghe pro”. Hãy dùng vì nó **giải quyết được vấn đề cụ thể** mà giải pháp đơn giản hơn không làm được.

### Trước khi refactor, team cần thống nhất:

- [ ] Quy mô hiện tại và dự kiến (file/ngày)
- [ ] Pain point cụ thể đang muốn giải quyết
- [ ] Ai sẽ vận hành RabbitMQ
- [ ] SLA: chấp nhận trễ bao lâu, mất bao nhiêu %

-----

User → POST /upload → FastAPI:
   1. Lưu file
   2. Đẩy 1 "message" vào RabbitMQ: {file_id: 123, path: "..."}
   3. Trả 202 Accepted ngay lập tức (< 1s)

[Tách biệt hoàn toàn]

Worker (process riêng) → lắng nghe RabbitMQ:
   1. Lấy message ra
   2. Parse PDF, chunk, embed, lưu DB
   3. Báo cho RabbitMQ "xong rồi" (ack)


*Tài liệu chuẩn bị cho buổi thảo luận refactor luồng ingestion. Mọi câu hỏi/thảo luận, ping trong channel team.*