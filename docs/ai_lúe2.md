# [TÊN DỰ ÁN] - Báo cáo Kế hoạch Triển khai AI (Thử nghiệm 3 tháng)

> **Hướng dẫn sử dụng mẫu này**
> 
> Mẫu này được thiết kế để nhóm cùng điền và sau đó trình lên cấp trên. Mỗi mục có ba lớp.
> Lớp một là tiêu đề mục cần giữ nguyên. Lớp hai là phần hướng dẫn đặt trong block trích dẫn, gồm câu hỏi gợi ý và độ dài khuyến nghị, cần xóa sau khi điền xong. Lớp ba là ví dụ ngắn đặt trong block code, cần xóa sau khi điền xong.
> 
> Mỗi mục đều có ghi rõ vai trò chịu trách nhiệm điền và vai trò review. Sau khi điền xong, người phụ trách dự án tổng hợp và rà soát toàn bộ trước khi trình.
> 
> **Vai trò trong nhóm** (điền tên thực vào đây trước khi phân công)
> 
> - Người phụ trách dự án (PM): ________________
> - Lead Developer (Lead): ________________
> - Senior Developer (Senior): ________________
> - Developer (Dev): ________________
> - Security Lead (SecLead): ________________ (có thể kiêm nhiệm)
> 
> **Quy ước phân công**: Mỗi mục ghi `[Điền: VAI_TRÒ] [Review: VAI_TRÒ]` ngay dưới tiêu đề. Sau khi điền xong và đã review, xóa dòng này.
> 
> **Deadline tổng thể**: Hoàn tất bản nháp trong ____ ngày kể từ khi phân công.

-----

## Tóm tắt Điều hành

[Điền: PM] [Review: Lead]

> **Hướng dẫn**: Mục này là phần quan trọng nhất với cấp trên, có thể là phần duy nhất họ đọc kỹ. Cần trả lời bốn câu hỏi sau trong 1 đoạn ngắn không quá nửa trang.
> 
> 1. Dự án này làm gì và kéo dài bao lâu?
> 1. Ba rủi ro lớn nhất là gì và biện pháp kiểm soát chính ra sao?
> 1. Chi phí và nguồn lực cần cấp trên phê duyệt?
> 1. Tiêu chí nào để xác định dự án thành công hay thất bại?
> 
> Viết phần này sau cùng, khi các mục khác đã điền xong.

```
Ví dụ:
Nhóm phát triển đề xuất triển khai thử nghiệm AI (Cline + VS Code) vào workflow phát triển phần mềm trong 3 tháng, với mục tiêu đánh giá tác động đến tốc độ và chất lượng công việc. Ba rủi ro chính được xác định là rò rỉ thông tin nhạy cảm qua AI, suy giảm chất lượng code do phụ thuộc AI, và đánh giá sai lỗ hổng bảo mật khi điều tra CVE. Các biện pháp kiểm soát tương ứng bao gồm danh sách module cấm truy cập AI, quy định mọi code AI phải qua review, và yêu cầu hai người độc lập xác nhận với CVE có CVSS cao. Nguồn lực cần thiết là chi phí license công cụ AI khoảng [X] USD/tháng cho nhóm và thời gian setup ban đầu khoảng 5 ngày-người. Dự án được xem là thành công nếu cải thiện rõ rệt ở ít nhất một trục đo lường mà không gây suy giảm ở trục còn lại, đo bằng số liệu so sánh với baseline 4 tuần trước thử nghiệm.
```

-----

## 1. Rủi ro và Biện pháp Kiểm soát

[Điền: Lead + SecLead] [Review: PM]

> **Hướng dẫn**: Đây là mục quan trọng thứ hai và được đặt sớm trong tài liệu. Mỗi rủi ro cần ba thành phần. Mô tả rủi ro cụ thể không chung chung. Mức độ ảnh hưởng và xác suất xảy ra. Biện pháp kiểm soát kèm người chịu trách nhiệm thực hiện.
> Liệt kê từ 4 đến 6 rủi ro chính, mỗi rủi ro khoảng 4-6 câu. Tổng độ dài mục này khoảng 1.5 trang.

### 1.1. Rủi ro [Tên rủi ro 1]

> **Câu hỏi gợi ý**: Rủi ro này phát sinh khi nào? Hậu quả tệ nhất là gì? Ai chịu trách nhiệm theo dõi? Khi nào xem là đã kiểm soát thành công?

```
Ví dụ - Rủi ro rò rỉ thông tin nhạy cảm qua AI:
Khi AI xử lý code, có khả năng credential, API key, hoặc logic nghiệp vụ bí mật bị gửi đến server bên thứ ba. Mức độ ảnh hưởng cao vì có thể vi phạm hợp đồng với khách hàng. Xác suất trung bình nếu không có biện pháp kiểm soát. Biện pháp gồm danh sách module cấm AI truy cập được liệt kê trong file .clinerules, quy ước không paste credential vào prompt, và kiểm tra ngẫu nhiên log Cline hàng tuần. SecLead chịu trách nhiệm chính, báo cáo trạng thái mỗi 2 tuần. Rủi ro xem là đã kiểm soát khi qua 4 tuần không phát hiện vi phạm.
```

### 1.2. Rủi ro [Tên rủi ro 2]

### 1.3. Rủi ro [Tên rủi ro 3]

### 1.4. Rủi ro [Tên rủi ro 4]

-----

## 2. Bối cảnh và Lý do thực hiện

[Điền: PM] [Review: Lead]

> **Hướng dẫn**: Giải thích tại sao nhóm cần làm dự án này NGAY BÂY GIỜ, không phải sau hoặc trước. Tránh viết chung chung kiểu “AI đang phát triển nhanh”. Cần nêu được vấn đề cụ thể của nhóm mà dự án muốn giải quyết hoặc cơ hội cụ thể mà nhóm muốn nắm bắt. Độ dài khoảng nửa trang.

```
Ví dụ:
Nhóm đang đối mặt với áp lực tiến độ tăng dần do số lượng feature backlog tăng [X]% so với cùng kỳ năm ngoái, trong khi quy mô nhân sự giữ nguyên. Đồng thời, thời gian điều tra CVE hàng tháng đang chiếm khoảng [Y] giờ-người, ảnh hưởng đến tiến độ phát triển feature. Các công cụ AI hỗ trợ lập trình đã đủ trưởng thành để xem xét nghiêm túc như một giải pháp. Tuy nhiên nhóm cần đánh giá kỹ trước khi cam kết triển khai chính thức vì có những đánh đổi về bảo mật và chất lượng cần được hiểu rõ.
```

-----

## 3. Mục tiêu và Tiêu chí Thành công

[Điền: PM] [Review: Lead]

### 3.1. Mục tiêu chính

> **Câu hỏi gợi ý**: Sau 3 tháng, nhóm muốn trả lời được câu hỏi cụ thể nào? Câu trả lời đó sẽ dẫn đến quyết định gì?
> Độ dài khoảng 1 đoạn ngắn.

### 3.2. Mục tiêu phụ

> **Câu hỏi gợi ý**: Ngoài mục tiêu chính, dự án còn tạo ra giá trị gì khác (ví dụ kinh nghiệm, tài liệu, prompt library)?
> Độ dài khoảng 1 đoạn ngắn.

### 3.3. Tiêu chí thành công cụ thể

> **Hướng dẫn**: Liệt kê các tiêu chí định lượng. Tránh tiêu chí mơ hồ kiểu “team hài lòng”. Mỗi tiêu chí cần có ngưỡng số cụ thể.

```
Ví dụ:
- Tốc độ hoàn thành task tăng tối thiểu 20% so với baseline
- Tỷ lệ bug trong code AI không cao hơn code thuần quá 10%
- Thời gian điều tra trung bình mỗi CVE giảm tối thiểu 30%
- Toàn bộ rủi ro ở mục 1 không xảy ra incident nghiêm trọng nào
```

-----

## 4. Phạm vi Dự án

[Điền: Lead] [Review: PM]

### 4.1. Trong phạm vi

> **Câu hỏi gợi ý**: Loại công việc nào, repo nào, thành viên nào tham gia thử nghiệm?

### 4.2. Ngoài phạm vi

> **Câu hỏi gợi ý**: Loại công việc nào, module nào KHÔNG tham gia thử nghiệm và tại sao? Phần này quan trọng để cấp trên hiểu giới hạn của thử nghiệm.

```
Ví dụ - Ngoài phạm vi:
Module xử lý thanh toán (payment-service) không được sử dụng AI do chứa logic xử lý thông tin tài chính nhạy cảm. Module xác thực (auth-service) chỉ cho phép AI đọc để hiểu ngữ cảnh, không cho phép AI sửa code. Quá trình release lên production không được sử dụng AI dù chỉ ở mức gợi ý.
```

-----

## 5. Tool và Cấu hình

[Điền: Lead + Senior] [Review: SecLead]

### 5.1. Công cụ chọn

> **Câu hỏi gợi ý**: Công cụ AI nào, phiên bản nào? Tại sao chọn công cụ này thay vì các giải pháp khác? Có cần license trả phí không?

### 5.2. Cấu hình kỹ thuật thống nhất

> **Hướng dẫn**: Liệt kê các thiết lập cần thống nhất trong toàn nhóm. Mỗi thành viên dùng cùng cấu hình để dữ liệu so sánh được.

```
Ví dụ:
- VS Code version: [X.Y.Z], Cline version: [A.B.C]
- Model AI chính: [tên model]
- Quyền tự động: chế độ "yêu cầu xác nhận" cho 4 tuần đầu, sau đó xem xét nâng lên
- File .env riêng cho mỗi thành viên, đã thêm vào .gitignore
```

### 5.3. Cấu hình ngữ cảnh dự án

> **Hướng dẫn**: Mô tả file `.clinerules` sẽ được xây dựng cho các repo tham gia. Ai phụ trách viết, khi nào hoàn tất.

### 5.4. Quy ước tổ chức

> **Hướng dẫn**: Liệt kê các quy ước về cách cả nhóm cùng làm việc với AI. Ví dụ quy ước gắn nhãn commit, danh sách “AI read-only”, cách báo cáo trạng thái.

-----

## 6. Cách Triển khai

[Điền: Lead] [Review: PM]

### 6.1. Quy trình bốn bước

> **Hướng dẫn**: Mô tả quy trình chuẩn áp dụng cho mọi nhiệm vụ trong dự án. Tham khảo tài liệu chi tiết của dự án để có quy trình đầy đủ. Phần này chỉ cần tóm tắt khung quy trình trong nửa trang.

### 6.2. Mức độ tự chủ của AI

> **Hướng dẫn**: Liệt kê các mức độ tự chủ sẽ được thử nghiệm và phương án mặc định cho từng loại task.

-----

## 7. Các Nhiệm vụ Triển khai

[Điền: Lead + các thành viên phụ trách từng nhiệm vụ] [Review: PM]

### 7.1. Nhiệm vụ - [Tên nhiệm vụ 1]

[Điền: ________________]

> **Câu hỏi gợi ý**: Nhiệm vụ này gồm những bước nào? AI hỗ trợ bước nào? Cần chuẩn bị gì cho AI? Tiêu chí đánh giá output là gì?
> Độ dài khoảng 1 trang cho mỗi nhiệm vụ.

```
Ví dụ - cấu trúc một nhiệm vụ:
Mô tả nhiệm vụ: ...
Phân rã các bước: ...
AI hỗ trợ ở bước nào và mức độ tự chủ: ...
Chuẩn bị cần thiết: ...
Tiêu chí đánh giá output: ...
Ví dụ workflow thực tế: ...
```

### 7.2. Nhiệm vụ - [Tên nhiệm vụ 2]

[Điền: ________________]

### 7.3. Nhiệm vụ - [Tên nhiệm vụ 3]

[Điền: ________________]

-----

## 8. Chỉ số Đo lường

[Điền: PM + Senior] [Review: Lead]

### 8.1. Baseline (Tuần 1)

> **Hướng dẫn**: Liệt kê các số liệu cần thu thập trong tuần 1 trước khi bắt đầu dùng AI. Nguồn dữ liệu cho từng số liệu là gì.

### 8.2. Chỉ số tốc độ

> **Hướng dẫn**: Mỗi chỉ số cần có tên, công thức tính, nguồn dữ liệu, tần suất đo, và người phụ trách thu thập.

```
Ví dụ:
- Cycle time PR: thời gian từ tạo PR đến merge, tính bằng giờ. Nguồn: GitHub API. Tần suất: tuần. Phụ trách: Senior.
```

### 8.3. Chỉ số chất lượng

### 8.4. Cách thu thập và báo cáo

> **Câu hỏi gợi ý**: Dữ liệu được tổng hợp như thế nào? Báo cáo định kỳ nào? Ai là người tổng hợp và phân tích?

-----

## 9. Cơ chế Đúc kết Kinh nghiệm

[Điền: Lead] [Review: PM]

> **Hướng dẫn**: Mô tả ba cơ chế chính. Prompt library dùng chung lưu ở đâu, ai duy trì. Log tình huống đáng chú ý theo template nào, lưu ở đâu. Retrospective định kỳ tần suất ra sao, ai chủ trì.
> Độ dài khoảng nửa trang.

-----

## 10. Timeline và Milestone

[Điền: PM] [Review: Lead]

> **Hướng dẫn**: Chia 12 tuần thành các giai đoạn chính, mỗi giai đoạn có mục tiêu và deliverable cụ thể. Trình bày dưới dạng bảng nếu được.

```
Ví dụ:
Tuần 1: Setup - hoàn tất .clinerules, baseline, đào tạo. Deliverable: file .clinerules merged, bảng baseline.
Tuần 2-4: Vận hành ban đầu...
Tuần 5-10: Vận hành ổn định...
Tuần 11: Tổng hợp số liệu...
Tuần 12: Báo cáo và quyết định...
```

-----

## 11. Nguồn lực và Chi phí

[Điền: PM] [Review: Lead]

### 11.1. Chi phí trực tiếp

> **Hướng dẫn**: Liệt kê các khoản phí cụ thể. License công cụ AI, chi phí API nếu dùng, các phần mềm phụ trợ. Đưa con số ước tính cho 3 tháng và quy ra hàng tháng.

### 11.2. Chi phí gián tiếp

> **Hướng dẫn**: Thời gian setup ban đầu, thời gian retrospective, thời gian đào tạo. Quy ra số ngày-người.

### 11.3. Đề xuất phê duyệt

> **Hướng dẫn**: Nêu rõ con số cần cấp trên phê duyệt và mục đích sử dụng.

-----

## 12. Vai trò và Trách nhiệm

[Điền: PM] [Review: tất cả]

> **Hướng dẫn**: Bảng RACI hoặc danh sách vai trò với trách nhiệm cụ thể. Ai làm gì, báo cáo cho ai, tần suất ra sao.

-----

## 13. Kế hoạch Kết thúc Dự án

[Điền: PM] [Review: Lead]

### 13.1. Tiêu chí ra quyết định

> **Câu hỏi gợi ý**: Sau 3 tháng, dựa vào tiêu chí nào để quyết định triển khai chính thức, điều chỉnh tiếp, hay dừng?

### 13.2. Các kịch bản và phương án tương ứng

> **Hướng dẫn**: Liệt kê 3 kịch bản chính (thành công rõ, kết quả lẫn lộn, thất bại) và phương án xử lý cho từng kịch bản.

-----

## Phụ lục

[Phần này điền dần trong quá trình triển khai]

- Phụ lục A: Bảng số liệu baseline chi tiết
- Phụ lục B: File `.clinerules` mẫu
- Phụ lục C: Template báo cáo CVE
- Phụ lục D: Prompt library hiện tại
- Phụ lục E: Biên bản các buổi retrospective
- Phụ lục F: Log các tình huống đáng chú ý

-----

## Checklist trước khi trình cấp trên

> **Hướng dẫn**: Sau khi nhóm điền xong, PM dùng checklist này để rà soát trước khi gửi báo cáo. Xóa toàn bộ phần này sau khi đã rà soát xong.

- [ ] Tất cả các mục đã được điền, không còn placeholder `[...]`
- [ ] Đã xóa toàn bộ các block hướng dẫn (`> **Hướng dẫn**`) và block ví dụ
- [ ] Tóm tắt điều hành (Mục đầu) đã được viết sau cùng và cô đọng
- [x] Số liệu cụ thể đã được điền vào các chỗ trống `[X]`, `[Y]`
- [ ] Phần Rủi ro có từ 4 đến 6 rủi ro cụ thể, không chung chung
- [ ] Tiêu chí thành công có ngưỡng định lượng rõ ràng
- [ ] Đã có chữ ký xác nhận của Lead và SecLead cho phần kỹ thuật và bảo mật
- [ ] Văn phong đã được rà soát để đảm bảo nhất quán giữa các phần do nhiều người viết
- [ ] Độ dài tổng thể trong khoảng 8-12 trang