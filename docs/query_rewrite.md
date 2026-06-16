# Bộ Test Case Query Rewrite (Wiki nội bộ – RAG)

## Tổng quan

|Hạng mục |Nội dung                                        |
|---------|------------------------------------------------|
|Đối tượng|Module query rewrite                            |
|Ngôn ngữ |Tiếng Nhật là chính (có lẫn thuật ngữ tiếng Anh)|
|Hình thức|Multi-turn (có lịch sử hội thoại)               |
|Đầu ra   |Một câu, giữ ngôn ngữ gốc, tự đứng độc lập      |

Tiêu chí nghiệm thu: câu sau khi rewrite **hiểu được mà không cần xem lịch sử hội thoại**.

-----

## Nhóm 1: Bổ sung chủ ngữ / tân ngữ bị lược bỏ

### TC-01 Khôi phục chủ ngữ bị lược

- **Lịch sử**: U「経費精算の締め日はいつですか？」/ A「毎月末です。」
- **Câu hỏi hiện tại**: 「承認は誰がしますか？」
- **Rewrite kỳ vọng**: 「経費精算の承認は誰がしますか？」
- **Điểm kiểm thử**: Có lấy được chủ đề trước đó (thanh toán chi phí) làm chủ ngữ không

### TC-02 Khôi phục đối tượng bị lược

- **Lịch sử**: U「有給休暇の申請方法を教えて」/ A「勤怠システムから申請します。」
- **Câu hỏi hiện tại**: 「何日前まで？」
- **Rewrite kỳ vọng**: 「有給休暇は何日前までに申請する必要がありますか？」
- **Điểm kiểm thử**: Có biến mảnh câu rời rạc thành câu hoàn chỉnh không

-----

## Nhóm 2: Giải tham chiếu (chỉ thị từ)

### TC-03 Giải tham chiếu「それ」(cái đó)

- **Lịch sử**: U「VPNの設定マニュアルはどこ？」/ A「社内Wikiの情シスページにあります。」
- **Câu hỏi hiện tại**: 「それMac版もありますか？」
- **Rewrite kỳ vọng**: 「VPNの設定マニュアルのMac版はありますか？」
- **Điểm kiểm thử**: Có thay chỉ thị từ「それ」bằng thực thể cụ thể không

### TC-04 Tham chiếu mơ hồ「あの制度」(chế độ đó)

- **Lịch sử**: U「リモートワーク手当について知りたい」/ A「月5,000円支給されます。」
- **Câu hỏi hiện tại**: 「あの制度って試用期間中でも対象？」
- **Rewrite kỳ vọng**: 「リモートワーク手当は試用期間中の社員も対象ですか？」
- **Điểm kiểm thử**: Có giải được tham chiếu mơ hồ về đúng tên chế độ không

-----

## Nhóm 3: Duy trì chủ đề và lược bỏ (quan trọng nhất)

### TC-05 Câu hỏi ngắn nối tiếp cùng chủ đề

- **Lịch sử**: U「東京オフィスの会議室予約方法は？」/ A「予約システムTeamsから予約します。」
- **Câu hỏi hiện tại**: 「大阪は？」
- **Rewrite kỳ vọng**: 「大阪オフィスの会議室予約方法は？」
- **Điểm kiểm thử**: Với mẫu「Xは？」có kế thừa được vị ngữ bị lược không

### TC-06 Hỏi liên tiếp các thuộc tính

- **Lịch sử**: U「健康診断はいつ実施されますか？」/ A「毎年10月です。」
- **Câu hỏi hiện tại**: 「予約は必要？」
- **Rewrite kỳ vọng**: 「健康診断の予約は必要ですか？」
- **Điểm kiểm thử**: Có giữ chủ đề (khám sức khỏe) khi hỏi thuộc tính mới không

-----

## Nhóm 4: Xử lý thuật ngữ kỹ thuật / biến thể chữ viết

### TC-07 Giữ nguyên thuật ngữ tiếng Anh

- **Lịch sử**: U「authenticationのエラーが出る」/ A「ログを確認してください。」
- **Câu hỏi hiện tại**: 「ログはどこ？」
- **Rewrite kỳ vọng**: 「authenticationのエラーログはどこにありますか？」
- **Điểm kiểm thử**: Có giữ thuật ngữ tiếng Anh ở dạng gốc (không chuyển sang katakana) không — quan trọng cho độ chính xác retrieval

### TC-08 Giữ nguyên từ viết tắt

- **Lịch sử**: U「PRのレビュー依頼はどうやって出す？」/ A「GitHubでreviewerを指定します。」
- **Câu hỏi hiện tại**: 「マージは誰が？」
- **Rewrite kỳ vọng**: 「PRのマージは誰が行いますか？」
- **Điểm kiểm thử**: Có tự ý mở rộng / dịch từ viết tắt (PR) không

-----

## Nhóm 5: Phán đoán không cần rewrite (chống sửa quá tay)

### TC-09 Câu hỏi đã hoàn chỉnh

- **Lịch sử**: U「組織図はどこにありますか？」/ A「人事ポータルにあります。」
- **Câu hỏi hiện tại**: 「2026年度の新しい就業規則の全文はどこで確認できますか？」
- **Rewrite kỳ vọng**: 「2026年度の新しい就業規則の全文はどこで確認できますか？」(giữ nguyên)
- **Điểm kiểm thử**: Có tránh viết lại không cần thiết với câu đã tự đủ nghĩa không (chống over-rewriting)

### TC-10 Phát hiện chuyển chủ đề

- **Lịch sử**: U「経費精算のやり方は？」/ A「経費システムから申請します。」
- **Câu hỏi hiện tại**: 「ところで社員食堂の営業時間は？」
- **Rewrite kỳ vọng**: 「社員食堂の営業時間は何時から何時までですか？」
- **Điểm kiểm thử**: Khi đổi chủ đề có tránh kế thừa nhầm chủ đề cũ không

-----

## Nhóm 6: Khử nhiễu / làm rõ nghĩa

### TC-11 Loại bỏ từ đệm / khẩu ngữ

- **Lịch sử**: (không có / lượt đầu)
- **Câu hỏi hiện tại**: 「えーっと、なんか経費の、領収書って、何ヶ月くらい保管すればいいんでしたっけ？」
- **Rewrite kỳ vọng**: 「経費の領収書は何ヶ月間保管する必要がありますか？」
- **Điểm kiểm thử**: Có bỏ từ đệm (えーっと, なんか) mà vẫn giữ nghĩa không

### TC-12 Sửa lỗi gõ / chính tả

- **Lịch sử**: (không có / lượt đầu)
- **Câu hỏi hiện tại**: 「在宅勤務の申請てどこからやりまふか」
- **Rewrite kỳ vọng**: 「在宅勤務の申請はどこから行いますか？」
- **Điểm kiểm thử**: Có sửa lỗi nhỏ mà không làm đổi nghĩa không

-----

## Nhóm 7: Trường hợp biên (edge case)

### TC-13 Không tự ý đổi văn phong / kính ngữ

- **Lịch sử**: U「議事録のテンプレある？」/ A「共有ドライブにあります。」
- **Câu hỏi hiện tại**: 「英語版もある？」
- **Rewrite kỳ vọng**: 「議事録のテンプレートの英語版はありますか？」
- **Điểm kiểm thử**: Có chỉ làm rõ nghĩa mà không nâng cấp khẩu ngữ thành kính ngữ quá mức không

### TC-14 Câu chứa nhiều ý (cân bằng với ràng buộc một câu)

- **Lịch sử**: (không có / lượt đầu)
- **Câu hỏi hiện tại**: 「入社時の保険手続きと、あと交通費の登録ってどうやる？」
- **Rewrite kỳ vọng**: 「入社時の保険手続きと交通費登録の方法を教えてください。」
- **Điểm kiểm thử**: Có gộp nhiều ý vào một câu tự nhiên mà không mất thông tin không

### TC-15 Tham chiếu xa (cách 3 lượt trở lên)

- **Lịch sử**: U「新製品Xの仕様書ある？」/ A「あります。」/ U「PDFで欲しい」/ A「ダウンロードできます。」
- **Câu hỏi hiện tại**: 「英語版は？」
- **Rewrite kỳ vọng**: 「新製品Xの仕様書の英語版はありますか？」
- **Điểm kiểm thử**: Có truy ngược về chủ đề cách vài lượt để giải tham chiếu không

-----

## Yêu cầu chung cho đầu ra kỳ vọng

Mọi case đều phải thỏa:

- Đầu ra là **một câu**
- **Giữ ngôn ngữ gốc (tiếng Nhật)**, thuật ngữ tiếng Anh giữ nguyên dạng
- **Tự đứng độc lập**, hiểu được mà không cần lịch sử
- **Không thêm / không đổi** ý định gốc của câu hỏi (chống bịa)