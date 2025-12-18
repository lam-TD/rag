# Checklist dự án – Giai đoạn Tiến hành (Execution)

> Mục tiêu: kiểm soát **phạm vi – tiến độ – chất lượng – rủi ro – truyền thông** để dự án chạy ổn định và dự đoán được.

---

## 0) Thông tin nền (1 lần, cập nhật khi thay đổi)
- [ ] Xác định **mục tiêu/OKR** của dự án (1–3 mục tiêu rõ ràng)
- [ ] Xác định **tiêu chí thành công** (KPIs/Acceptance criteria tổng)
- [ ] Xác định **phạm vi In-scope / Out-of-scope**
- [ ] Xác định **deliverables** (danh sách đầu ra + định nghĩa “xong”)
- [ ] Chốt **timeline/milestones** (mốc & ngày)
- [ ] Chốt **nguồn sự thật** (link PRD/SRS, backlog, repo, drive, board)
- [ ] Chốt **cơ chế thay đổi (Change control)**: ai duyệt, form nào, SLA phản hồi
- [ ] Chốt **kênh liên lạc chính** (Slack/Teams/Zalo + rule dùng kênh)

---

## 1) Thiết lập vận hành (1 lần, rà soát hàng tháng)
### 1.1 Nhịp họp & nghi thức
- [ ] Daily (15’): cập nhật tiến độ + blockers + ưu tiên hôm nay
- [ ] Weekly planning (30–60’): chốt mục tiêu tuần/sprint
- [ ] Weekly stakeholder update (15–30’): báo cáo trạng thái + quyết định cần duyệt
- [ ] Demo/Review: trình diễn tính năng hoàn thành
- [ ] Retro: rút kinh nghiệm + action items
- [ ] Quy ước ghi biên bản: ai ghi, format, nơi lưu, thời hạn gửi

### 1.2 Vai trò & trách nhiệm (RACI)
- [ ] Xác định Owner cho: Product/Scope, Tech, QA, DevOps, Security, Data
- [ ] Danh sách stakeholder + mức ưu tiên + người ra quyết định cuối (D)
- [ ] Danh sách liên hệ khẩn cấp (on-call / escalation)

### 1.3 Công cụ
- [ ] Board (Jira/Trello/GitLab): trạng thái chuẩn (To do/In progress/Review/Done)
- [ ] Repo + branch strategy (main/dev/release/hotfix)
- [ ] CI/CD tối thiểu (build + test + lint)
- [ ] Nơi lưu tài liệu (Drive/Confluence/Wiki) + cấu trúc thư mục
- [ ] Quy ước đặt tên tài liệu/issue/tag/release

---

## 2) Checklist lập kế hoạch thực thi (mỗi Sprint/tuần)
### 2.1 Backlog readiness
- [ ] Backlog được ưu tiên (P0/P1/P2) và có owner
- [ ] User story có: mô tả, value, AC, mock/flow (nếu cần)
- [ ] Task kỹ thuật đã bóc tách đủ nhỏ (≤ 1–2 ngày/task)
- [ ] Có estimate (SP/giờ) + capacity tuần/sprint
- [ ] Dependency đã được ghi rõ và có người xử lý
- [ ] Các hạng mục rủi ro cao được spike/POC trước

### 2.2 Sprint/tuần goal
- [ ] Chốt goal rõ ràng (1–3 dòng)
- [ ] Chốt danh sách commit scope (cái gì chắc chắn giao)
- [ ] Chốt “không làm” (để tránh scope creep)

---

## 3) Checklist điều phối hằng ngày (Daily Ops)
### 3.1 Theo dõi tiến độ
- [ ] Board được cập nhật đúng trạng thái (ít nhất 1 lần/ngày)
- [ ] Mỗi task đang làm có: assignee, ETA, link PR/MR
- [ ] Theo dõi burndown/burnup (nếu có) hoặc checklist hoàn thành theo ngày

### 3.2 Blocker management (cực quan trọng)
- [ ] Tất cả blocker được ghi vào Issue log
- [ ] Mỗi blocker có owner + deadline + next action
- [ ] Escalate đúng cấp nếu quá SLA (vd: 24h không giải quyết)
- [ ] Dependency với team khác có người “đầu mối” theo dõi

### 3.3 Truyền thông nội bộ
- [ ] Daily update: “Done / Today / Blocked”
- [ ] Quyết định quan trọng được chốt bằng văn bản (comment/email)
- [ ] Không để quyết định trôi trong chat (phải có link/tài liệu)

---

## 4) Checklist chất lượng (Quality Gate)
### 4.1 Definition of Done (DoD)
- [ ] Code review đạt chuẩn (ít nhất 1 reviewer)
- [ ] Unit tests/Integration tests đạt mức tối thiểu đã thống nhất
- [ ] Lint/format pass
- [ ] Build pass trên CI
- [ ] Feature có logging cơ bản + error handling
- [ ] Cập nhật tài liệu (README/CHANGELOG/API docs) nếu ảnh hưởng
- [ ] QA/UAT pass theo AC
- [ ] Không còn bug severity cao (Blocker/Critical)

### 4.2 Quản lý bug
- [ ] Bug được phân loại severity/priority
- [ ] Có SLA sửa bug theo mức độ
- [ ] Regression test checklist cho các bug đã fix
- [ ] Báo cáo xu hướng bug (tăng/giảm) mỗi tuần

### 4.3 Phiên bản & release
- [ ] Quy ước versioning (SemVer hoặc theo ngày)
- [ ] Release note có: tính năng, fix, thay đổi breaking, migration
- [ ] Tag/release được tạo đúng quy ước
- [ ] Có rollback plan cho release

---

## 5) Checklist rủi ro & vấn đề (Risk/Issue)
### 5.1 Risk log (cập nhật hàng tuần)
- [ ] Top 10 risks có: mô tả, xác suất, ảnh hưởng, mức độ, owner
- [ ] Có mitigation plan + trigger condition
- [ ] Risk mới phát sinh được ghi ngay (không để “nhớ trong đầu”)

### 5.2 Issue log (cập nhật hằng ngày)
- [ ] Issue có: mô tả, ảnh hưởng, owner, deadline, trạng thái
- [ ] Có decision/giải pháp và ghi nhận bài học (nếu tái diễn)

---

## 6) Checklist quản lý thay đổi (Scope & Change)
- [ ] Mọi yêu cầu mới đều tạo ticket/change request
- [ ] Đánh giá tác động: effort, timeline, cost, risk, quality
- [ ] Có quyết định: accept / defer / reject + lý do
- [ ] Cập nhật lại plan/milestone sau khi change được duyệt
- [ ] Thông báo stakeholder liên quan (không “âm thầm” đổi scope)

---

## 7) Checklist bảo mật & tuân thủ (tùy dự án)
- [ ] Access control: quyền repo/CI/DB được cấp đúng người
- [ ] Secrets management: không hardcode key, có rotate policy
- [ ] Log không chứa dữ liệu nhạy cảm (PII/secret)
- [ ] Backup/restore tối thiểu (DB, file, config)
- [ ] Security review cho tính năng nhạy cảm (auth/payment/upload)

---

## 8) Checklist triển khai (Deployment Readiness)
- [ ] Môi trường dev/staging/prod tách biệt rõ ràng
- [ ] ENV/config được quản lý (không cấu hình tay lộn xộn)
- [ ] Healthcheck/monitoring tối thiểu (uptime, error rate)
- [ ] Migration plan (DB) + dữ liệu mẫu (nếu cần)
- [ ] Rollback plan đã thử (hoặc mô phỏng)
- [ ] Runbook: cách deploy, cách xử lý sự cố phổ biến

---

## 9) Checklist báo cáo cho stakeholder (Weekly Status)
- [ ] Trạng thái: Green / Yellow / Red (kèm lý do)
- [ ] Done tuần này (3–7 gạch đầu dòng)
- [ ] Plan tuần tới (3–7 gạch đầu dòng)
- [ ] Blockers cần hỗ trợ/ra quyết định (rõ ai cần làm gì)
- [ ] Rủi ro top 3 + kế hoạch giảm thiểu
- [ ] Các mốc sắp tới (ngày cụ thể)
- [ ] Tài nguyên/capacity: có thiếu người hay không

---

## 10) Checklist kết thúc sprint/phase (Review & Retro)
- [ ] Demo đầy đủ theo scope đã commit
- [ ] Tổng kết: đạt/không đạt goal + nguyên nhân
- [ ] Các hạng mục dở dang: re-plan + re-estimate
- [ ] Retro action items: 1–3 việc cụ thể, có owner, có deadline
- [ ] Cập nhật tài liệu/kiến thức (wiki/runbook)

---

## 11) Mẫu log nhanh (copy/paste)
### 11.1 Risk item
- ID:
- Mô tả:
- Xác suất/Ảnh hưởng:
- Mức độ:
- Trigger:
- Mitigation:
- Owner:
- Trạng thái:

### 11.2 Issue item
- ID:
- Mô tả:
- Ảnh hưởng:
- Root cause (nếu biết):
- Next action:
- Owner:
- Deadline:
- Trạng thái:

### 11.3 Weekly status (1 đoạn)
- Status:
- Highlights:
- Next:
- Needs help:
- Risks: