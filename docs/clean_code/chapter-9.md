# Clean Code – Chương 9: Unit Tests

## 1. Mục tiêu buổi thảo luận

Sau buổi thảo luận, nhóm nên thống nhất được:

- Vì sao **unit test** là một phần của chất lượng mã nguồn chứ không phải “phần phụ”.
- Thế nào là một **bài test sạch, dễ đọc, dễ bảo trì**.
- Cách áp dụng các nguyên tắc của chương 9 vào dự án thực tế của team.
- Những vấn đề hiện tại của test trong dự án và hướng cải thiện.

---

## 2. Nội dung cốt lõi của chương

## 2.1. Ba định luật của TDD

Tác giả nhấn mạnh rằng unit test nên đi **trước** mã nguồn sản xuất theo 3 định luật:

1. **Không viết mã nguồn sản xuất** cho đến khi đã có một unit test thất bại.
2. **Không viết nhiều test hơn mức đủ để thất bại**.
3. **Không viết nhiều mã nguồn sản xuất hơn mức đủ để test hiện tại pass**.

### Ý nghĩa thảo luận

- TDD giúp lập trình viên đi từng bước nhỏ, rõ ràng.
- Test trở thành công cụ định hình thiết kế code.
- Việc viết test trước giúp code dễ test hơn, ít phụ thuộc hơn.

### Câu hỏi thảo luận

1. Team hiện tại có đang viết test trước khi viết code không?
2. Nếu không áp dụng TDD đầy đủ, chúng ta có thể áp dụng ở mức nào?
3. Trong dự án thực tế, phần nào phù hợp với TDD nhất? Phần nào khó áp dụng?

---

## 2.2. Giữ cho bài kiểm thử sạch sẽ

Theo tác giả, **mã kiểm thử quan trọng ngang với mã nguồn sản xuất**.

### Nếu test bẩn thì điều gì xảy ra?

- Test khó đọc, khó sửa.
- Khi production code thay đổi, test vỡ hàng loạt nhưng khó fix.
- Team bắt đầu thấy test là gánh nặng.
- Cuối cùng có thể bỏ luôn test.
- Khi không còn test đáng tin cậy, lập trình viên sẽ **sợ sửa code**, khiến production code xuống cấp dần.

### Giá trị thật của unit test

Unit test sạch giúp:

- Giảm nỗi sợ khi refactor.
- Tăng khả năng bảo trì.
- Tăng độ tin cậy khi thêm tính năng mới.
- Giúp phát hiện lỗi sớm.

### Câu hỏi thảo luận

1. Trong dự án của team, test đang là “lưới an toàn” hay đang là “gánh nặng”?
2. Có tình huống nào team ngại sửa code vì sợ vỡ logic mà không có test bảo vệ không?
3. Theo mọi người, nguyên nhân khiến test trở nên khó bảo trì là gì?

---

## 2.3. Tiêu chuẩn của một bài kiểm thử sạch

### a. Readability là quan trọng nhất

Một bài test tốt phải **dễ đọc**, để người đọc nhìn vào là hiểu:

- đang kiểm tra hành vi gì,
- dữ liệu đầu vào là gì,
- kết quả mong đợi là gì.

Test khó đọc thường dẫn đến:

- hiểu sai mục đích test,
- sửa test sai,
- ngại bổ sung test mới.

### b. Mô hình Build – Operate – Check

Mỗi test nên thể hiện rõ 3 bước:

1. **Build**: Chuẩn bị dữ liệu, mock, object.
2. **Operate**: Gọi hàm hoặc thực hiện hành vi cần test.
3. **Check**: Kiểm tra kết quả.

### c. Tạo DSL cho test

Thay vì lặp đi lặp lại các setup phức tạp, có thể tạo các helper/hàm tiện ích để test đọc giống ngôn ngữ nghiệp vụ hơn.

Ví dụ tư duy:

- Thay vì tự dựng object rất dài trong mỗi test,
- có thể tạo helper như `make_valid_user()`, `make_expired_order()`, `login_as_admin()`.

### d. Dual Standard

Code test vẫn phải sạch, nhưng không cần quá tối ưu hiệu năng như production code.

Điều quan trọng hơn là:

- dễ đọc,
- dễ hiểu,
- dễ chỉnh sửa.

### Câu hỏi thảo luận

1. Khi review test, team ưu tiên điều gì nhất: độ ngắn, độ đẹp, hay độ dễ hiểu?
2. Các test hiện tại của team có tách rõ Build – Operate – Check không?
3. Team có nên tạo helper/fixture/factory để giảm lặp trong test không?

---

## 2.4. Các quy tắc tổ chức bài kiểm thử

## Mỗi bài test một khái niệm

Tác giả có nhắc tới ý tưởng **mỗi test một assert**, nhưng điều quan trọng hơn là:

> Mỗi bài test chỉ nên kiểm tra **một khái niệm**.

Điều này giúp test:

- dễ hiểu,
- dễ đặt tên,
- dễ xác định nguyên nhân khi fail.

### Câu hỏi thảo luận

1. Một test có nhiều assert có luôn là xấu không?
2. Khi nào nhiều assert vẫn chấp nhận được?
3. Làm sao phân biệt “nhiều assert cho một khái niệm” và “gom nhiều khái niệm vào một test”?

---

## 2.5. Nguyên tắc F.I.R.S.T

## F — Fast

Test phải chạy nhanh để developer chạy thường xuyên.

**Thảo luận:**

- Bộ test hiện tại có chậm không?
- Điều gì đang làm test chậm: DB, network, file, sleep, setup nặng?

## I — Independent

Các test phải độc lập, không phụ thuộc thứ tự chạy hay kết quả của nhau.

**Thảo luận:**

- Team có test nào phụ thuộc vào dữ liệu do test trước tạo ra không?
- Có dùng shared state làm test dễ fail ngẫu nhiên không?

## R — Repeatable

Test phải chạy được ở mọi môi trường và cho cùng kết quả.

**Thảo luận:**

- Test có phụ thuộc máy cá nhân, timezone, file local, internet, môi trường ngoài không?
- Có test nào “máy tôi chạy được nhưng CI fail” không?

## S — Self-Validating

Test phải tự xác định pass/fail, không yêu cầu người chạy đọc log rồi tự kết luận.

**Thảo luận:**

- Team có còn kiểu test in log ra để kiểm tra thủ công không?
- Assertion hiện tại có rõ ràng không?

## T — Timely

Test nên được viết đúng thời điểm, tốt nhất là **ngay trước** hoặc **rất gần** lúc viết production code.

**Thảo luận:**

- Team hay viết test lúc nào: trước, trong, hay sau khi code xong?
- Viết test quá muộn gây ra khó khăn gì?

---

## 3. Tình huống liên hệ với dự án thực tế

Có thể dùng các tình huống dưới đây để nhóm thảo luận:

### Tình huống 1: Sợ refactor

Một module đã chạy ổn định lâu rồi nhưng code rất khó đọc. Team muốn refactor nhưng không ai dám đụng vào vì sợ gây lỗi.

**Câu hỏi:**

- Gốc rễ vấn đề có phải là thiếu test không?
- Nếu bắt đầu bổ sung test, nên viết test ở mức nào trước?
- Nên ưu tiên test hành vi hiện tại hay refactor ngay?

### Tình huống 2: Test rất nhiều nhưng ít giá trị

Một module có nhiều test nhưng hễ đổi tên method, đổi cấu trúc class, hoặc đổi implementation nhỏ là test vỡ hàng loạt.

**Câu hỏi:**

- Những test này đang kiểm tra hành vi hay đang bám chặt vào implementation?
- Làm thế nào để test bền hơn khi refactor?

### Tình huống 3: Test khó đọc

Một test có setup rất dài, nhiều mock, nhiều biến trung gian, đọc xong vẫn không hiểu đang test điều gì.

**Câu hỏi:**

- Nên cải thiện bằng cách nào?
- Tách helper, dùng fixture, đổi tên test, hay chia nhỏ production code?

### Tình huống 4: Test fail ngẫu nhiên

Có bài test lúc pass lúc fail tùy thời điểm chạy hoặc tùy môi trường.

**Câu hỏi:**

- Có vi phạm nguyên tắc FIRST nào?
- Làm sao loại bỏ yếu tố thời gian, random, external dependency?

---

## 4. Gợi ý câu hỏi thảo luận nhóm

### Nhóm câu hỏi hiểu nội dung

1. Vì sao tác giả cho rằng mã test bẩn sẽ kéo theo production code bẩn?
2. Vì sao readability lại là yếu tố quan trọng nhất của test?
3. “Mỗi test một khái niệm” khác gì với “mỗi test một assert”?
4. FIRST là gì và nguyên tắc nào team mình đang vi phạm nhiều nhất?

### Nhóm câu hỏi liên hệ thực tế

1. Trong dự án hiện tại, vấn đề lớn nhất của test là gì?
2. Team có đang viết quá ít test, hay có test nhưng chất lượng chưa tốt?
3. Có phần nào trong hệ thống nên ưu tiên bổ sung unit test trước?
4. Khi code review, team có review cả chất lượng test không?

### Nhóm câu hỏi định hướng cải tiến

1. Team có nên thống nhất template viết test theo Build – Operate – Check không?
2. Có nên tạo guideline đặt tên test chung cho team không?
3. Có nên tách unit test và integration test rõ hơn không?
4. Mỗi task mới có nên yêu cầu bổ sung test tương ứng không?

---

## 5. Kết luận rút ra từ chương 9

Những điểm quan trọng cần thống nhất sau buổi thảo luận:

- **Test không phải phần phụ**, mà là nền tảng để duy trì khả năng thay đổi của hệ thống.
- **Test bẩn sẽ làm team mất niềm tin vào test**.
- Một bài test tốt phải **dễ đọc, tập trung, độc lập, chạy nhanh và tự xác thực**.
- Mục tiêu lớn nhất của test là **giúp team thay đổi code mà không sợ hãi**.

---

## 6. Đề xuất action cho team sau buổi thảo luận

1. Thống nhất tiêu chí tối thiểu cho một unit test sạch.
2. Review lại các test khó đọc hoặc hay fail ngẫu nhiên.
3. Áp dụng nguyên tắc Build – Operate – Check khi viết test mới.
4. Ưu tiên bổ sung test cho những vùng code team ngại sửa nhất.
5. Đưa chất lượng test vào checklist code review.

---

## 7. Gợi ý checklist review test

Có thể dùng nhanh khi review PR:

- [ ] Tên test có nói rõ hành vi cần kiểm tra không?
- [ ] Test có dễ đọc không?
- [ ] Test có tách rõ Build – Operate – Check không?
- [ ] Test có đang kiểm tra đúng một khái niệm không?
- [ ] Test có phụ thuộc môi trường, thời gian, thứ tự chạy, network, DB thật không?
- [ ] Assertion có rõ ràng và tự xác thực không?
- [ ] Test có quá bám vào implementation không?
- [ ] Test mới có thực sự tăng độ tin cậy cho code không?

---

## 8. Một câu chốt để mở hoặc kết thúc buổi thảo luận

> Nếu production code là tài sản của dự án, thì test chính là hệ thống bảo vệ tài sản đó. Khi test mục nát, khả năng thay đổi an toàn của hệ thống cũng mất đi.
