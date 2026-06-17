# Kế hoạch test: So sánh Latency & Chi phí (Tóm tắt/Trích xuất văn bản — Chat API)

> **Lưu ý trước khi bắt đầu:** Hãy xác nhận lại trên dashboard OpenAI rằng các model name (`gpt-5-mini`, `gpt-5.4-mini`) và các mức reasoning effort (`minimal`, `none`, `low`, `medium`) thực sự tồn tại và được Chat API chấp nhận. Nếu một config không hợp lệ, API sẽ trả lỗi và làm hỏng phép so sánh.

## 1. Ma trận test (test matrix)

|Config ID|Version|Model       |Reasoning effort|
|---------|-------|------------|----------------|
|A        |v1.1.0 |gpt-5-mini  |minimal         |
|B        |v1.2.0 |gpt-5.4-mini|none            |
|C        |v1.2.0 |gpt-5.4-mini|low             |
|D        |v1.2.0 |gpt-5.4-mini|medium          |

→ 4 config cần so sánh trực tiếp với nhau.

## 2. Bộ dữ liệu test

|Yếu tố           |Thiết kế                                                            |
|-----------------|--------------------------------------------------------------------|
|Số mẫu văn bản   |≥ 30 (lý tưởng 50+) để latency có ý nghĩa thống kê                  |
|Phân tầng độ dài |Ngắn (~500 token), trung bình (~2.000), dài (~8.000) — chia đều nhóm|
|Loại nội dung    |Đồng nhất theo use case thực tế (báo cáo, email, tài liệu…)         |
|Prompt           |Cố định, giống hệt nhau cho cả 4 config                             |
|max_tokens output|Cố định cùng một giá trị để output không lệch nhau                  |

Giữ mọi biến giống nhau giữa các config — chỉ thay model + effort.

## 3. Chỉ số đo (metrics)

### Latency

|Metric                    |Ý nghĩa                                           |
|--------------------------|--------------------------------------------------|
|TTFT (time to first token)|Độ trễ cảm nhận; chỉ đo được nếu bật `stream=true`|
|Total latency             |Tổng thời gian từ request đến token cuối          |
|p50 / p90 / p99           |Phân vị, quan trọng hơn giá trị trung bình        |
|Latency theo độ dài input |Tách riêng theo nhóm ngắn/TB/dài                  |

### Chi phí

|Metric               |Nguồn                                                                                                                         |
|---------------------|------------------------------------------------------------------------------------------------------------------------------|
|Input tokens         |`usage.prompt_tokens`                                                                                                         |
|Output tokens        |`usage.completion_tokens`                                                                                                     |
|Reasoning tokens     |`usage.completion_tokens_details.reasoning_tokens` (nếu có) — tính phí như output, là điểm khác biệt chính giữa các mức effort|
|Cost/request         |Tính theo đơn giá từng model                                                                                                  |
|Cost trung bình + p90|Tổng hợp                                                                                                                      |

Reasoning tokens là yếu tố then chốt: effort càng cao thì reasoning tokens càng nhiều → chi phí và latency tăng.

## 4. Quy trình chạy

|Bước                    |Chi tiết                                                                |
|------------------------|------------------------------------------------------------------------|
|Warm-up                 |Bỏ 2–3 request đầu mỗi config (loại nhiễu cold-start)                   |
|Lặp lại                 |Mỗi mẫu chạy ≥ 3 lần/config, lấy trung vị để giảm nhiễu mạng            |
|Tuần tự, không song song|Chạy nối tiếp để latency không bị nhiễu do tranh tài nguyên             |
|Cùng thời điểm          |Chạy 4 config xen kẽ theo từng mẫu, tránh so sánh chéo giờ tải khác nhau|
|Ghi log raw             |Lưu lại từng response + usage + timestamp để audit                      |
|Cố định seed/params     |temperature, top_p… giống nhau giữa các config                          |

## 5. Mẫu bảng kết quả

|Config|p50 latency|p90 latency|TTFT p50|Avg input tok|Avg output tok|Avg reasoning tok|Cost/req|Chất lượng*|
|------|-----------|-----------|--------|-------------|--------------|-----------------|--------|-----------|
|A     |           |           |        |             |              |                 |        |           |
|B     |           |           |        |             |              |                 |        |           |
|C     |           |           |        |             |              |                 |        |           |
|D     |           |           |        |             |              |                 |        |           |

*Dù chỉ đo latency, nên thêm cột kiểm tra chất lượng tối thiểu (eyeball 5–10 mẫu) — vì effort=none có thể nhanh/rẻ nhưng tóm tắt kém, khiến so sánh thuần latency gây hiểu nhầm.

## 6. Cách tính P50 / P90

P50 và P90 là giá trị phân vị (percentile), mô tả phân bố latency tốt hơn giá trị trung bình.

- **P50** (trung vị): 50% request nhanh hơn giá trị này → độ trễ “điển hình”.
- **P90**: 90% request nhanh hơn (hoặc bằng), chỉ 10% chậm hơn → độ trễ “trường hợp xấu” phổ biến.

**Công thức (nearest-rank):** sắp xếp latency tăng dần, lấy giá trị tại vị trí `P/100 × N` (N = số mẫu).

Ví dụ 10 request (giây): `0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.5, 1.8, 2.4, 5.0`

- P50 → vị trí 5 → **1.2s**
- P90 → vị trí 9 → **2.4s**
- Trung bình = 1.7s (bị kéo lệch bởi mẫu 5.0s → lý do dùng percentile thay vì mean)

```python
import numpy as np

latencies = [0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.5, 1.8, 2.4, 5.0]
p50 = np.percentile(latencies, 50)
p90 = np.percentile(latencies, 90)
```

Có nhiều phương pháp nội suy (nearest-rank, linear interpolation…) nên kết quả lệch nhẹ ở bộ nhỏ — dùng thư viện là chuẩn nhất.

## 7. Lưu ý làm sai lệch kết quả

- Latency phụ thuộc tải server OpenAI theo thời điểm → đừng kết luận từ một lần chạy duy nhất.
- Nên chạy lại toàn bộ matrix ở 2–3 khung giờ khác nhau nếu cần độ tin cậy cao.
- Reasoning effort cao thường làm “đuôi” phân bố dài ra (một số request sinh nhiều reasoning token bất thường → chậm hẳn). P90 bắt được hiện tượng này, mean thì che mất.