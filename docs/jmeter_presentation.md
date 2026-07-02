# Kế hoạch họp team: Thuyết trình Performance Testing với JMeter

## 1. Mục tiêu buổi họp

Thống nhất hướng thuyết trình và phân chia nhiệm vụ cho nhóm 4 người.

Mục tiêu chính của bài thuyết trình không chỉ là **giới thiệu JMeter**, mà là:

> Biết dùng JMeter để đo hiệu năng, phân tích kết quả, tìm bottleneck và đưa ra quyết định cải thiện performance.

---

## 2. Đề tài thống nhất

### Tên đề tài đề xuất

**Performance Testing với JMeter: Từ đo tải đến quyết định cải thiện hệ thống**

Hoặc ngắn hơn:

**Dùng JMeter để phát hiện bottleneck và cải thiện hiệu năng ứng dụng**

### Lý do chọn đề tài này

- Có tính ứng dụng cao trong dự án thực tế.
- Phù hợp với backend, API, web app, hệ thống nội bộ.
- Dễ chia việc cho 4 người.
- Có thể demo trực quan bằng API và report.
- Ít rủi ro đạo đức/pháp lý hơn so với demo tấn công Man-in-the-Middle.
- Giúp người nghe hiểu cách ra quyết định kỹ thuật dựa trên dữ liệu đo được.

---

## 3. Thông điệp chính của bài thuyết trình

JMeter không trực tiếp tối ưu hệ thống.

JMeter giúp chúng ta:

1. Giả lập nhiều user truy cập cùng lúc.
2. Đo response time, throughput, error rate.
3. Phát hiện hệ thống bắt đầu chậm hoặc lỗi ở mức tải nào.
4. Kết hợp với log, CPU, RAM, database metrics để tìm bottleneck.
5. Đưa ra quyết định cải thiện: optimize query, thêm cache, scale server, queue background job, rate limit, v.v.

Thông điệp cần nhấn mạnh:

> Không đo thì không biết hệ thống yếu ở đâu.  
> Có số liệu thì mới ra quyết định cải thiện performance đúng hướng.

---

## 4. Bài toán thực tế dùng để dẫn dắt

### Scenario đề xuất

Một API chạy ổn khi ít user, nhưng khi 50–100 user truy cập cùng lúc thì:

- Response time tăng cao.
- Một số request bị timeout.
- Error rate bắt đầu xuất hiện.
- Người dùng cảm thấy hệ thống chậm hoặc không ổn định.

Câu hỏi đặt ra:

> Làm sao biết vấn đề nằm ở application code, database, server, network hay cấu hình hệ thống?

---

## 5. Dàn ý thuyết trình đề xuất

## Phần 1: Vấn đề performance trong dự án

### Nội dung

- Vì sao performance testing quan trọng?
- Hệ thống có thể chạy tốt khi ít user nhưng lỗi khi nhiều user.
- Các triệu chứng thường gặp:
  - API phản hồi chậm.
  - Timeout.
  - Error rate tăng.
  - CPU/RAM tăng bất thường.
  - Database query chậm.
  - User phàn nàn hệ thống lag hoặc không ổn định.

### Câu hỏi tương tác

> Mọi người từng gặp app/web nào bị chậm hoặc sập khi nhiều người dùng chưa? Lúc đó ảnh hưởng thế nào?

---

## Phần 2: Cần đo gì trước khi dùng JMeter?

### Nội dung

Trước khi chạy test, cần xác định các chỉ số quan trọng.

| Chỉ số | Ý nghĩa |
|---|---|
| Response time | Một request mất bao lâu để hoàn thành |
| Average response time | Thời gian phản hồi trung bình |
| p95 / p99 | 95% hoặc 99% request nhanh hơn mức này |
| Throughput | Số request xử lý được mỗi giây |
| Error rate | Tỷ lệ request lỗi |
| CPU / RAM | Server có bị quá tải không |
| DB query time | Database có phải bottleneck không |

### Điểm cần nhấn mạnh

Không nên chỉ nhìn **average response time**.

Ví dụ:

- Average = 500ms có vẻ ổn.
- Nhưng p95 = 5s nghĩa là 5% user vẫn gặp trải nghiệm rất chậm.

### Câu hỏi tương tác

> Theo mọi người, vì sao chỉ nhìn average response time có thể gây hiểu lầm?

---

## Phần 3: JMeter là gì và dùng để làm gì?

### Nội dung

JMeter là công cụ dùng để giả lập tải lên hệ thống.

Có thể dùng để test:

- API.
- Web application.
- Database.
- Service nội bộ.

### Các loại performance test

| Loại test | Mục đích |
|---|---|
| Load test | Kiểm tra hệ thống dưới mức tải kỳ vọng |
| Stress test | Tăng tải đến khi hệ thống bắt đầu hỏng |
| Spike test | Kiểm tra khi traffic tăng đột ngột |
| Endurance test | Chạy lâu để phát hiện memory leak hoặc degradation |

### Câu hỏi tương tác

> Load test và Stress test khác nhau ở điểm nào?

---

## Phần 4: Demo thực hành với JMeter

### Demo nên làm theo case study

Không nên chỉ demo thao tác tool.  
Nên demo theo một bài toán cụ thể.

### Kịch bản demo đề xuất

Test một API giả lập, ví dụ:

- `GET /search`
- `POST /login`
- `POST /upload`
- `GET /products`

Chạy test với các mức tải:

| Số user giả lập | Mục tiêu |
|---|---|
| 10 users | Baseline, xem hệ thống hoạt động bình thường |
| 50 users | Kiểm tra mức tải trung bình |
| 100 users | Kiểm tra khi hệ thống bắt đầu quá tải |

### Kết quả demo mẫu

| Users | Avg response | p95 | Error rate | Nhận xét |
|---|---:|---:|---:|---|
| 10 | 300ms | 600ms | 0% | Ổn |
| 50 | 900ms | 2.5s | 1% | Bắt đầu chậm |
| 100 | 3s | 8s | 12% | Không ổn |

### Câu hỏi tương tác

> Nhìn vào kết quả này, mọi người đoán bottleneck có thể nằm ở đâu?

---

## Phần 5: Từ kết quả JMeter đến quyết định cải thiện performance

Đây là phần quan trọng nhất của bài.

| Dấu hiệu khi test | Có thể là vấn đề | Quyết định cải thiện |
|---|---|---|
| Response time cao, CPU app cao | Code xử lý nặng | Optimize code, dùng async, chuyển task nặng sang background job |
| Response time cao, DB CPU cao | Query chậm hoặc thiếu index | Thêm index, optimize query, kiểm tra connection pool |
| Error rate tăng khi user tăng | App quá tải | Scale instance, rate limit, tăng resource |
| p95/p99 cao nhưng average ổn | Một nhóm request bị chậm bất thường | Check slow query, external API, lock, file I/O |
| RAM tăng dần khi chạy lâu | Có thể có memory leak | Profiling, kiểm tra resource cleanup |
| Throughput không tăng dù tăng thread | Có bottleneck cố định | Kiểm tra DB, app worker, network hoặc external service |

### Thông điệp cần chốt

> Số liệu từ JMeter chỉ là điểm bắt đầu.  
> Muốn ra quyết định đúng, cần kết hợp thêm monitoring, logs và database metrics.

---

## Phần 6: Best practices và lỗi thường gặp

### Best practices

- Xác định mục tiêu test trước khi chạy.
- Có baseline để so sánh.
- Test trên môi trường gần giống production.
- Không test nhầm production nếu chưa được phép.
- Theo dõi cả JMeter report và server metrics.
- Chuẩn bị dữ liệu test đủ thực tế.
- Dùng HTML report để trình bày kết quả dễ hiểu.
- Với tải lớn, không nên chạy bằng JMeter GUI mode.

### Lỗi thường gặp

- Nghĩ rằng performance testing chính là optimization.
- Chạy test nhưng không biết tiêu chí pass/fail.
- Chỉ nhìn average response time.
- Bỏ qua p95/p99.
- Không theo dõi CPU/RAM/DB khi test.
- Tăng số thread quá cao rồi kết luận sai.
- Demo live nhưng không có phương án dự phòng.

---

## 6. Phân chia nhiệm vụ cho 4 người

| Người | Phụ trách chính | Deliverable cần chuẩn bị |
|---|---|---|
| Người 1 | Bối cảnh performance và bài toán thực tế | Slide mở đầu, ví dụ thực tế, câu hỏi tương tác 1 |
| Người 2 | Metrics và JMeter concept | Slide về metrics, loại test, JMeter overview, câu hỏi tương tác 2 |
| Người 3 | Demo JMeter | File `.jmx`, API demo, kết quả chạy test, screenshot/report dự phòng |
| Người 4 | Phân tích kết quả và quyết định cải thiện | Bảng mapping kết quả → bottleneck → action, best practices, câu hỏi ôn tập, tổng kết |

---

## 7. Nhiệm vụ chi tiết từng người

## Người 1: Bối cảnh và mở đầu

### Cần chuẩn bị

- Vấn đề performance trong dự án thực tế.
- Ví dụ app/web bị chậm khi nhiều user.
- Giải thích vì sao cần đo thay vì đoán.
- Dẫn vào scenario chính của bài.

### Output

- 2–3 slide.
- 1 câu hỏi tương tác.
- 1 ví dụ thực tế dễ hiểu.

---

## Người 2: Metrics và JMeter overview

### Cần chuẩn bị

- Response time.
- Average vs p95/p99.
- Throughput.
- Error rate.
- Load test, Stress test, Spike test, Endurance test.
- JMeter dùng để làm gì.

### Output

- 3–4 slide.
- Bảng giải thích metrics.
- Câu hỏi tương tác về Load test vs Stress test.

---

## Người 3: Demo JMeter

### Cần chuẩn bị

- Một API demo.
- Một test plan JMeter.
- Chạy test với 10, 50, 100 users.
- Kết quả test.
- Screenshot hoặc HTML report dự phòng.
- File `.jmx` để backup.

### Output

- Demo live hoặc video demo.
- Report kết quả.
- Bảng kết quả ngắn gọn.
- Câu hỏi tương tác về bottleneck.

### Lưu ý

Người 3 nên chuẩn bị kỹ nhất vì demo dễ lỗi.

Bắt buộc có phương án dự phòng:

- Screenshot kết quả.
- HTML report.
- Video demo ngắn.
- File `.jmx`.

---

## Người 4: Phân tích và tổng kết

### Cần chuẩn bị

- Cách đọc kết quả JMeter.
- Mapping kết quả sang bottleneck.
- Đề xuất hướng cải thiện performance.
- Best practices.
- Lỗi thường gặp.
- 3 câu hỏi ôn tập cuối bài.

### Output

- 3–4 slide.
- Bảng quyết định kỹ thuật.
- Slide tổng kết.
- 3 câu hỏi ôn tập.

---

## 8. Checklist chuẩn bị chung

## Nội dung

- [ ] Chốt tên đề tài.
- [ ] Chốt scenario demo.
- [ ] Chốt API dùng để test.
- [ ] Chốt các mức tải: 10, 50, 100 users.
- [ ] Chốt metrics cần trình bày.
- [ ] Chốt format report.
- [ ] Chốt người thuyết trình từng phần.

## Demo

- [ ] API demo chạy được.
- [ ] JMeter test plan chạy được.
- [ ] File `.jmx` đã lưu.
- [ ] Có screenshot kết quả.
- [ ] Có HTML report.
- [ ] Có video demo dự phòng nếu cần.
- [ ] Không phụ thuộc hoàn toàn vào internet hoặc môi trường live.

## Slide

- [ ] Slide dùng cùng một format.
- [ ] Không quá nhiều chữ.
- [ ] Có diagram hoặc bảng minh họa.
- [ ] Có phần before/after nếu làm được.
- [ ] Có câu hỏi tương tác.
- [ ] Có slide tổng kết.

---

## 9. Agenda buổi họp team

Thời lượng đề xuất: 30–45 phút.

| Thời gian | Nội dung |
|---|---|
| 5 phút | Thống nhất mục tiêu bài thuyết trình |
| 5 phút | Chốt tên đề tài và thông điệp chính |
| 10 phút | Review dàn ý từng phần |
| 10 phút | Phân chia nhiệm vụ cho 4 người |
| 5 phút | Chốt demo và phương án backup |
| 5 phút | Chốt deadline và output từng người |

---

## 10. Quyết định cần chốt trong buổi họp

- Tên đề tài cuối cùng là gì?
- Demo dùng API nào?
- Có làm before/after optimization không?
- Ai phụ trách chuẩn bị API demo?
- Ai phụ trách thiết kế slide chung?
- Deadline gửi nội dung từng phần là ngày nào?
- Deadline chạy thử demo là ngày nào?
- Có cần quay video demo backup không?

---

## 11. Đề xuất timeline

| Mốc thời gian | Việc cần hoàn thành |
|---|---|
| Ngày 1 | Chốt đề tài, dàn ý, phân công |
| Ngày 2 | Mỗi người hoàn thành draft nội dung phần mình |
| Ngày 3 | Hoàn thành API demo và JMeter test plan |
| Ngày 4 | Chạy thử demo, lấy report, sửa slide |
| Ngày 5 | Rehearsal toàn bộ bài thuyết trình |
| Trước ngày trình bày | Chuẩn bị backup: screenshot, report, video, file `.jmx` |

---

## 12. Câu hỏi ôn tập cuối bài

1. JMeter dùng để làm gì trong performance testing?
2. Load test và Stress test khác nhau như thế nào?
3. Vì sao không nên chỉ nhìn average response time?
4. Kể tên 3 metrics quan trọng khi đọc kết quả performance test.
5. Nếu p95 cao nhưng average vẫn ổn, ta nên nghi ngờ vấn đề gì?
6. Khi error rate tăng mạnh lúc tăng số user, có thể đưa ra những hướng xử lý nào?

---

## 13. Kết luận cho team

Hướng thuyết trình nên tránh biến thành một bài tutorial JMeter đơn thuần.

Bài nên đi theo flow:

> Problem → Metrics → JMeter → Demo → Result → Bottleneck → Decision

Mục tiêu cuối cùng:

> Người nghe hiểu cách dùng JMeter để hỗ trợ quyết định cải thiện performance trong dự án thực tế.
