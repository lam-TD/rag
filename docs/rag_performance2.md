# 01 — Problem Framing (Giai đoạn Socratic)

## Quá trình mài bài toán (Socratic — đã hội tụ)

Triệu chứng ban đầu: "3 user upload 10MB → quá tải". Qua hỏi-đáp, đã bóc 2 mâu thuẫn và định vị lại đúng nút thắt:

1. **"Embedding ngốn 99% CPU"** mâu thuẫn với **"embedding gọi API ngoài"** → đã xác minh: khâu ngốn CPU thực sự là **parse PDF→text**, không phải embedding.
2. **"3 user đồng thời gây sập"** mâu thuẫn với **"xử lý tuần tự 1 job/lúc"** → nếu chỉ 1 job chạy thì 3 upload không thể làm vỡ *do xử lý*. Nguyên nhân thật: việc parse CPU-bound chạy **chung process uvicorn** (background task trong lifespan) → **chặn event loop** → chat đói CPU/treo.

## Phát biểu bài toán sau khi mài
>
> Không phải "hệ thống quá tải khi 3 người upload". Mà là: **một tác vụ CPU-bound (parse PDF) chạy chung tiến trình với web server, không bị cô lập, nên khi nó chạy thì tiến trình phục vụ chat bị đói CPU và treo.** "3 user" chỉ là cách kích hoạt cho thấy triệu chứng, không phải nguyên nhân. Bài toán = **cô lập + giới hạn ngân sách CPU cho tác vụ nặng** để chat luôn còn CPU, trong giới hạn 2core/2GB.

## Giả thuyết ngầm cần kiểm chứng

| Giả thuyết | Nếu sai thì sao? | Cách kiểm chứng rẻ nhất |
|---|---|---|
| CPU 99% là do parse PDF, không phải embedding | Chữa nhầm khâu, vô ích | `py-spy dump`/log timestamp từng bước lúc CPU cháy |
| Parse chạy chung event loop → chặn chat | Nếu đã tách process thì frame sai | Xem code: parse gọi trực tiếp trong coroutine, hay `run_in_executor`/process riêng? |
| Parse là pure-Python (giữ GIL) | Nếu nhả GIL (pymupdf) thì offload thread đủ, không cần tách process | Kiểm thư viện parse đang dùng |
| RAM không phải nút thắt chính | Nếu parse 10MB phình >1GB → OOM là rủi ro song song, phải xử lý cùng lúc | `docker stats` lúc parse 1 file |

## Phạm vi: trong / ngoài

- **Trong:** cô lập tác vụ parse khỏi tiến trình chat; giới hạn CPU/RAM cho tác vụ nặng; giữ chat khả dụng; (có thể) giảm chi phí parse.
- **Ngoài (cố ý loại bỏ):** nâng cấu hình server (cấm); đổi sang embedding local; tối ưu chất lượng RAG/retrieval; autoscale nhiều máy.

## Chốt cổng: ta đã đồng thuận "đây là đúng bài toán" chưa? ☐ (chờ người dùng xác nhận phát biểu bài toán ở trên)
