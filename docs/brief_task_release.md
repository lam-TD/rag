# Brief: Phương pháp lựa chọn task cho version tiếp theo

**Lưu ý:** Một số thông tin chưa được cung cấp đầy đủ (quy mô team, số lượng task ứng viên, effort trung bình/task, buffer đã có...). Các điểm dưới đây được đánh dấu rõ đâu là **giả định** và đâu là **fact** đã cung cấp.

---

## 1. Khuyến nghị chính

Cách tiếp cận "ưu tiên cao nhất → estimate → check test gap → lấp đầy thời gian dư" là **đúng hướng nhưng thiếu 2 bước kiểm soát rủi ro quan trọng**: buffer cho unknown/bug-fix, và điểm cắt (cut-line) rõ ràng khi task mới phát sinh giữa chừng.

## 2. 5 điều cần biết

| # | Điểm | Nguồn |
|---|------|-------|
| 1 | Dev deadline (30/09) và QC deadline (30/10) chỉ cách nhau 1 tháng — đây là thời gian test, không phải thời gian "dự phòng" cho dev trễ. | Fact (đã cung cấp) |
| 2 | Việc "check thiếu test thì bổ sung" nên áp dụng cho **integration test**, không nên áp dụng cho manual test ở giai đoạn dev — manual test thường thuộc phase QC. | Giả định dựa trên thực hành phổ biến |
| 3 | Task ưu tiên cao nhất cần tiêu chí rõ ràng (business impact, risk nếu không làm, dependency) — nếu không, "ưu tiên cao nhất" dễ bị cảm tính. | Opinion / best practice |
| 4 | Nếu chọn thêm task khi dư thời gian, mỗi task thêm vào đều kéo theo test effort tương ứng (không chỉ dev effort) — dễ bị bỏ sót khi estimate. | Opinion, dựa trên rủi ro thường gặp |
| 5 | Chưa rõ số lượng task ứng viên và effort trung bình — nếu không có, không thể tính được "dư thời gian" một cách đáng tin cậy. | **Thiếu thông tin — cần bổ sung** |

## 3. 3 rủi ro lớn nhất

1. **Rủi ro lịch trình:** Không có buffer cho việc integration test phát hiện lỗi cần fix lại → có thể đẩy lùi QC deadline.
2. **Rủi ro scope creep:** "Nếu dư thời gian thì chọn thêm task" dễ dẫn đến thêm task giữa chừng mà không re-estimate lại toàn bộ timeline.
3. **Rủi ro chất lượng test:** Bổ sung test "khi thấy thiếu" là phản ứng bị động — nên có checklist test coverage tối thiểu *trước khi* bắt đầu task, không phải phát hiện giữa chừng.

## 4. Điều người ta hay hiểu sai

- Nhiều team nghĩ "1 tháng để QC" là dư dả — thực tế thời gian này thường bị ăn vào bởi bug-fix loop (QC tìm lỗi → dev sửa → QC test lại), không phải QC thuần túy.
- "Task ưu tiên cao nhất" thường bị nhầm với "task khẩn cấp nhất" — hai khái niệm khác nhau (impact vs urgency).

## 5. So sánh phương án

| Tiêu chí | A: Ưu tiên chặt (chỉ làm task top, giữ buffer) | B: Ưu tiên + lấp đầy thời gian dư (cách đề xuất ban đầu) |
|---|---|---|
| Tốc độ deliver | Chậm hơn nhưng chắc | Có thể nhanh hơn nếu mọi thứ suôn sẻ |
| Rủi ro trễ deadline | Thấp | Trung bình-cao (không buffer) |
| Effort quản lý | Thấp | Cao hơn (cần theo dõi liên tục) |
| Chất lượng test | Ổn định nếu có checklist trước | Dễ bị bỏ sót nếu chỉ "check khi thấy thiếu" |
| Phù hợp khi | Deadline cứng, rủi ro cao | Đội ngũ có kinh nghiệm, task nhỏ, rõ ràng |

## 6. Thông tin còn thiếu & câu hỏi phản biện

**Thiếu:**
- Số lượng task ứng viên và effort estimate của từng task
- Team size / số dev, QC hiện có
- Buffer đã tính trong 30 ngày (30/09 → 30/10) hay chưa

**Câu hỏi một manager khó tính sẽ hỏi:**
- "Nếu integration test phát hiện lỗi nghiêm trọng ở task ưu tiên cao nhất, ai chịu trách nhiệm re-plan?"
- "Task 'thêm vào khi dư thời gian' có được tính vào QC deadline 30/10 không, hay ngầm hiểu là optional?"
- "Tiêu chí nào xác định 'task ưu tiên cao nhất' — dựa trên số liệu gì?"

## 7. Kết luận

**Đề xuất chọn phương án A (ưu tiên chặt, giữ buffer)** vì khoảng cách 1 tháng giữa dev và QC deadline là khá sát, không có nhiều dư địa để chấp nhận rủi ro từ việc mở rộng scope giữa chừng.

**Điều duy nhất có thể thay đổi kết luận này:** nếu team xác nhận đã có sẵn buffer riêng (ví dụ QC deadline 30/10 đã tính dư 20-30% cho bug-fix loop) và các task ứng viên thêm vào đều nhỏ, độc lập, không có dependency phức tạp.

---

*Brief này cần được bổ sung thêm danh sách task cụ thể + effort ước tính để có bảng ưu tiên chi tiết hơn.*
