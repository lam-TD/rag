# Phân tích yêu cầu và thiết kế giải pháp

## Workflow hiện tại

```text
User → POST /upload → FastAPI:
    1. Lưu file (local disk / object storage — cần xác định)
    2. Parse PDF (10s)
    3. Chunking (5s)
    4. Gọi OpenAI embedding API (30s)
    5. Lưu vào vector DB (5s)
    → Trả response 200 OK (kèm file_id)
```

**Ghi chú bối cảnh hiện tại** (để argument vấn đề chính xác hơn):

- Tổng thời gian xử lý: ~50s/file → vượt timeout HTTP mặc định (30–60s) ở nhiều reverse proxy / load balancer.
- Validation đầu vào: hiện tại chưa rõ có check MIME type, file size, số trang PDF tối đa không.
- AuthN/AuthZ: chưa xác định ai được upload, có quota/rate limit không.
- Hành vi khi crash giữa chừng: mất state hoàn toàn, không phục hồi được.
- Chưa có audit trail (ai upload, lúc nào, file gì).

### Vấn đề

- Chạy tất cả trong 1 request → timeout + bad UX.
- Phụ thuộc vào bên thứ 3 (OpenAI) → nếu API chậm hoặc lỗi thì toàn bộ request fail mặc dù file đã được upload thành công.
- Không dễ dàng retry từng bước nếu có lỗi (ví dụ OpenAI API fail thì phải re-upload file).
- Không có visibility về tiến trình (user không biết đang ở bước nào, mất bao lâu nữa).
- Nếu muốn thêm bước mới (ví dụ virus scan) thì sẽ càng làm request chậm hơn.
- Nếu có nhiều request đồng thời thì sẽ làm quá tải server.
- **Tốn resource HTTP server**: 1 request chiếm 1 worker process suốt 50s → ít connection slot cho user khác, dễ exhaust pool khi traffic tăng.
- **Lãng phí chi phí OpenAI**: nếu user F5 hoặc client retry sau timeout → gọi embedding lại từ đầu. Không có idempotency / deduplication.
- **Không có observability**: không log được ai upload, lỗi ở bước nào, mất bao lâu — khó debug ở production.
- **Rủi ro DOS**: không có cap file size / page count → 1 file lớn (vd 500MB / 1000 trang) có thể block server lâu.
- **Không có dead letter**: job fail vĩnh viễn thì biến mất, không có chỗ điều tra root cause sau này.

### Nhu cầu và giải pháp

**Nhu cầu cốt lõi:**

- Tách thành các luồng khác nhau: HTTP (fast), xử lý file (chậm, async).
- Nếu có nhiều request đồng thời thì xử lý tuần tự theo queue → không quá tải server.
- Nếu muốn thêm bước mới thì chỉ cần thêm vào luồng xử lý, không ảnh hưởng đến luồng HTTP.
- Có thể retry từng bước nếu có lỗi, không phải re-upload file.
- User có visibility về tiến trình (ví dụ: "File uploaded thành công, đang xử lý...").

**Nhu cầu bổ sung (nên có cho production):**

- **Idempotency**: hash nội dung file → nếu trùng thì trả job cũ, không xử lý lại (tiết kiệm chi phí OpenAI, tránh duplicate trong vector DB).
- **Cancel job**: cho phép user huỷ job đang queue hoặc đang processing.
- **Cơ chế notification**: làm sao user biết khi xong? Các phương án:
  - Polling: `GET /jobs/{id}` → trả status + progress.
  - WebSocket / SSE: server push update real-time.
  - Email / webhook: thông báo khi hoàn thành.
- **Cleanup**: chính sách xoá file tạm — sau khi job xong? Sau N ngày? Khi storage đầy?
- **Rate limit**: giới hạn N file/phút/user để chống spam.
- **Backpressure**: khi queue quá dài thì reject request mới hay accept và báo ETA?
- **Priority queue**: file nhỏ ưu tiên hơn file lớn? User trả phí ưu tiên hơn?
- **Dead letter queue (DLQ)**: job fail nhiều lần đẩy vào DLQ để con người xem xét.

**Sơ đồ workflow mới:**

```text
User → POST /upload → FastAPI:
    1. Validate (MIME, size, page count)
    2. Hash file → check idempotency
    3. Lưu file (object storage)
    4. Tạo job record (status=queued) → trả về job_id
    5. Push job vào queue (file path, metadata, job_id)
    → Response 202 Accepted, { job_id, status: "queued" }

User → GET /jobs/{job_id} → FastAPI:
    → Trả status (queued / parsing / chunking / embedding / storing / completed / failed)
       + progress + error (nếu có)

Worker (background loop):
    1. Pull job từ queue
    2. Update job status = "parsing"
    3. Parse PDF (10s)
    4. Update status = "chunking" → Chunking (5s)
    5. Update status = "embedding" → Gọi OpenAI (30s)  [retry với backoff]
    6. Update status = "storing" → Lưu vector DB (5s)
    7. Update job status = "completed"
    [Nếu lỗi không retry được → status = "failed", push vào DLQ]
```

---

## Lựa chọn công nghệ giải pháp

### 1. Queue / Task Worker

Bối cảnh hiện tại: đang ở giai đoạn POC, chưa rõ scale tương lai. Ưu tiên đơn giản, dễ học,
dễ chuyển đổi khi cần, nhưng không muốn chọn công nghệ "chết yểu" sau 6 tháng.

#### So sánh các phương án

| Tiêu chí                     | Celery + Redis            | RQ (Redis Queue)        | Dramatiq                  | ARQ (async)              |
| ---------------------------- | ------------------------- | ----------------------- | ------------------------- | ------------------------ |
| Độ trưởng thành              | Rất cao (2009)            | Cao (2012)              | Trung bình (2017)         | Trung bình (2018)        |
| Độ phổ biến / cộng đồng      | Lớn nhất                  | Lớn                     | Vừa                       | Đang lên                 |
| Đường cong học               | Dốc — nhiều khái niệm     | Thoải — API rất gọn     | Vừa                       | Vừa (cần hiểu async)     |
| Phù hợp FastAPI (async)      | OK, nhưng sync-first      | Sync-only               | Sync-first                | **Async-native**         |
| Retry / scheduling           | Đầy đủ, mạnh              | Cơ bản, đủ dùng         | Mạnh, middleware tốt      | Đầy đủ                   |
| Monitoring UI                | Flower (tốt)              | rq-dashboard (đơn giản) | dramatiq-dashboard        | arq không có UI sẵn      |
| Broker                       | Redis / RabbitMQ / SQS    | Redis only              | Redis / RabbitMQ          | Redis only               |
| Boilerplate                  | Nhiều                     | Rất ít                  | Ít                        | Ít                       |
| Phù hợp POC                  | Hơi nặng                  | **Rất phù hợp**         | Phù hợp                   | Phù hợp                  |
| Đường nâng cấp khi scale lớn | Đã chứng minh ở scale lớn | Có thể chuyển Celery    | Chứng minh ở mid-scale    | Chưa nhiều case lớn      |

#### Phân tích cho use case này

- **Workload đặc trưng**: I/O-bound (gọi OpenAI 30s/file), không CPU-heavy. Worker chủ yếu chờ
  network → async (ARQ) về lý thuyết hiệu quả hơn, nhưng với throughput POC thì khác biệt
  không đáng kể.
- **Số bước trong pipeline**: 4 bước (parse, chunk, embed, store). Nếu muốn retry từng bước
  riêng biệt → cần "chain"/"pipeline" abstraction. Celery có canvas (chain/group/chord) mạnh
  nhất. RQ có dependency cơ bản. Dramatiq có pipeline. ARQ phải tự code.
- **Rủi ro OpenAI rate-limit**: Cần backoff + retry → mọi lựa chọn đều hỗ trợ, nhưng Celery
  và Dramatiq có chính sách retry tinh vi hơn.
- **POC → Production**: Nếu bắt đầu bằng RQ, sau này muốn chuyển sang Celery là một lần
  refactor nhỏ (API tương đồng). Bắt đầu bằng Celery thì over-engineering ở POC.

#### Quyết định

**→ Chọn RQ (Redis Queue) cho giai đoạn POC.**

Lý do:
- API gọn, ít boilerplate → triển khai POC nhanh.
- Đủ tính năng cần thiết: retry, scheduled job, job dependency cơ bản, rq-dashboard cho monitoring.
- Redis đã thường có sẵn trong stack (có thể dùng làm cache + queue + job status backend).
- Nếu scale lên cần Celery, đường migrate tương đối thẳng (cùng concept task/queue).

---

### 2. Storage cho file upload

> _(Sẽ điền sau)_

---

### 3. Vector DB

> _(Sẽ điền sau)_

---

### 4. Tracking tiến trình job

> _(Sẽ điền sau)_

---

### 5. PDF Parser & Chunking Strategy

> _(Sẽ điền sau)_

---

## Tiêu chí đánh giá và kiểm tra

### Tiêu chí đánh giá (Acceptance Criteria)

Hệ thống được coi là đạt yêu cầu khi đáp ứng các tiêu chí sau:

**Functional:**
- File PDF được parse → chunk → embed → lưu vào vector DB đầy đủ, không mất chunk.
- Vector trong DB có đúng dimension, đúng metadata (file_id, chunk_index, page).
- Query semantic search trên vector DB trả về chunk đúng từ file vừa upload.

**Performance:**
- HTTP endpoint `/upload`: p95 latency < 500ms (chỉ làm validate + push queue).
- HTTP endpoint `/jobs/{id}`: p95 < 100ms.
- Worker: xử lý 1 file PDF 20 trang trong < 60s end-to-end (95% trường hợp).
- Throughput: tối thiểu N file/phút (định lượng theo nhu cầu thực tế khi rõ scale).

**Reliability:**
- Retry success rate ≥ 95% (job fail tạm thời do OpenAI 429/5xx phải tự retry thành công).
- Dead-letter rate < 1% trên tổng số job.
- Worker crash giữa chừng → job được requeue, không mất.

**Cost:**
- Chi phí OpenAI embedding / file phù hợp với budget (định lượng cụ thể khi rõ pricing).
- Không gọi embedding trùng lặp với cùng nội dung file (idempotency).

**Observability:**
- Mọi job có structured log với job_id, file_id, user_id, step, duration, error.
- Metrics: queue depth, job duration p50/p95/p99, retry count, DLQ size.
- Trace từ HTTP request đến worker (correlation id xuyên suốt).

### Testing

**Unit test:**
- Test cô lập từng component: PDF parser, chunker, embedding wrapper, vector DB wrapper, job state machine.
- Mock external dependencies (OpenAI, vector DB).
- Coverage target: ≥ 80% trên business logic.

**Integration test (hit thật, không mock infra):**
- Spin up Redis + vector DB bằng `testcontainers` hoặc docker-compose dành riêng cho test.
- OpenAI: dùng VCR / recorded responses (rẻ + deterministic) thay vì hit thật mỗi lần CI.
- Test thật pipeline: enqueue job → worker xử lý → kiểm tra vector DB có data đúng.
- Test các kịch bản lỗi: OpenAI 429, OpenAI timeout, vector DB down → hệ thống retry / fail đúng.

**End-to-end (E2E) test:**
- Từ HTTP `POST /upload` → polling `GET /jobs/{id}` → vector DB có dữ liệu.
- Test với file PDF thật ở nhiều kích thước, ngôn ngữ.

**Load / stress test:**
- Đo throughput thực tế của worker (file/phút).
- Đo p95/p99 latency của HTTP endpoint dưới tải.
- Tìm điểm gãy: queue depth bao nhiêu thì latency vọt? OOM ở mức nào?

**Chaos test:**
- Kill worker giữa chừng → job có được requeue không?
- Redis down trong vài giây → HTTP có degrade gracefully không?
- OpenAI trả 429 liên tục → backoff có hoạt động không, có chuyển DLQ sau N retry không?

**Smoke test sau deploy:**
- Một test ngắn chạy ngay sau khi deploy: upload file mẫu → verify pipeline ok.

**Security test:**
- Upload file không phải PDF (đổi extension) → bị reject.
- Upload PDF chứa payload độc hại (PDF bomb, JS, oversized) → bị reject hoặc cô lập an toàn.
- Upload vượt quá rate limit → bị chặn.

**Automation (CI):**
- Mỗi PR: lint + format + type check + unit test + integration test (với services từ container).
- Nightly: full E2E + load test (subset).
- Trên merge vào main: deploy staging + smoke test tự động.
