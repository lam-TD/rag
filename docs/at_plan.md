# Kế hoạch Automation Test — 2 Dự án PHP (Thí điểm)

> Tài liệu thảo luận nội bộ
> Phiên bản nháp — cần điều chỉnh theo bối cảnh cụ thể từng dự án

-----

## 1. Bối cảnh & ràng buộc (đã xác nhận)

|Yếu tố              |Giá trị                                            |
|--------------------|---------------------------------------------------|
|Stack               |PHP thuần (không framework), full-stack có UI      |
|Phạm vi thí điểm    |2 dự án PHP                                        |
|Tình trạng test     |Chưa có automation, **chưa có CI/CD**              |
|Codebase            |Khó test — logic lẫn UI, ít tách hàm (legacy-style)|
|Người viết & duy trì|Cả team dev cùng viết                              |
|Baseline số liệu    |Chưa có — **sẽ tự thu thập trước khi bắt đầu**     |
|CI/CD platform      |GitLab CI                                          |
|Timeline            |Không có deadline cứng, làm theo giai đoạn         |

**Định nghĩa “thay thế normal test”:** Automation gánh phần lớn các case lặp lại (regression). Manual test **không bị bỏ hoàn toàn** — giữ lại cho exploratory, usability, edge case.

-----

## 2. Mục tiêu

### Định lượng

1. **Giảm 30% công sức test trước release** (so với baseline)
1. **Giảm 20% thời gian từ dev xong → merge vào `develop`** (so với baseline)

### Định tính

1. **Ghi chép kiến thức** — test đóng vai trò tài liệu sống về hành vi hệ thống

-----

## 3. ⚠️ Cảnh báo & kỳ vọng thực tế (đọc kỹ trước khi cam kết)

Đây là phần quan trọng nhất để thảo luận với nhóm, dựa trên các nguồn uy tín:

### 3.1. Mục tiêu định lượng chỉ đo được khi có baseline

Không có số liệu gốc thì không thể chứng minh “giảm 30%/20%”. Lưu ý ROI đo quá sớm
thường ra kết quả âm vì lợi ích automation tích lũy dần theo thời gian
(BrowserStack, 2026).
→ **Bắt buộc đo baseline TRƯỚC khi thay đổi quy trình.** Đo “sau” rồi mới đo “trước”
sẽ làm số liệu mất giá trị so sánh.

### 3.2. Thời gian hoàn vốn không nhanh

- Tổ chức thường kỳ vọng thu hồi vốn trong 6–12 tháng; setup trưởng thành đạt
  150–200% ROI dài hạn nhờ giảm chu kỳ regression (ThinkSys).
- Với team nhỏ + ít test, ROI dương thực tế có thể ở mốc 18–24 tháng nếu regression
  thủ công đang chiếm >20% sức sprint (ContextQA, 2026).
  → **Đừng kỳ vọng kết quả trong quý đầu.**

### 3.3. Mục tiêu “giảm 20% thời gian dev→merge” có thể ĐI NGƯỢC trong ngắn hạn

Giai đoạn đầu, thêm test + refactor code khó test sẽ **làm CHẬM** dev→merge trước
khi nhanh lên. Cần truyền thông rõ điều này với nhóm để tránh mất niềm tin.

### 3.4. “Thay thế manual” 100% là phi thực tế

- Giả định automation thay thế hoàn toàn manual là phi thực tế (BrowserStack).
- Automation *bổ sung* cho manual, không thay thế: manual vẫn thiết yếu cho
  exploratory, usability, edge case (ThinkSys).

### 3.5. Code khó test là rào cản số một (Legacy Dilemma)

Vấn đề kinh điển: *không thể refactor an toàn nếu chưa có test, nhưng cần refactor
để viết được test*. Giải pháp là **Characterization Test** (xem mục 5).

### 3.6. “Cả team cùng viết” cần buy-in, không áp đặt

Nếu team lo automation thay thế họ, cần truyền thông rõ là không có sự thay thế nào,
automation chỉ làm mạnh thêm quy trình (nhiều nguồn).

-----

## 4. Công cụ đề xuất (PHP thuần)

|Mục đích                  |Công cụ                      |Ghi chú                          |
|--------------------------|-----------------------------|---------------------------------|
|Unit / Integration test   |**PHPUnit**                  |Chuẩn công nghiệp cho PHP        |
|(Tùy chọn) Syntax hiện đại|Pest                         |Build trên PHPUnit, cú pháp gọn  |
|E2E (UI)                  |**Playwright** hoặc Cypress  |Chỉ làm SAU, cho luồng quan trọng|
|Code coverage             |Xdebug / PCOV                |Tích hợp PHPUnit                 |
|CI/CD                     |**GitLab CI**                |`.gitlab-ci.yml`                 |
|Báo cáo                   |JUnit XML (GitLab đọc native)|Hiển thị test report trong MR    |

-----

## 5. Chiến lược cho code khó test: Characterization Test

Vì codebase trộn logic với UI, **không viết unit test trực tiếp ngay được**. Quy trình an toàn:

1. **Xác định điểm cần đổi** (change point) — nơi hay sửa nhất.
1. **Tìm điểm có thể viết test** (test point / seam).
1. **Phá vỡ phụ thuộc** — tách logic ra khỏi UI/DB ở mức tối thiểu, an toàn.
1. **Viết characterization test** — ghi lại hành vi *hiện tại* của code (kể cả khi
   chưa chắc đúng/sai), làm lưới an toàn.
1. **Refactor** dần dần, chạy lại test liên tục để đảm bảo không phá hành vi cũ.

> Characterization test ghi lại code *đang làm gì*, không phải *nên làm gì* — đây
> chính là cơ chế “ghi chép kiến thức” (mục tiêu 3).

-----

## 6. Cách đo Baseline (Giai đoạn 0 — bạn tự thực hiện)

Thực hiện trong **2–4 tuần TRƯỚC KHI** viết test hay đổi quy trình. Cần đo tối thiểu:

|Chỉ số                          |Cách đo                                                              |Phục vụ mục tiêu            |
|--------------------------------|---------------------------------------------------------------------|----------------------------|
|Giờ test thủ công / release     |QA/dev ghi log thời gian test mỗi release                            |Mục tiêu 1 (30%)            |
|Thời gian dev→merge             |Thời gian từ commit “done” đến merge vào `develop` (lấy từ GitLab MR)|Mục tiêu 2 (20%)            |
|Số bug lọt sau release          |Đếm bug production / release                                         |Đánh giá chất lượng         |
|Số case test lặp lại mỗi release|Liệt kê các case test thủ công lặp đi lặp lại                        |Xác định ứng viên automation|

**Lưu ý:** đo ít nhất 2–3 release để có trung bình, tránh lấy 1 lần làm chuẩn.

-----

## 7. Lộ trình theo giai đoạn (không gắn deadline cứng)

### Giai đoạn 0 — Đo baseline *(điều kiện tiên quyết)*

- [ ] Đo 4 chỉ số ở mục 6, qua 2–3 release
- [ ] Liệt kê các case test thủ công lặp lại (ứng viên automation)

### Giai đoạn 1 — Hạ tầng CI/CD *(có thể song song GĐ0)*

- [ ] Tạo `.gitlab-ci.yml` cơ bản
- [ ] Cài PHPUnit + Xdebug/PCOV
- [ ] Chạy được 1 test mẫu trong pipeline GitLab
- [ ] Hiển thị test report trong Merge Request

### Giai đoạn 2 — Characterization test cho 1 luồng quan trọng nhất

- [ ] Chọn 1 luồng nghiệp vụ giá trị cao + hay bị sửa
- [ ] Viết characterization test bọc quanh luồng đó
- [ ] Tách logic khỏi UI ở mức tối thiểu, an toàn
- [ ] Tài liệu hóa convention viết test cho nhóm

### Giai đoạn 3 — Mở rộng regression + đo lại

- [ ] Tự động hóa các case regression lặp nhiều nhất (ROI cao nhất)
- [ ] Đo lại 4 chỉ số, so sánh với baseline GĐ0
- [ ] Đánh giá đã đạt bao nhiêu % so với mục tiêu 30%/20%

### Giai đoạn 4 — Quality gate + tài liệu hóa

- [ ] Block merge vào `develop` nếu test fail
- [ ] Đặt ngưỡng coverage tối thiểu (bắt đầu thấp, tăng dần)
- [ ] Hoàn thiện tài liệu test convention cho cả team

-----

## 8. Tiêu chí ưu tiên chọn cái gì automation trước

Ưu tiên cao (ROI tốt): case **lặp lại nhiều**, regression, smoke test, logic nghiệp vụ thuần.
Ưu tiên thấp (cân nhắc): UI phức tạp, case ad-hoc, luồng ít thay đổi — chi phí maintain
có thể vượt lợi ích, để manual có khi rẻ hơn.

-----

## 9. Nguồn tham khảo

1. BrowserStack — How to Calculate Test Automation ROI (2026)
   <https://www.browserstack.com/guide/calculate-test-automation-roi>
1. ContextQA — ROI of Test Automation: Benchmarks & Calculation Guide (2026)
   <https://contextqa.com/blog/roi-of-test-automation/>
1. ThinkSys — Test Automation ROI Framework Guide
   <https://thinksys.com/qa-testing/test-automation-roi-framework-guide/>
1. Quinnox — How to Calculate Test Automation ROI (2025)
   <https://www.quinnox.com/blogs/test-automation-roi/>
1. Characterization testing — adding tests to legacy code (Mario Cervera, 2025)
   <https://mariocervera.com/characterization-testing-adding-tests-to-legacy-code>
1. Refactoring Legacy code with tests (testdouble)
   <https://github.com/testdouble/contributing-tests/wiki/Refactoring-Legacy-code-with-tests>
1. Augment Code — How to Refactor Legacy Code (2026)
   <https://www.augmentcode.com/learn/how-to-refactor-legacy-code>

-----

## 10. Câu hỏi mở để thảo luận với nhóm

- Ai chịu trách nhiệm đo baseline (GĐ0) và trong bao lâu?
- Luồng nghiệp vụ nào nên chọn làm thí điểm characterization test ở GĐ2?
- Ngưỡng coverage tối thiểu ban đầu đặt bao nhiêu cho hợp lý?
- Có chấp nhận việc dev→merge CHẬM hơn trong giai đoạn đầu không?
- Phân chia thế nào giữa thời gian viết test và thời gian làm feature mới?

-----

*Tài liệu nháp phục vụ thảo luận. Các con số ROI/thời gian là tham chiếu ngành, cần
hiệu chỉnh theo số liệu baseline thực tế của công ty.*