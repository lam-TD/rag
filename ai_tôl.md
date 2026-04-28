# Đề xuất ứng dụng AI Tool vào công việc của công ty phát triển phần mềm/web

## Mục tiêu nghiên cứu

Khảo sát và đề xuất các hướng ứng dụng AI tool khả thi nhất cho công ty phát triển phần mềm/web, dựa trên các tiêu chí chính:

- **Bảo mật**
- **Tăng ít nhất 10% tốc độ hoàn thành task của developer**
- **Khả thi khi triển khai pilot**
- **Không làm giảm chất lượng code hoặc tăng rủi ro vận hành**

---

## 1. Tổng quan 3 đề xuất ưu tiên

| # | Đề xuất | Mục tiêu chính | Mức khả thi | Ưu tiên |
|---|---|---|---|---|
| 1 | **AI coding assistant trong IDE** | Dev code nhanh hơn, giảm boilerplate, viết test/refactor nhanh hơn | Cao | Rất nên pilot |
| 2 | **AI code review + security/static analysis** | Giảm thời gian review, phát hiện bug/security sớm | Cao | Rất nên pilot |
| 3 | **Internal AI knowledge assistant/RAG** | Giảm thời gian tìm tài liệu, hỏi senior, hiểu source code/quy trình | Trung bình–cao | Nên pilot sau hoặc song song nhỏ |

---

# Đề xuất 1: AI Coding Assistant cho Developer

Ví dụ công cụ:

- GitHub Copilot Business/Enterprise
- JetBrains AI Enterprise
- Cursor Enterprise
- Hoặc công cụ tương đương có chính sách doanh nghiệp

## Use case phù hợp với công ty web/software

| Nhóm việc | AI hỗ trợ |
|---|---|
| CRUD/API | Generate controller/service/repository/schema cơ bản |
| Unit test | Gợi ý test cases, mock, edge cases |
| Refactor | Tách hàm, đổi tên biến, giảm duplicate |
| Frontend | Generate component, form validation, TypeScript type |
| Backend | Viết migration, query, DTO, validation |
| Documentation | Viết README, API docs, comment kỹ thuật |

## Lý do khả thi

AI coding assistant là nhóm công cụ dễ triển khai nhất vì developer có thể dùng trực tiếp trong IDE hoặc code editor hiện tại.

Một số nghiên cứu thực nghiệm về GitHub Copilot cho thấy nhóm dùng AI pair programmer có thể hoàn thành task nhanh hơn đáng kể so với nhóm không dùng. Vì vậy, mục tiêu nội bộ **tăng 10% tốc độ hoàn thành task** là mục tiêu tương đối thận trọng, miễn là chọn đúng loại task để pilot.

Nguồn tham khảo:

- GitHub Copilot productivity study: https://arxiv.org/abs/2302.06590
- GitHub Copilot Business/Enterprise privacy discussion: https://github.com/orgs/community/discussions/188488

## Điều kiện bảo mật nên yêu cầu

| Rủi ro | Kiểm soát đề xuất |
|---|---|
| Lộ source code nội bộ | Chỉ dùng gói Business/Enterprise, cấm dùng account cá nhân |
| Lộ secret/API key | Bật secret scanning, pre-commit hook, training guideline |
| Code AI sinh ra kém chất lượng | Bắt buộc human review + test + CI |
| AI dùng dữ liệu để train | Chỉ chọn vendor có cam kết không train trên business data hoặc có setting quản trị rõ ràng |
| Gợi ý code giống public code | Bật policy chặn hoặc cảnh báo public code matching nếu tool hỗ trợ |

## KPI đo pilot

| KPI | Cách đo |
|---|---|
| Dev completion time | So sánh thời gian từ `In Progress` → `Ready for Review/Done` |
| % task hoàn thành sớm hơn baseline | Mục tiêu: ≥ 10% |
| PR size/rework | Số lần sửa lại sau review không tăng |
| Defect rate | Bug sau merge không tăng |
| Test coverage | Không giảm, tốt nhất tăng nhẹ |

---

# Đề xuất 2: AI Code Review + Security/Static Analysis

Ví dụ công cụ:

- GitHub Copilot Code Review
- CodeQL
- SonarQube AI Code Assurance
- Snyk Code/AI Security

## Mục tiêu

Không thay thế human reviewer, mà tạo một bước **pre-review tự động** trước khi senior/dev lead review.

## Workflow đề xuất

```text
Developer tạo PR
        ↓
AI review / Static analysis chạy tự động
        ↓
Dev xử lý issue rõ ràng trước
        ↓
Human reviewer tập trung vào business logic, architecture, maintainability
        ↓
Merge nếu pass CI + quality gate
```

## Giá trị mang lại

AI code review và static analysis giúp giảm thời gian reviewer phải bắt các lỗi lặp lại như:

- Naming chưa rõ
- Code duplicate
- Thiếu test
- Logic đơn giản bị sai
- Risk về SQL injection, XSS, insecure config
- Dependency issue
- Complexity quá cao
- Code AI sinh ra chưa đạt chuẩn

Nguồn tham khảo:

- GitHub Copilot Code Review: https://docs.github.com/en/copilot/concepts/agents/code-review
- CodeQL Code Scanning: https://docs.github.com/code-security/code-scanning/introduction-to-code-scanning/about-code-scanning-with-codeql
- SonarQube AI Code Assurance: https://docs.sonarsource.com/sonarqube-server/ai-capabilities/ai-code-assurance

## Lưu ý về công nghệ

CodeQL hỗ trợ nhiều ngôn ngữ như:

- JavaScript/TypeScript
- Python
- Java/Kotlin
- C#
- Go
- Ruby
- Rust
- Swift

Tuy nhiên, CodeQL không phải lúc nào cũng phù hợp nếu công ty có nhiều project PHP/Laravel. Trong trường hợp đó, nên cân nhắc thêm SonarQube hoặc Snyk để hỗ trợ tốt hơn cho PHP.

## Use case phù hợp

| Use case | Giá trị |
|---|---|
| Review PR nhỏ/trung bình | Giảm lỗi cơ bản trước khi human review |
| Check security | SQL injection, XSS, insecure config, dependency risk |
| Check maintainability | Duplicate, complexity, naming, dead code |
| Review AI-generated code | Đảm bảo code AI không bypass quality standard |

## KPI đo pilot

| KPI | Mục tiêu |
|---|---|
| PR review cycle time | Giảm ≥ 10% |
| Số comment lặp lại về lỗi cơ bản | Giảm |
| Số bug/security issue bị phát hiện trước merge | Tăng |
| Defect escape rate sau release | Không tăng hoặc giảm |
| Reviewer satisfaction | Tăng, vì reviewer bớt phải bắt lỗi nhỏ |

## Nguyên tắc quan trọng

AI review không nên được tính là approval cuối cùng.

AI review nên được xem là:

> Review assistant, không phải reviewer chịu trách nhiệm.

Human reviewer vẫn phải chịu trách nhiệm cuối cùng về:

- Business logic
- Architecture
- Security impact
- Maintainability
- Khả năng vận hành sau khi merge

---

# Đề xuất 3: Internal AI Knowledge Assistant / RAG

Đây là đề xuất phù hợp nếu công ty có nhiều tài liệu rải rác như:

- Coding convention
- Onboarding docs
- API docs
- Deployment guide
- Incident notes
- Requirement docs
- Architecture Decision Records
- Meeting notes
- System design documents

## Use case

| Tình huống | AI assistant hỗ trợ |
|---|---|
| Dev mới vào team | Hỏi “project này chạy local như thế nào?” |
| Dev đang làm task | Hỏi “quy ước viết service/repository ở project này là gì?” |
| Debug | Hỏi “lỗi deploy thường gặp ở GitLab CI là gì?” |
| Review | Hỏi “coding standard về exception handling của team là gì?” |
| BA/PM/QA | Hỏi logic nghiệp vụ từ tài liệu có citation |

## Thiết kế đề xuất

```text
Internal docs / code guidelines / API docs
        ↓
Index theo collection/project/team
        ↓
AI search + answer with citations
        ↓
Nếu không đủ dữ liệu → trả lời "không đủ thông tin"
```

## Điều kiện bảo mật

| Rủi ro | Kiểm soát |
|---|---|
| Lộ tài liệu nội bộ | RBAC theo project/team |
| AI trả lời sai | Bắt buộc citation/source |
| Prompt injection từ tài liệu | Lọc nguồn, cảnh báo dữ liệu không đáng tin, không cho AI tự thực thi action |
| Dữ liệu nhạy cảm | Phân loại tài liệu: public/internal/confidential/restricted |
| Trả lời vượt quyền | Search theo quyền của user, không index tất cả vào một kho chung |

## KPI đo pilot

| KPI | Mục tiêu |
|---|---|
| Thời gian tìm tài liệu | Giảm ≥ 10–20% |
| Số câu hỏi lặp lại cho senior/dev lead | Giảm |
| Onboarding time | Giảm |
| Tỷ lệ câu trả lời có citation đúng | ≥ 90% |
| Số lần AI trả lời “không đủ thông tin” đúng lúc | Có theo dõi |

## Nguồn tham khảo

- OpenAI Enterprise Privacy: https://openai.com/enterprise-privacy/

---

# Ma trận chấm điểm đề xuất

| Tiêu chí | AI coding assistant | AI code review/security | Internal AI knowledge/RAG |
|---|---:|---:|---:|
| Tăng tốc dev ≥ 10% | 5/5 | 4/5 | 3.5/5 |
| Bảo mật | 3.5/5 | 4/5 | 4/5 nếu tự kiểm soát RBAC |
| Dễ triển khai | 5/5 | 4/5 | 3/5 |
| Dễ đo KPI | 4/5 | 5/5 | 3.5/5 |
| Tác động tới quy trình hiện tại | Trung bình | Thấp–trung bình | Trung bình |
| Khả năng pilot trong 4–6 tuần | Cao | Cao | Trung bình |

## Kết luận đề xuất

Nên chọn **AI coding assistant** và **AI code review/security** làm 2 pilot đầu tiên vì:

- Dễ triển khai
- Dễ đo KPI
- Tác động trực tiếp đến thời gian hoàn thành task
- Có thể tích hợp vào workflow hiện tại của developer
- Không cần xây dựng hệ thống phức tạp ngay từ đầu

**Internal AI knowledge/RAG** nên là đề xuất thứ 3 vì giá trị lâu dài cao, đặc biệt với công ty có:

- Nhiều project
- Nhiều team
- Nhiều convention
- Onboarding khó
- Tài liệu phân tán

---

# Cách thiết kế khảo sát nội bộ

Có thể thiết kế khảo sát theo 5 nhóm câu hỏi.

---

## 1. Current Pain Points

| Câu hỏi | Mục đích |
|---|---|
| Dev thường mất thời gian nhất ở giai đoạn nào? | Xác định AI nên can thiệp vào đâu |
| Task nào lặp lại nhiều nhất? | Tìm use case phù hợp |
| Review PR có đang là bottleneck không? | Đánh giá đề xuất AI review |
| Dev có mất nhiều thời gian tìm tài liệu/hỏi người khác không? | Đánh giá RAG assistant |

---

## 2. AI Readiness

| Câu hỏi | Mục đích |
|---|---|
| Bạn đã từng dùng AI coding tool chưa? | Đo adoption |
| Bạn dùng AI cho việc gì? | Tìm use case thật |
| Bạn có tin code AI sinh ra không? | Đo risk perception |
| Bạn cần guideline gì để dùng AI an toàn? | Chuẩn bị policy |

---

## 3. Security Concern

| Câu hỏi | Mục đích |
|---|---|
| Bạn có lo ngại việc paste source code vào AI không? | Đo mức nhạy cảm |
| Loại dữ liệu nào không được đưa vào AI? | Xây policy |
| Có cần phân quyền theo project/team không? | Thiết kế RBAC |
| Có cần audit log prompt/output không? | Governance |

---

## 4. Productivity Measurement

| Câu hỏi | Mục đích |
|---|---|
| Theo bạn AI có thể giúp giảm bao nhiêu % thời gian task? | So với mục tiêu 10% |
| Loại task nào dễ tăng tốc nhất? | Chọn pilot task |
| Bạn chấp nhận dùng AI nếu phải review kỹ output không? | Đánh giá khả năng áp dụng |

---

## 5. Pilot Commitment

| Câu hỏi | Mục đích |
|---|---|
| Bạn có sẵn sàng tham gia pilot 4–6 tuần không? | Chọn nhóm thử nghiệm |
| Bạn muốn tool tích hợp ở IDE, GitHub/GitLab, hay chat nội bộ? | Chọn kênh triển khai |
| Bạn cần training bao lâu để dùng hiệu quả? | Lên kế hoạch rollout |

---

# Pilot Plan đề xuất

| Giai đoạn | Thời lượng | Việc cần làm |
|---|---:|---|
| Baseline | 2 tuần | Đo thời gian task hiện tại, PR review time, bug/rework |
| Pilot | 4–6 tuần | Cho 1–2 team dùng AI tool với guideline rõ ràng |
| Evaluation | 1 tuần | So sánh KPI trước/sau |
| Decision | 1 tuần | Mở rộng, điều chỉnh hoặc dừng |

---

# Success Criteria

Pilot được xem là thành công nếu:

```text
1. Thời gian hoàn thành task giảm ít nhất 10%.
2. Defect rate không tăng.
3. Không có vi phạm bảo mật dữ liệu.
4. Developer satisfaction ≥ 70%.
5. Reviewer không ghi nhận tăng burden do code AI kém chất lượng.
```

---

# Kết luận ngắn để đưa vào báo cáo

Ba đề xuất khả thi nhất là:

1. **AI coding assistant cho developer** để tăng tốc coding, test, refactor và documentation.
2. **AI code review + security scanning** để giảm bottleneck review và kiểm soát chất lượng code AI sinh ra.
3. **Internal AI knowledge assistant/RAG** để giảm thời gian tìm tài liệu, hỏi senior và onboarding.

Trong đó, nên ưu tiên pilot **#1 và #2 trước** vì dễ đo tác động trực tiếp lên mục tiêu **giảm ít nhất 10% thời gian hoàn thành task dev**, đồng thời vẫn kiểm soát được rủi ro bảo mật thông qua:

- Enterprise plan
- RBAC
- Audit log
- Secret scanning
- Human review
- Quality gate

---

# Phụ lục: Gợi ý chính sách sử dụng AI an toàn

## Dữ liệu không được đưa vào AI tool public

- Source code private nếu chưa được công ty cho phép
- API key, password, token, secret
- Dữ liệu khách hàng
- Thông tin hợp đồng
- Dữ liệu tài chính
- Dữ liệu cá nhân
- Incident report nhạy cảm
- Tài liệu nội bộ thuộc nhóm confidential/restricted

## Nguyên tắc sử dụng AI cho developer

```text
AI can suggest, but developer owns the final code.
```

Developer cần chịu trách nhiệm:

- Hiểu code trước khi commit
- Kiểm tra security impact
- Viết hoặc cập nhật test
- Không paste secret vào AI
- Không dùng AI output nếu chưa review
- Không bypass code review/CI/quality gate

## Nguyên tắc dùng AI trong review

```text
AI review is a support layer, not a final approval.
```

AI có thể hỗ trợ:

- Phát hiện lỗi cơ bản
- Gợi ý refactor
- Gợi ý test case
- Cảnh báo security smell
- Tóm tắt PR

Human reviewer vẫn quyết định cuối cùng.
