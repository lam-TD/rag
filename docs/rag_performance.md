# 00 — Context Brief

**Loại dự án:** ☒ THẬT  ☐ GIẢ ĐỊNH

## Bài toán một câu
>
> Khi xử lý file upload, hệ thống RAG ngốn CPU đến mức **không phục vụ được chat song song** — cần giữ cho endpoint chat luôn đáp ứng khi đang xử lý file, trong giới hạn server cố định 2 core / 2GB.

## Ràng buộc định lượng

| Hạng mục | Giá trị | Nguồn / Cơ sở | FACT / INFERENCE |
|---|---|---|---|
| Quy mô người dùng / traffic | Mục tiêu chịu được **3 user upload đồng thời**, mỗi file ~10MB (PDF) | Người dùng cấp | FACT |
| Tăng trưởng dự kiến | Chưa cấp | — | — |
| Ngân sách (CAPEX/OPEX) | Server **không thể nâng cấp** (cứng) | Người dùng cấp | FACT |
| Quy mô & kỹ năng team | Chưa cấp | — | — |
| SLA / SLO | "Không sập + vẫn chat được" khi 3 user upload | Người dùng cấp | FACT |
| Stack hiện có / lock-in | FastAPI (uvicorn), RabbitMQ, Docker container | Người dùng cấp | FACT |
| Deadline / mốc thời gian | Chưa cấp | — | — |
| Ràng buộc pháp lý/tuân thủ | Chưa cấp | — | — |
| **Cấu hình server** | **2 core / 2GB RAM** (cứng, không nâng) | Người dùng cấp | FACT |
| Embedding | **Gọi API model ngoài** (I/O-bound, không tốn CPU local) | Người dùng cấp | FACT |
| Cơ chế xử lý | Upload → lưu file, trả **202**; xử lý nền **tuần tự (1 job/lúc)** qua khóa hàng đợi; RabbitMQ chỉ chuyển thông báo | Người dùng cấp | FACT |
| Nơi chạy xử lý nền | **Trong chính process uvicorn** (background task khởi từ FastAPI lifespan) | Người dùng cấp | FACT |
| Khâu ngốn CPU | **Đọc/parse file PDF→text** chiếm ~99% CPU (KHÔNG phải embedding) | Người dùng cấp | FACT |

## Phi-chức năng ưu tiên (xếp hạng)

1. **Khả dụng của chat khi đang xử lý file** (chat không được treo/timeout).
2. **Không sập / không OOM** ở 2core-2GB khi 3 user upload.
3. **Throughput xử lý file** (có thể chậm, miễn không chết) — ưu tiên thấp nhất.

## Điều CHƯA biết (rủi ro lớn nhất nếu đoán sai)

- **RAM đỉnh khi parse 1 PDF 10MB** là bao nhiêu? (PDF có thể phình hàng trăm MB khi render → rủi ro OOM thứ cấp dù CPU là triệu chứng chính.)
- Parse là **thuần Python** (giữ GIL) hay dùng **C-extension nhả GIL** (pymupdf...)? → quyết định việc offload sang thread có đủ hay buộc phải tách process.
- **Cách parse được gọi** trong code: (a) gọi thẳng trong coroutine, (b) `run_in_executor` (thread), hay (c) process riêng? → ngã rẽ lớn nhất của options. **CHƯA rõ.**

### Đã giải quyết
- **OCR:** KHÔNG có (PDF không cần OCR ảnh) → parse chỉ là trích xuất text, bớt 1 nguồn ngốn CPU lớn. `[FACT]` người dùng cấp.
- **uvicorn worker = 1** `[FACT]` → web server + background parse **dùng chung 1 process / 1 event loop**. Đây là xác nhận mạnh cho frame ở `01`: chỉ có đúng 1 tiến trình phục vụ tất cả, nên parse CPU-bound chặn nó là chat chết.

## Tiêu chí thành công (đo được)

- Khi 3 user upload 10MB đồng thời: container **không restart/OOMKilled**.
- Trong lúc xử lý file, request chat trả lời **dưới ngưỡng X giây** (cần chốt X) thay vì treo/timeout.
- CPU của process phục vụ chat **không bị đói** (luôn còn phần CPU cho chat).
