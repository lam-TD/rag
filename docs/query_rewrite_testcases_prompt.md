# Prompt: Sinh bộ test case Query Rewrite từ tài liệu

## Vai trò

Bạn là kỹ sư QA chuyên về hệ thống RAG. Nhiệm vụ của bạn là dựa vào **tài liệu được cung cấp** để thiết kế một bộ test case kiểm thử module **query rewrite** (viết lại câu truy vấn của người dùng).

## Bối cảnh hệ thống

- Module query rewrite nằm trong một hệ thống RAG dùng cho **wiki nội bộ công ty**.
- Hệ thống là **multi-turn** (có lịch sử hội thoại nhiều lượt).
- Ngôn ngữ chính của câu hỏi là **tiếng Nhật**, có thể lẫn thuật ngữ tiếng Anh.
- Đầu ra của query rewrite phải là: **một câu duy nhất**, **giữ nguyên ngôn ngữ gốc** của câu hỏi, **tự đứng độc lập** (hiểu được mà không cần xem lịch sử), và **không thêm/đổi ý định gốc**.

## Mục tiêu của query rewrite (để thiết kế test bám sát)

1. Bổ sung chủ ngữ / tân ngữ bị lược bỏ dựa trên lịch sử hội thoại.
1. Giải tham chiếu (chỉ thị từ như「それ」「あの〜」về thực thể cụ thể).
1. Duy trì chủ đề khi người dùng hỏi nối tiếp ngắn gọn (ví dụ「大阪は？」).
1. Khử nhiễu, sửa lỗi gõ, loại bỏ từ đệm, làm rõ nghĩa.
1. Giữ nguyên thuật ngữ kỹ thuật / từ viết tắt tiếng Anh (không dịch sang katakana) để tối ưu retrieval.
1. Không viết lại quá tay khi câu đã hoàn chỉnh (chống over-rewriting).
1. Phát hiện chuyển chủ đề để không kế thừa nhầm ngữ cảnh cũ.

## Yêu cầu thực hiện

1. **Đọc kỹ tài liệu được cung cấp** và xác định các chủ đề, thực thể, thuật ngữ, quy trình, con số quan trọng có trong đó.
1. **Mỗi test case phải bắt nguồn từ nội dung có thật trong tài liệu** — câu hỏi và đáp án trong lịch sử hội thoại phải phản ánh thông tin thực tế của tài liệu, không bịa thông tin ngoài tài liệu.
1. Thiết kế test case phủ đủ các nhóm sau (mỗi nhóm ít nhất 2 case):
- Bổ sung chủ ngữ / tân ngữ bị lược
- Giải tham chiếu (chỉ thị từ)
- Duy trì chủ đề khi hỏi nối tiếp
- Xử lý thuật ngữ kỹ thuật / từ viết tắt
- Không cần rewrite (chống over-rewriting)
- Khử nhiễu / sửa lỗi / làm rõ
- Trường hợp biên: câu nhiều ý, tham chiếu xa (≥3 lượt), chuyển chủ đề
1. Câu hỏi, lịch sử hội thoại và kết quả rewrite kỳ vọng viết bằng **tiếng Nhật**. Phần mô tả mục đích và điểm kiểm thử viết bằng **tiếng Việt**.
1. Mỗi case phải có **điểm kiểm thử rõ ràng** nêu rõ đang kiểm tra năng lực gì.

## Định dạng đầu ra (Markdown)

Xuất ra Markdown theo đúng cấu trúc sau:

```markdown
# Bộ Test Case Query Rewrite – [Tên tài liệu]

## Tổng quan
| Hạng mục | Nội dung |
|---|---|
| Tài liệu nguồn | ... |
| Số lượng case | ... |
| Ngôn ngữ | Tiếng Nhật (có lẫn thuật ngữ tiếng Anh) |
| Hình thức | Multi-turn |

## Nhóm [N]: [Tên nhóm]

### TC-[số] [Tên ngắn của case]
- **Lịch sử**: U「...」/ A「...」   ← (để trống nếu là lượt đầu)
- **Câu hỏi hiện tại**: 「...」
- **Rewrite kỳ vọng**: 「...」
- **Trích từ tài liệu**: [phần/mục nào của tài liệu làm căn cứ]
- **Điểm kiểm thử**: [đang kiểm tra năng lực gì]
```

Kết thúc bằng mục **Yêu cầu chung cho đầu ra kỳ vọng**:

- Đầu ra là một câu
- Giữ ngôn ngữ gốc (tiếng Nhật), thuật ngữ tiếng Anh giữ nguyên dạng
- Tự đứng độc lập, hiểu được mà không cần lịch sử
- Không thêm / không đổi ý định gốc của câu hỏi

## Lưu ý quan trọng

- **Tuyệt đối không bịa thông tin** không có trong tài liệu. Mọi đáp án trong lịch sử hội thoại phải truy được về nội dung tài liệu.
- Kết quả rewrite kỳ vọng phải **tự nhiên, đúng ngữ pháp tiếng Nhật**, và phản ánh đúng những gì một người dùng thực sự sẽ hỏi.
- Ưu tiên các tình huống **gần với cách nhân viên thật sự tra cứu wiki nội bộ**.

-----

**Tài liệu để thiết kế test case:**

[Dán nội dung tài liệu vào đây]