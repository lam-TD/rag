# Template báo cáo tuần + Hướng dẫn

> Mục tiêu: người đọc (GĐ, BrSE) nhìn 1 phút là biết dự án ổn hay không, deadline nào gần.
> Người viết mất tối đa 30 phút/tuần.
> Cách áp dụng: dùng thử 4 tuần, sau đó cùng chỉnh rồi chốt.

## 1. Template (copy vào Teams)

```text
📋 BÁO CÁO TUẦN — [Tên leader] — Tuần [số] ([ngày]–[ngày])

■ [Tên dự án A] — [🟢/🟡/🔴] [1 câu tình trạng]
- Cột mốc sắp tới: [tên] — deadline [dd/mm] (Redmine #[id]) — hoàn thành ~[X]%
- Tuần này: (tối đa 3 gạch — ghi việc ĐÃ XONG hoặc ĐANG LÀM, nói rõ cái nào)
- Tuần sau: (tối đa 3 gạch)
- Vướng mắc / cần hỗ trợ: [cần ai làm gì, trước ngày nào] hoặc "Không"

■ [Tên dự án B] — (như trên)

■ Nhiệm vụ khác: [tuyển dụng, đào tạo, hỗ trợ team khác…] hoặc "Không"
■ Nghỉ phép sắp tới: [tên — ngày] hoặc "Không"
```

## 2. Quy ước chung

### 2.1. Đèn trạng thái

| Đèn | Định nghĩa | Dấu hiệu nhận biết (khi phân vân) | Phải ghi kèm |
|---|---|---|---|
| 🟢 | Dự kiến hoàn thành đúng hạn, chưa cần can thiệp | Không có dấu hiệu nào của 🟡 | — |
| 🟡 | Deadline hoặc phạm vi có nguy cơ bị ảnh hưởng — cần theo dõi hoặc hành động | Có thể trễ một deadline trong 2 tuần tới; chờ đầu vào đã quá ngày hẹn; (dự án maintain) ticket tồn tăng 2 tuần liền | Rủi ro ở mốc nào, khoảng bao lâu, vì sao, cần gì để gỡ |
| 🔴 | Không thể giữ đồng thời deadline, phạm vi và chất lượng theo kế hoạch hiện tại | Đã trễ, hoặc chắc chắn trễ / phải cắt tính năng / phải hạ chất lượng | Như 🟡 + đề xuất phương án đánh đổi để cấp trên chọn |

**Bật 🟡 sớm là làm tốt, không phải nhận lỗi.** Đáng lo là tuần trước 🟢, tuần này nhảy thẳng 🔴.

### 2.2. Deadline lấy từ đâu

1. Deadline trong báo cáo phải là ngày **đã có trên Redmine** (due date hoặc version, do PM đặt hoặc duyệt). Luôn ghi kèm mã #ticket.
2. PM mới chốt qua chat, chưa lên Redmine → dùng được, nhưng phải đưa lên Redmine ngay trong tuần.
3. PM chưa xác nhận → ghi rõ: `chưa xác nhận với PM (dự kiến 25/07)`. Không được viết như đã chốt.
4. % hoàn thành — theo thứ tự ưu tiên, không theo cảm giác:
   - Tốt nhất: theo **effort / estimated hours** trên Redmine (giờ đã xong ÷ tổng giờ ước tính).
   - Không có estimate: theo **tỷ lệ ticket**, và phải ghi rõ nhãn, ví dụ `~60% (tỷ lệ ticket)` — vì ticket to nhỏ khác nhau, số này chỉ là ước thô.
   - Chưa tính được: ghi rõ lý do, ví dụ "chưa tính được (chờ chốt danh sách task)".

### 2.3. Dự án không có milestone

- **Dự án maintain / task lẻ:** thay dòng "Cột mốc sắp tới" bằng:
  `Ticket tuần này: nhận [X] / xong [Y] / tồn [Z] (tồn quá 2 tuần: [N])`
- **Có mốc bàn giao nhưng không phải version Redmine** (báo cáo định kỳ, buổi demo…): vẫn ghi dòng cột mốc, kèm nguồn xác nhận (ticket, biên bản họp ngày nào, tin nhắn PM). Không tính được % thì thay bằng 1 câu tình trạng, ví dụ "đang thu thập dữ liệu, chưa viết".

## 3. Ví dụ

**✅ Đèn 🟢 (báo cáo thật):**

```text
📋 BÁO CÁO TUẦN — [Tên leader] — Tuần 29 (13/07–17/07)

■ Dự án A — 🟢 đúng tiến độ
- Cột mốc sắp tới: v1.3.0 — deadline 30/09/2026 (Redmine #38989) — hoàn thành: chưa tính được (chờ chốt danh sách task)
- Tuần này:
  - Đang thảo luận với PM chốt danh sách task cho v1.3.0 — dự kiến chốt 17/07/2026
  - Đang làm, kịp hạn 17/07: #34255 Refactor RabbitMQ, #34256 Điều tra thư viện Langchain
  - Đang làm, kịp hạn 24/07: #34567 Điều tra CVEs
- Tuần sau:
  - Phân bổ task v1.3.0 sau khi chốt; hoàn thành #34567
- Vướng mắc / cần hỗ trợ: Không

■ Dự án B — 🟢 đúng tiến độ
- Cột mốc sắp tới: Báo cáo đợt 1 — deadline 30/09/2026 (Redmine #345345) — đang ghi nhật ký ứng dụng, chưa vào giai đoạn viết
- Tuần này:
  - Ghi nhật ký ứng dụng AI vào quá trình dev
  - #123456 Hoàn thành triển khai LiteLLM proxy
- Tuần sau:
  - Lựa chọn task sử dụng AI
- Vướng mắc / cần hỗ trợ: Không

■ Nhiệm vụ khác:
- Tech Sharing — thuyết trình 20/10/2026
  - Cột mốc sắp tới: Báo cáo nghiên cứu — 24/07/2026
  - Tuần này: thảo luận và phân công công việc cho từng thành viên
  - Tuần sau: các thành viên nghiên cứu và báo cáo kết quả
- Quy trình đào tạo cho dự án AI
  - Đề cương: đang soạn — deadline 24/07/2026
■ Nghỉ phép sắp tới:
- t-la: 16/07/2026
```

**✅ Đèn 🟡 (ví dụ):** nói rõ trễ mốc nào, vì sao, cần ai giúp gì.

```text
■ Dự án C — 🟡 Có thể trễ release vì chờ spec thanh toán
- Cột mốc sắp tới: Release v2.1 — deadline 25/07/2026 (Redmine v2.1) — hoàn thành ~70%
- Tuần này:
  - Xong: màn hình quản lý user (#35102), fix 5 bug UAT
  - Đang làm: #35110 màn hình lịch sử giao dịch
  - Đã gửi câu hỏi spec thanh toán cho PM từ 08/07 — chưa có trả lời
- Tuần sau:
  - Làm phần thanh toán nếu có spec trước 16/07. Sau ngày đó, chờ thêm ngày nào trễ thêm ngày đó
- Vướng mắc / cần hỗ trợ: nhờ BrSE thúc PM trả lời câu hỏi spec (#35098) trước 16/07
```

**✅ Đèn 🔴 (ví dụ):** không giấu — nói trễ bao lâu, vì sao, và tự đưa phương án cho cấp trên chọn.

```text
■ Dự án D — 🔴 Trễ release: phát hiện 2 bug nặng khi UAT
- Cột mốc sắp tới: Release v3.0 — deadline 18/07/2026 (Redmine v3.0) — hoàn thành ~85%, ước trễ 1 tuần (25/07)
- Tuần này:
  - Xong: 12/14 mục UAT
  - Phát sinh: #35201, #35202 — bug mất dữ liệu khi import file lớn, cần ~4 ngày công để fix và test lại
- Tuần sau:
  - Fix 2 bug trên, chạy lại UAT phần import
- Vướng mắc / cần hỗ trợ: xin PM chọn 1 trong 2, trước họp 15/07:
  (a) lùi release sang 25/07
  (b) giữ 18/07 nhưng tắt tính năng import, bổ sung ở bản v3.0.1
```

Lưu ý từ ví dụ 🔴: dự án D tuần trước đáng lẽ đã là 🟡 (bug bắt đầu lộ khi UAT). Nếu tuần trước còn 🟢 thì câu cấp trên sẽ hỏi là "vì sao không thấy sớm?".

**❌ Không đạt (kiểu "cho có"):**

```text
■ Dự án ABC: đang làm bình thường, dev tiếp các task. Không có gì đặc biệt.
```

Không có deadline, không thấy tiến độ, không biết ổn hay sắp cháy — người đọc phải đi hỏi lại.

## 4. Kiểm tra 30 giây trước khi gửi

- [ ] Mỗi dự án có đèn + deadline kèm mã Redmine (hoặc số liệu ticket)?
- [ ] Deadline nào PM chưa xác nhận đã ghi "chưa xác nhận"?
- [ ] Đèn 🟡/🔴 có lý do + cần gì để gỡ?
- [ ] "Vướng mắc", "Nhiệm vụ khác", "Nghỉ phép" đã điền, kể cả khi là "Không"?
- [ ] Chỗ nào ghi "chờ / đang thảo luận" đã có ngày dự kiến chốt? Nếu chỉ ngồi đợi bên kia, hoặc đã quá ngày dự kiến → đưa lên "Vướng mắc".
- [ ] Ngày tháng đúng năm, đúng dạng dd/mm? Mã ticket đủ số, đúng dự án?
