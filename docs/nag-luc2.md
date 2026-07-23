Chương trình nâng cao năng lực Developer & Technical Leader

1. Mục tiêu chương trình

Chương trình hướng đến ba kết quả chính:

1. Nâng cao chất lượng thiết kế, phát triển và kiểm thử phần mềm.
2. Giúp developer hình thành tư duy chủ động, có khả năng phân tích và ra quyết định kỹ thuật.
3. Giúp leader nâng cao năng lực quản lý kỹ thuật, giao việc, kiểm soát rủi ro và phát triển thành viên.

Không nên đánh giá chương trình chỉ bằng số buổi học. Mỗi đề tài phải tạo ra ít nhất một đầu ra có thể áp dụng vào dự án như checklist, guideline, template, công cụ hoặc cải tiến quy trình.

⸻

2. Cấu trúc chương trình

Chia chương trình thành ba nhóm năng lực.

Nhóm A — Năng lực Developer

A1. Software Testing Mindset

Tài liệu gợi ý: The Art of Software Testing.

Nội dung chính:

* Tư duy kiểm thử: kiểm thử nhằm tìm lỗi, không phải chứng minh hệ thống không có lỗi.
* Phân biệt unit, integration, API, system và acceptance testing.
* Thiết kế test case bằng:
    * Equivalence partitioning.
    * Boundary value analysis.
    * Decision table.
    * State transition.
* Phân tích rủi ro để ưu tiên kiểm thử.
* Những lỗi phổ biến khi viết automation test.

Đầu ra:

* Test strategy mẫu cho dự án.
* Checklist review test case.
* Danh sách test case cho một chức năng thực tế.
* Đề xuất tỷ lệ unit, integration và end-to-end test phù hợp với công ty.

Lưu ý: Không nên triển khai theo hình thức chỉ đọc và tóm tắt toàn bộ sách. Nên chọn các chương có thể áp dụng trực tiếp vào dự án.

⸻

A2. Thiết kế ứng dụng theo 12-Factor App

Nội dung chính:

* Quản lý source code và dependency.
* Tách configuration khỏi source code.
* Sử dụng backing services.
* Phân tách build, release và run.
* Thiết kế stateless process.
* Logging, concurrency và disposable process.
* Sự khác nhau giữa nguyên tắc 12-Factor và cách triển khai thực tế bằng Docker, Kubernetes hoặc cloud.

Đầu ra:

* Checklist đánh giá mức độ tuân thủ 12-Factor.
* Đánh giá một dự án hiện tại.
* Danh sách điểm chưa phù hợp và kế hoạch cải thiện.
* Template cấu hình môi trường development, staging và production.

Lưu ý: 12-Factor phù hợp với web service và cloud-native application, nhưng không phải nguyên tắc nào cũng nên áp dụng máy móc cho mọi hệ thống.

⸻

A3. Clean Code và Code Review

Nội dung chính:

* Cách đặt tên và tổ chức code.
* Function, module và class có trách nhiệm rõ ràng.
* Xử lý exception và logging.
* Phát hiện code smell.
* Phân biệt vấn đề bắt buộc sửa và ý kiến mang tính sở thích.
* Cách viết comment code review rõ ràng, tôn trọng và có căn cứ.

Đầu ra:

* Coding convention cho từng dự án.
* Pull request checklist.
* Bộ ví dụ “before–after” từ code thực tế.
* Quy ước mức độ comment: blocker, major, minor và suggestion.

⸻

A4. System Design căn bản

Nội dung chính:

* Xác định functional và non-functional requirements.
* Thiết kế API, database và luồng dữ liệu.
* Caching, queue, retry và idempotency.
* Scalability, availability và consistency.
* Phân tích bottleneck.
* Các trade-off khi lựa chọn giải pháp.

Đầu ra:

* System design document mẫu.
* Sơ đồ kiến trúc của một hệ thống nội bộ.
* Architecture Decision Record.
* Buổi design review có phản biện giữa các thành viên.

⸻

A5. Observability và Production Readiness

Nội dung chính:

* Logging, metrics và tracing.
* Health check và readiness check.
* Theo dõi latency, error rate và resource usage.
* Alert và incident response.
* Memory leak, connection leak và performance bottleneck.
* Cách chuẩn bị hệ thống trước khi release.

Đầu ra:

* Production readiness checklist.
* Dashboard mẫu.
* Runbook xử lý sự cố.
* Danh sách metric tối thiểu của mỗi service.

⸻

Nhóm B — Năng lực Technical Leader

B1. Phân rã công việc và lập kế hoạch kỹ thuật

Nội dung chính:

* Chuyển yêu cầu lớn thành milestone, workstream và task.
* Xác định dependency.
* Ước lượng bằng khoảng thay vì một con số tuyệt đối.
* Quản lý assumption, risk và buffer.
* Definition of Ready và Definition of Done.
* Theo dõi tiến độ dựa trên kết quả thay vì phần trăm cảm tính.

Đầu ra:

* Template task breakdown.
* Risk register.
* Checklist trước khi bắt đầu sprint.
* Quy trình xử lý task có nguy cơ trễ.

⸻

B2. Giao việc và phát triển thành viên

Nội dung chính:

* Giao việc dựa trên năng lực và mục tiêu phát triển.
* Làm rõ expected outcome, phạm vi và deadline.
* Phân biệt delegation và micromanagement.
* Cách kiểm tra tiến độ mà không gây áp lực không cần thiết.
* Feedback theo tình huống cụ thể.
* Xây dựng kế hoạch phát triển cá nhân.

Đầu ra:

* Delegation brief mẫu.
* Template one-on-one.
* Individual Development Plan.
* Skill matrix của đội nhóm.

⸻

B3. Ra quyết định kỹ thuật

Nội dung chính:

* Xác định vấn đề cần giải quyết.
* So sánh giải pháp dựa trên cost, risk, complexity và maintainability.
* Phân biệt reversible và irreversible decisions.
* Tránh lựa chọn công nghệ chỉ vì đang phổ biến.
* Ghi nhận và truyền đạt quyết định.

Đầu ra:

* Architecture Decision Record.
* Decision matrix.
* Danh sách tiêu chí đánh giá thư viện hoặc công nghệ mới.
* Một case study từ quyết định thực tế của công ty.

⸻

B4. Quản lý chất lượng và rủi ro dự án

Nội dung chính:

* Thiết lập quality gate.
* Kiểm soát technical debt.
* Phân loại và ưu tiên bug.
* Release readiness.
* Root cause analysis.
* Blameless retrospective.

Đầu ra:

* Quality gate cho CI/CD.
* Bug severity matrix.
* Release checklist.
* Template phân tích nguyên nhân gốc.

⸻

B5. Giao tiếp kỹ thuật với stakeholder

Nội dung chính:

* Giải thích vấn đề kỹ thuật bằng ngôn ngữ kinh doanh.
* Báo cáo tiến độ, rủi ro và tác động.
* Không che giấu vấn đề nhưng cũng không báo cáo gây hoang mang.
* Đưa ra phương án thay vì chỉ nêu khó khăn.
* Quản lý kỳ vọng về phạm vi và deadline.

Đầu ra:

* Mẫu báo cáo tuần.
* Mẫu escalation.
* Mẫu đề xuất thay đổi phạm vi.
* Bài tập trình bày một vấn đề kỹ thuật trong năm phút.

⸻

Nhóm C — Năng lực chung

C1. Problem Solving và Root Cause Analysis

* 5 Whys.
* Fishbone diagram.
* Phân biệt triệu chứng và nguyên nhân.
* Xây dựng giả thuyết.
* Thu thập dữ liệu trước khi kết luận.

C2. Security Mindset

* OWASP Top 10.
* Quản lý secret.
* Authentication và authorization.
* Dependency vulnerability.
* Secure coding checklist.

C3. AI-assisted Software Development

* Sử dụng AI để đọc code, viết test và tạo tài liệu.
* Kiểm chứng kết quả AI.
* Bảo vệ dữ liệu nội bộ.
* Những trường hợp không nên phụ thuộc vào AI.
* Đo lường hiệu quả sử dụng AI.

⸻

3. Thứ tự ưu tiên đề tài

Không nên triển khai quá nhiều chủ đề cùng lúc. Giai đoạn đầu nên chọn bốn đề tài:

Ưu tiên	Đề tài	Đối tượng chính	Lý do
1	Software Testing Mindset	Developer, QA, Leader	Tác động trực tiếp đến chất lượng sản phẩm
2	12-Factor App	Backend, DevOps, Leader	Phù hợp với hệ thống service, Docker và cloud
3	Code Review và Clean Code	Toàn bộ developer	Có thể áp dụng ngay trong công việc hằng ngày
4	Task Breakdown và Risk Management	Leader, senior developer	Giảm task trễ và vấn đề phát hiện quá muộn

System Design và Observability nên triển khai trong giai đoạn tiếp theo, sau khi đội nhóm đã có nền tảng chung.

⸻

4. Kế hoạch pilot 12 tuần

Giai đoạn 1 — Chuẩn bị: Tuần 1–2

Hoạt động:

* Khảo sát vấn đề hiện tại của các dự án.
* Thu thập dữ liệu về bug, task trễ, test coverage và incident.
* Đánh giá nhanh năng lực thành viên.
* Chọn một hoặc hai dự án pilot.
* Chỉ định program owner và topic owner.

Đầu ra:

* Baseline trước chương trình.
* Danh sách vấn đề ưu tiên.
* Kế hoạch và lịch sinh hoạt.
* Danh sách người phụ trách từng chủ đề.

⸻

Giai đoạn 2 — Software Testing: Tuần 3–4

Tuần 3:

* Workshop tư duy kiểm thử.
* Hướng dẫn các kỹ thuật thiết kế test.
* Phân tích một chức năng thực tế.

Tuần 4:

* Thành viên xây dựng test strategy và test case.
* Review chéo giữa các nhóm.
* Chọn các test case phù hợp để automation.

Đầu ra:

* Test strategy.
* Test case checklist.
* Một cải tiến test được đưa vào dự án.

⸻

Giai đoạn 3 — 12-Factor App: Tuần 5–6

Tuần 5:

* Giới thiệu các nguyên tắc.
* Phân tích ví dụ đúng và sai.
* Đánh giá một service hiện tại.

Tuần 6:

* Xác định gap.
* Chọn từ một đến ba cải tiến khả thi.
* Triển khai thử nghiệm.

Đầu ra:

* 12-Factor assessment.
* Danh sách cải tiến.
* Pull request hoặc technical proposal.

⸻

Giai đoạn 4 — Clean Code và Code Review: Tuần 7–8

Tuần 7:

* Thống nhất code review principles.
* Phân tích code smell trong code thực tế.
* Xây dựng checklist.

Tuần 8:

* Áp dụng checklist vào pull request.
* Thu thập phản hồi.
* Điều chỉnh coding convention.

Đầu ra:

* Pull request checklist.
* Coding convention phiên bản đầu tiên.
* Bộ ví dụ code thực tế.

⸻

Giai đoạn 5 — Leadership: Tuần 9–10

Tuần 9:

* Workshop task breakdown, estimation và risk management.
* Phân tích một task từng bị trễ.

Tuần 10:

* Leader áp dụng template mới vào sprint.
* Developer phản hồi về độ rõ ràng của task.
* Chuẩn hóa Definition of Ready và Definition of Done.

Đầu ra:

* Task template.
* Risk register.
* Definition of Ready và Definition of Done.

⸻

Giai đoạn 6 — Tổng kết và chuẩn hóa: Tuần 11–12

Hoạt động:

* Đánh giá lại dữ liệu so với baseline.
* Trình bày các cải tiến đã thực hiện.
* Xác định nội dung nên trở thành quy định chung.
* Chọn chủ đề cho chu kỳ tiếp theo.

Đầu ra:

* Báo cáo kết quả pilot.
* Danh sách guideline được chính thức áp dụng.
* Backlog cải tiến.
* Kế hoạch chương trình quý tiếp theo.

⸻

5. Cấu trúc triển khai mỗi chủ đề

Mỗi chủ đề kéo dài khoảng hai tuần và sử dụng cùng một quy trình:

1. Learn: Đọc tài liệu hoặc tham gia workshop.
2. Discuss: Thảo luận và phản biện nội dung.
3. Assess: Đánh giá dự án hiện tại.
4. Apply: Thực hiện một cải tiến nhỏ.
5. Review: Đo kết quả và rút kinh nghiệm.
6. Standardize: Chuyển kết quả tốt thành guideline hoặc checklist.

Tỷ lệ thời gian đề xuất:

* 20% lý thuyết.
* 30% thảo luận và phân tích.
* 50% thực hành trên dự án.

⸻

6. Hình thức tổ chức

Mỗi tuần

* Một buổi từ 60 đến 90 phút.
* Tài liệu chuẩn bị trước không quá 30 phút đọc.
* Một bài tập liên quan trực tiếp đến dự án.
* Một người trình bày và một người phản biện.

Phân công vai trò

Program Sponsor

* Xác định mục tiêu và hỗ trợ nguồn lực.
* Giải quyết vấn đề vượt thẩm quyền của nhóm.

Program Owner

* Quản lý lịch, đầu ra và kết quả chương trình.
* Theo dõi việc áp dụng vào dự án.

Topic Owner

* Chuẩn bị nội dung.
* Điều phối workshop.
* Tổng hợp guideline sau buổi học.

Project Leader

* Lựa chọn tình huống thực tế.
* Hỗ trợ đưa cải tiến vào dự án.

Thành viên

* Chuẩn bị trước.
* Tham gia thảo luận.
* Hoàn thành bài tập và phản hồi.

⸻

7. Tiêu chí đánh giá

Chỉ số tham gia

* Tỷ lệ tham dự từ 85% trở lên.
* Tỷ lệ hoàn thành bài tập từ 80% trở lên.
* Mỗi thành viên có ít nhất một lần trình bày hoặc phản biện.

Chỉ số đầu ra

* Mỗi chủ đề tạo ra ít nhất một checklist, template hoặc guideline.
* Mỗi chủ đề có ít nhất một cải tiến được áp dụng vào dự án.
* Tài liệu được lưu tập trung và có người chịu trách nhiệm cập nhật.

Chỉ số tác động

Có thể chọn một số chỉ số phù hợp:

* Giảm bug bị phát hiện sau release.
* Tăng tỷ lệ task hoàn thành đúng hạn.
* Giảm số lần pull request phải sửa lại nhiều vòng.
* Tăng test coverage cho các module quan trọng.
* Giảm thời gian xử lý incident.
* Tăng mức độ rõ ràng của yêu cầu và task.
* Tăng tỷ lệ thành viên đánh giá chương trình hữu ích cho công việc.

Không nên đặt mục tiêu phần trăm quá cao ngay trong chu kỳ đầu. Pilot đầu tiên chủ yếu nhằm xây dựng baseline và kiểm chứng cách triển khai.

⸻

8. Các rủi ro cần tránh

Chương trình biến thành câu lạc bộ đọc sách

Thành viên chỉ trình bày nội dung sách nhưng không tạo ra thay đổi trong dự án.

Cách xử lý: Mọi chủ đề phải có bài tập thực tế và đầu ra được review.

Nội dung quá rộng

Mỗi buổi bao phủ quá nhiều khái niệm, người học hiểu sơ bộ nhưng không áp dụng được.

Cách xử lý: Mỗi chu kỳ chỉ giải quyết một vấn đề cụ thể.

Tạo quá nhiều guideline

Tài liệu được tạo ra nhưng không ai sử dụng hoặc cập nhật.

Cách xử lý: Chỉ chuẩn hóa những nội dung đã được thử nghiệm trên dự án.

Chỉ leader tham gia xây dựng chương trình

Developer cảm thấy chương trình mang tính áp đặt.

Cách xử lý: Luân phiên người trình bày, phản biện và lựa chọn case study.

Không có dữ liệu trước và sau

Không thể chứng minh chương trình có hiệu quả.

Cách xử lý: Xây dựng baseline đơn giản trước khi bắt đầu pilot.

⸻

9. Đề xuất chương trình đầu tiên

Tên đề xuất:

Engineering Excellence Pilot — From Knowledge to Practice

Phạm vi:

* Software Testing Mindset.
* 12-Factor App.
* Code Review và Clean Code.
* Task Breakdown và Risk Management.

Thời gian:

* 12 tuần.
* Một buổi mỗi tuần.
* Từ 60 đến 90 phút mỗi buổi.

Kết quả kỳ vọng:

* Một test strategy mẫu.
* Một 12-Factor checklist.
* Một code review checklist.
* Một task breakdown template.
* Một risk register.
* Tối thiểu bốn cải tiến thực tế được áp dụng vào dự án.

Sau pilot, công ty có thể mở rộng sang:

* System Design.
* Observability.
* Security.
* Technical Leadership.
* AI-assisted Development.