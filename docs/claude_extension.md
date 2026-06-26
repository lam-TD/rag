# Báo cáo: Claude Code Extension trong Visual Studio Code

## 1. Giới thiệu tổng quan

Claude Code là công cụ lập trình agentic (agentic coding tool) của Anthropic, hoạt động trong terminal, IDE và môi trường phát triển của lập trình viên. Extension Claude Code cho VS Code cung cấp một **giao diện đồ họa (graphical interface)** tích hợp trực tiếp vào IDE, và đây được Anthropic khuyến nghị là cách sử dụng Claude Code tốt nhất trong VS Code.

Điểm cốt lõi cần hiểu: extension **không phải là một sản phẩm khác** — nó sử dụng cùng một engine Claude Code (cùng model, cùng cấu hình CLAUDE.md, cùng hooks và MCP servers, cùng slash commands và skills) nhưng được "đóng gói" trong một panel biết vị trí con trỏ của bạn và có thể hiển thị diff (so sánh thay đổi) ngay trong giao diện. Extension đóng gói sẵn một bản sao của CLI bên trong nó để phục vụ chat panel.

## 2. Tính năng chính

Với extension, người dùng có thể:

- **Xem lại và chỉnh sửa kế hoạch (plan)** của Claude trước khi chấp nhận
- **Tự động chấp nhận chỉnh sửa (auto-accept edits)** khi chúng được thực hiện
- **@-mention file** với phạm vi dòng cụ thể dựa trên vùng văn bản đang chọn
- **Truy cập lịch sử hội thoại (conversation history)**
- **Mở nhiều hội thoại song song** trong các tab hoặc cửa sổ riêng biệt
- **Xem diff song song (side-by-side)** giữa nội dung gốc và đề xuất thay đổi, kèm quyền chấp nhận/từ chối/yêu cầu chỉnh sửa
- **Quản lý plugin** qua giao diện đồ họa (gõ `/plugins`)
- **Tích hợp Git**: tạo commit, pull request, làm việc đa nhánh
- **Checkpoints (rewind)**: theo dõi chỉnh sửa của Claude và quay lại trạng thái trước đó

## 3. Yêu cầu cài đặt (Prerequisites)

| Yêu cầu | Chi tiết |
|---------|----------|
| Phiên bản VS Code | 1.98.0 trở lên |
| Tài khoản | Bất kỳ gói Claude trả phí nào (Pro, Max, Team, hoặc Enterprise) hoặc tài khoản Claude Console |
| API key | **Không bắt buộc** — đăng nhập bằng tài khoản khi mở extension lần đầu |

Lưu ý: Nếu truy cập Claude qua nhà cung cấp bên thứ ba như Amazon Bedrock hoặc Google Vertex AI, cần cấu hình riêng.

## 4. Cách cài đặt

1. **Cài trực tiếp**: dùng link `vscode:extension/anthropic.claude-code`
2. **Qua Extensions view**: nhấn `Cmd+Shift+X` (Mac) hoặc `Ctrl+Shift+X` (Windows/Linux), tìm "Claude Code" và nhấn **Install**
3. **Các IDE fork khác** (Cursor, Devin Desktop, Kiro): tìm "Claude Code" trong Extensions view hoặc cài từ Open VSX registry

Nếu extension không xuất hiện sau khi cài, khởi động lại VS Code hoặc chạy "Developer: Reload Window" từ Command Palette.

## 5. Bắt đầu sử dụng

**Bước 1 — Mở panel Claude Code**: Biểu tượng Spark (✱) đại diện cho Claude Code. Có thể mở qua:
- Editor Toolbar (góc trên bên phải editor, hiển thị khi có file đang mở)
- Activity Bar (thanh bên trái)
- Command Palette (`Cmd/Ctrl+Shift+P`, gõ "Claude Code")
- Status Bar (góc dưới bên phải)

**Bước 2 — Đăng nhập**: Lần đầu mở panel sẽ hiện màn hình đăng nhập. Nhấn **Sign in** và hoàn tất ủy quyền trên trình duyệt.

**Bước 3 — Gửi prompt**: Yêu cầu Claude giải thích code, debug, hoặc chỉnh sửa. Claude tự động thấy văn bản bạn đang chọn. Nhấn `Option+K` (Mac) / `Alt+K` (Windows/Linux) để chèn @-mention với số dòng.

**Bước 4 — Xem lại thay đổi**: Khi Claude muốn sửa file, nó hiển thị so sánh song song và xin phép. Bạn có thể chấp nhận, từ chối hoặc yêu cầu khác.

## 6. Tùy biến quy trình làm việc

- **Vị trí panel**: kéo thả để đặt Claude ở secondary sidebar (phải), primary sidebar (trái), hoặc editor area (tab cạnh file)
- **Nhiều hội thoại**: dùng "Open in New Tab" hoặc "Open in New Window" để chạy song song
- **Chế độ terminal**: nếu thích giao diện kiểu CLI, bật cài đặt **Use Terminal**
- **Permission modes**: normal (hỏi trước mỗi hành động), Plan (mô tả và chờ duyệt), auto-accept (sửa không hỏi)

## 7. So sánh Extension và CLI

| Tính năng | CLI | Extension VS Code |
|-----------|-----|-------------------|
| Commands và skills | Toàn bộ | Một phần (gõ `/` để xem) |
| Cấu hình MCP server | Có | Một phần (thêm qua CLI; quản lý bằng `/mcp` trong chat panel) |
| Checkpoints | Có | Có |
| Bash shortcut `!` | Có | Không |
| Tab completion | Có | Không |

Extension và CLI **chia sẻ cùng lịch sử hội thoại**. Để tiếp tục hội thoại của extension trong CLI, chạy `claude --resume` trong terminal.

Lưu ý quan trọng: cài extension **không** thêm `claude` vào PATH của shell. Extension đóng gói bản sao CLI riêng cho chat panel; muốn gõ `claude` trong terminal cần cài CLI standalone riêng.

## 8. Tích hợp nâng cao

**MCP (Model Context Protocol)**: cho Claude truy cập công cụ, cơ sở dữ liệu và API bên ngoài. Thêm server bằng `claude mcp add` trong terminal tích hợp; quản lý bằng `/mcp` trong chat panel.

**Tự động hóa Chrome**: kết nối Claude với trình duyệt Chrome để test web app, debug bằng console log. Gõ `@browser` kèm yêu cầu (cần extension Claude in Chrome v1.0.36+).

**IDE MCP server tích hợp**: khi extension hoạt động, nó chạy một local MCP server (tên `ide`) để mở diff trong trình xem native của VS Code, đọc vùng chọn cho @-mention, và thực thi cell Jupyter. Server này bind vào `127.0.0.1` ở cổng ngẫu nhiên, không truy cập được từ máy khác, và mỗi lần kích hoạt sinh token xác thực ngẫu nhiên mới.

## 9. Cấu hình

Extension có hai loại cài đặt:

- **Extension settings** (trong VS Code): điều khiển hành vi trong VS Code — `useTerminal`, `initialPermissionMode`, `preferredLocation`, `autosave`, `respectGitIgnore`, v.v.
- **Claude Code settings** (`~/.claude/settings.json`): chia sẻ giữa extension và CLI — dùng cho allowed commands, biến môi trường, hooks và MCP servers

## 10. Bảo mật và quyền riêng tư

Code của bạn được giữ riêng tư. Claude Code xử lý code để hỗ trợ nhưng **không dùng để huấn luyện model**.

Khuyến nghị khi làm việc với code không tin cậy:
- Bật VS Code Restricted Mode cho workspace không tin cậy
- Dùng chế độ duyệt thủ công thay vì auto-accept
- Xem kỹ các thay đổi trước khi chấp nhận

## 11. Xử lý sự cố thường gặp

- **Extension không cài được**: kiểm tra VS Code ≥ 1.98.0, quyền cài extension
- **Không thấy biểu tượng Spark**: cần mở một file (chỉ mở folder là không đủ), kiểm tra phiên bản, reload window, tắt extension AI xung đột (Cline, Continue...)
- **`Cmd+Esc` không hoạt động trên macOS**: trên macOS Tahoe trở lên, shortcut Game Overlay của hệ thống chiếm phím này — cần tắt trong System Settings
- **Claude không phản hồi**: kiểm tra kết nối internet, thử hội thoại mới, hoặc chạy `claude` trong terminal để xem lỗi chi tiết

## 12. So sánh với Cline

Cline (trước đây tên là Claude Dev) là một trong những extension lập trình agentic mã nguồn mở phổ biến nhất cho VS Code, thường được đặt cạnh Claude Code khi lựa chọn công cụ. Cline được phát hành lần đầu năm 2024 bởi Saoud Rizwan, cấp phép theo Apache-2.0, và tính đến đầu năm 2026 đã vượt mốc vài triệu lượt cài đặt cùng hàng chục nghìn sao trên GitHub.

### Khác biệt cốt lõi

Sự khác biệt nền tảng nằm ở **kiến trúc và mô hình model**. Claude Code là agent terminal-native được tối ưu riêng cho model Claude, còn Cline là một extension VS Code "đa model" — cho phép mang theo API key của bất kỳ nhà cung cấp nào (Claude, GPT, Gemini, Azure, hoặc model local qua Ollama). Claude Code đánh đổi tính linh hoạt để lấy tốc độ và khả năng điều phối; Cline đánh đổi tốc độ để lấy sự minh bạch và tự do lựa chọn model.

### Bảng so sánh

| Tiêu chí | Claude Code (VS Code Extension) | Cline |
|----------|--------------------------------|-------|
| Nhà phát triển | Anthropic | Cline (Saoud Rizwan), mã nguồn mở |
| Giấy phép | Độc quyền (proprietary) | Apache-2.0 (mã nguồn mở) |
| Model hỗ trợ | Chỉ model Claude (tối ưu chuyên biệt) | Đa model: Claude, GPT, Gemini, Azure, Ollama (local)... |
| Mô hình chi phí | Cần gói Claude trả phí (Pro/Max/Team/Enterprise) | Extension miễn phí; trả tiền theo lượng dùng (BYOK) hoặc credit hosted của Cline |
| Chi phí điển hình | Theo gói thuê bao Claude | Phụ thuộc model và mức dùng; thường vài USD đến hơn 100 USD/tháng |
| Chế độ làm việc | Normal / Plan / Auto-accept | Plan Mode / Act Mode |
| Phê duyệt hành động | Có thể bật auto-accept | Human-in-the-loop — duyệt từng chỉnh sửa và lệnh terminal |
| Xem diff | Side-by-side trong IDE | Diff-based, hiển thị thay đổi trước khi áp dụng |
| Hỗ trợ MCP | Có | Có |
| Tự động hóa trình duyệt | Qua Claude in Chrome | Có browser integration tích hợp |
| Checkpoints / Rewind | Có | Có (checkpoint snapshots để rollback) |
| Chia sẻ với CLI | Có (cùng lịch sử hội thoại) | Có CLI riêng (Cline CLI 2.0, headless cho CI/CD) |
| Nền tảng IDE | VS Code và các fork (Cursor, Kiro...) | VS Code, JetBrains, Cursor, Windsurf, Zed, Neovim |

### Khi nào nên chọn công cụ nào

**Chọn Claude Code** nếu bạn ưu tiên hiệu năng tối đa với model Claude, muốn engine được tối ưu chuyên biệt, khả năng điều phối nâng cao (như Agent Teams) và auto-compaction cho phiên làm việc dài. Phù hợp với lập trình viên làm việc sâu với hệ sinh thái Anthropic.

**Chọn Cline** nếu bạn cần **tự do lựa chọn model** (kể cả model local để bảo mật dữ liệu), muốn kiểm soát rõ ràng chi phí theo từng lệnh gọi API, cần phê duyệt thủ công mọi hành động của AI, hoặc muốn tránh thuê bao cố định. Phù hợp với lập trình viên quan tâm chi phí và các nhóm đã có hợp đồng model sẵn.

Điểm chung: cả hai đều là agent agentic thực thụ (chứ không phải công cụ autocomplete như GitHub Copilot), đều hỗ trợ MCP, diff review, checkpoints, và đều có chế độ headless cho CI/CD. Trên thực tế nhiều lập trình viên dùng cả Cline lẫn Claude Code tùy theo tác vụ và ngân sách.

> *Lưu ý: Thông tin về Cline (giá, số lượt cài, tính năng) được tổng hợp từ các nguồn bên thứ ba và có thể thay đổi theo thời gian. Nên kiểm tra trang chính thức cline.bot để có dữ liệu mới nhất.*

## 13. Kết luận

Claude Code extension cho VS Code mang sức mạnh của công cụ lập trình agentic vào trong IDE quen thuộc, với điểm mạnh nổi bật là việc xem lại diff trực quan, @-mention theo vùng chọn, lịch sử phiên có tab, và tích hợp MCP. Trên thực tế, nhiều lập trình viên sử dụng **cả hai** — extension cho việc xem xét thay đổi trực quan và CLI (mở trong terminal tích hợp của VS Code) cho các tính năng power-user.

---

*Nguồn tham khảo: Tài liệu chính thức Claude Code — https://code.claude.com/docs/en/vs-code*
