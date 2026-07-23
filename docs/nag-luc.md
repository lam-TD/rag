# Decision Brief: Nâng cấp kiến thức cho đội nhóm Dev

**Chủ đề:** Lập trình web, tư duy thiết kế hệ thống, tư duy test
**Đối tượng:** Dev (cơ bản) + Leader (nâng cao)
**Ngày lập:** 23/07/2026

---

## PHẦN I — DECISION BRIEF

### 1. Khuyến nghị điều hành

Chọn **3 chủ đề trục xuyên suốt** — *Kiến trúc web hiện đại*, *Tư duy thiết kế hệ thống*, *Testing chiến lược* — và chạy theo mô hình **hai tầng**: Dev học nền tảng qua bài tập thực tế trên codebase thật, Leader học ra quyết định qua case study và design review.

Không tách thành hai chương trình riêng, mà **cùng một chủ đề, khác độ sâu và khác sản phẩm đầu ra**.

---

### 2. Năm điều cần biết

**1. Chương trình thất bại vì thiếu sản phẩm đầu ra, không phải thiếu nội dung.**
*(Ý kiến, dựa trên mô hình phổ biến)*
Team học xong buổi seminar rồi quay lại code như cũ. Mỗi chủ đề cần buộc ra một artifact: một ADR, một bộ test, một refactor có PR.

**2. "Dev cơ bản" và "Leader nâng cao" không nên là hai lớp học.**
*(Ý kiến)*
Cùng chủ đề, Leader đóng vai reviewer cho bài của Dev. Leader học cách phản biện thiết kế — đây chính là kỹ năng nâng cao thật sự, không phải học thêm framework.

**3. Testing là nơi có ROI nhanh nhất nhưng bị dạy sai nhiều nhất.**
*(Ý kiến + thực tiễn ngành)*
Đa số team dạy "cách viết unit test" thay vì "test cái gì và tại sao". Kim tự tháp test cổ điển đã bị tranh luận nhiều; mô hình "testing trophy" (nghiêng về integration test) phù hợp hơn với web app hiện đại.

**4. System design cho Dev cơ bản nên bắt đầu từ dữ liệu, không phải từ microservices.**
*(Ý kiến)*
Data modeling, transaction boundary, index, N+1 query — đây là thứ Dev gặp hàng ngày. Kafka và service mesh là nội dung cho Leader hoặc là nội dung sai thời điểm.

**5. Web hiện đại đang dịch chuyển về phía server.**
*(Giả định — cần kiểm chứng với stack cụ thể của bạn)*
Server components, streaming SSR, edge rendering đang thay đổi cách chia frontend/backend. Nếu team đang dùng React/Next hoặc tương đương, đây là chủ đề có giá trị ngay.

---

### 3. Ba rủi ro lớn nhất

| Rủi ro | Mô tả | Giảm thiểu |
|---|---|---|
| **Adoption** | Team coi buổi học là gánh nặng ngoài giờ, tham gia hình thức | Gắn vào giờ làm việc, gắn với backlog thật, có review công khai |
| **Phạm vi quá rộng** | Ôm 8 chủ đề, không cái nào đủ sâu để đổi hành vi | Giới hạn 3 chủ đề trong 3 tháng, mỗi chủ đề 4 buổi |
| **Leader không đủ tải** | Người dạy/review chính là Leader, dễ quá tải và bỏ giữa chừng | Luân phiên người dẫn, chuẩn bị tài liệu dùng lại được, giới hạn 2h/tuần |

---

### 4. Điều đa số hiểu sai

- **"Học nhiều framework = nâng cấp năng lực."**
  Framework thay đổi, tư duy trade-off thì không. Dạy *tại sao chọn*, không phải *cách gõ*.

- **"Test coverage cao = chất lượng cao."**
  Coverage đo dòng code chạy qua, không đo hành vi được bảo vệ. Team có thể đạt 90% mà vẫn để lọt bug logic.

- **"System design chỉ dành cho senior."**
  Dev cơ bản ra quyết định thiết kế mỗi ngày (đặt tên bảng, chọn kiểu dữ liệu, chia hàm). Dạy muộn nghĩa là để họ sai nhiều năm trước khi được sửa.

- **"Leader nâng cao = học kiến trúc phức tạp hơn."**
  Nâng cao thật sự là: đánh giá trade-off dưới ràng buộc, viết ADR, chạy design review, biết khi nào *không* làm.

---

### 5. So sánh phương án

| Phương án | Chi phí | Tốc độ | Rủi ro | Công sức triển khai | Độ phù hợp |
|---|---|---|---|---|---|
| **A. Book/course club** (đọc chung + thảo luận tuần) | Rất thấp | Chậm ra kết quả | Dễ chết yểu, không ra artifact | Thấp | Team tự giác cao |
| **B. Workshop nội bộ + bài tập trên codebase thật** | Thấp–trung (thời gian Leader) | Trung bình, 4–6 tuần thấy chuyển biến | Phụ thuộc Leader | Trung bình | **Phù hợp nhất** |
| **C. Thuê trainer ngoài** | Cao | Nhanh, tập trung | Nội dung generic, không dính codebase | Thấp | Khi cần chuẩn hóa nhanh hoặc Leader quá tải |
| **D. Design review định kỳ, không có "lớp học"** | Rất thấp | Chậm nhưng bền | Dev cơ bản có thể bị bỏ lại | Thấp | Team đã có nền tảng tương đối đều |

**Gợi ý:** B làm chính, D làm cơ chế duy trì sau khi kết thúc 3 tháng.

---

### 6. Khoảng trống thông tin & câu hỏi phản biện

#### Thông tin còn thiếu

- Stack công nghệ cụ thể (frontend framework, backend, DB, hạ tầng)
- Quy mô team (bao nhiêu Dev, bao nhiêu Leader)
- Vấn đề đau nhất hiện tại: bug production? tốc độ ship chậm? code khó bảo trì?
- Ngân sách và quỹ thời gian được phép dùng trong giờ làm
- Team có đang có test suite nào chưa, coverage bao nhiêu

#### Câu hỏi một manager hoài nghi sẽ hỏi

1. Đo bằng gì? Sau 3 tháng, chỉ số nào chứng minh chương trình có tác dụng?
2. Chi phí cơ hội là bao nhiêu — 2h/tuần × số người × 12 tuần bằng bao nhiêu story point bị hoãn?
3. Nếu Leader nghỉ hoặc chuyển team thì chương trình còn chạy được không?
4. Tại sao không đơn giản là siết code review chặt hơn, rẻ hơn nhiều?
5. Nội dung này 6 tháng nữa có còn đúng không, hay lại phải làm lại?

---

### 7. Kết luận

> **Tôi sẽ chọn phương án B** — workshop nội bộ gắn với codebase thật, 3 chủ đề trong 3 tháng, hai tầng độ sâu — **bởi vì** nó là phương án duy nhất vừa rẻ, vừa tạo ra artifact kiểm chứng được, vừa dùng chính vấn đề thật của team làm giáo trình, nên khả năng đổi hành vi cao hơn hẳn book club hay trainer ngoài.

> **Điều duy nhất khiến tôi đổi ý là:** nếu Leader không có đủ 2–3h/tuần ổn định trong 3 tháng — khi đó phương án C (trainer ngoài cho phần nền tảng) + D (design review duy trì) sẽ thực tế hơn.

---
---

## PHẦN II — BỘ CÂU HỎI TỰ VẤN

Sắp theo thứ tự nên trả lời, vì câu sau phụ thuộc câu trước.

### Tầng 1 — Chẩn đoán (trả lời trước tiên)

Đừng bắt đầu bằng "nên dạy gì". Bắt đầu bằng "đang đau ở đâu".

- [ ] **1. Ba tháng qua, team mất nhiều thời gian nhất vào việc gì?**
  Fix bug production? Sửa lại code người khác? Chờ review? Deploy hỏng?

- [ ] **2. Bug lọt ra production thường thuộc loại nào?**
  Logic sai, tích hợp sai, edge case, hay do thiếu hiểu domain? Loại bug quyết định nên dạy testing kiểu gì.

- [ ] **3. Có việc gì team *né* làm vì code khó động vào không?**
  Đó là chỗ nợ kỹ thuật cần dạy refactor/design.

- [ ] **4. Nếu tuần sau một Dev nghỉ, phần nào của hệ thống không ai dám chạm?**
  Bus factor lộ ra khoảng trống kiến thức thật.

- [ ] **5. Khoảng cách giữa người giỏi nhất và yếu nhất trong team là bao nhiêu?**
  Xa quá thì không thể dạy chung một lớp.

### Tầng 2 — Ràng buộc thật (đừng tự lừa mình ở đây)

- [ ] **6. Thực tế được bao nhiêu giờ/tuần trong giờ làm?**
  Không phải "lý tưởng", mà là con số sếp sẽ ký duyệt.

- [ ] **7. Ai sẽ đứng lớp, và người đó còn dư bao nhiêu năng lượng?**
  Nếu chính bạn — bạn đang gánh bao nhiêu việc khác?

- [ ] **8. Nếu chương trình này làm chậm delivery 10% trong quý, ai sẽ chịu trách nhiệm giải thích?**

- [ ] **9. Team có thật sự muốn học, hay đây là mong muốn của riêng tôi?**
  Hỏi thẳng 2–3 người, đừng đoán.

### Tầng 3 — Định nghĩa thành công

- [ ] **10. Sau 3 tháng, tôi nhìn vào đâu để biết nó có tác dụng?**
  Số bug giảm? PR ít vòng review hơn? Dev tự tin nhận task khó hơn? Phải chọn được 1–2 chỉ số cụ thể.

- [ ] **11. Hành vi nào tôi muốn thấy thay đổi?**
  Ví dụ: "Dev viết test trước khi mở PR" cụ thể hơn nhiều so với "Dev hiểu về testing".

- [ ] **12. Nếu chỉ đạt được một thứ duy nhất, tôi muốn đó là gì?**
  Câu này ép bạn xếp hạng ưu tiên.

### Tầng 4 — Kiểm tra ngược (phản biện chính mình)

- [ ] **13. Có cách nào rẻ hơn đạt cùng kết quả không?**
  Siết code review, pair programming, viết checklist, thêm CI gate — nhiều khi hiệu quả hơn "lớp học".

- [ ] **14. Vấn đề này là do thiếu kiến thức, hay do thiếu quy trình / thiếu thời gian / thiếu công cụ?**
  Đào tạo không chữa được vấn đề quy trình.

- [ ] **15. Nếu chương trình dừng sau tháng thứ hai, phần nào còn sót lại?**
  Thiết kế sao cho mỗi tháng đã tự có giá trị độc lập.

- [ ] **16. Tôi có đang chọn chủ đề vì nó thú vị với tôi, hay vì team cần?**

---

### Cách dùng

Trả lời câu **1, 2, 6, 10** trước — bốn câu này quyết định phần lớn. Có câu trả lời cho chúng thì mới chuyển được khung tổng quát này thành lộ trình cụ thể theo tuần.

---

## Ghi chú về độ tin cậy

| Loại nội dung | Cách nhận biết trong tài liệu |
|---|---|
| **Sự kiện / thực tiễn ngành** | Nêu rõ nguồn hoặc bối cảnh |
| **Ý kiến** | Đánh dấu *(Ý kiến)* |
| **Giả định** | Đánh dấu *(Giả định — cần kiểm chứng)* |

Brief này dựa trên mô tả ngắn, chưa có stack công nghệ, quy mô team và vấn đề đau nhất. Các khuyến nghị nên được đọc như khung tư duy, không phải kế hoạch triển khai đã kiểm chứng.
