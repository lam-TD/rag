# Claude (Anthropic) — Báo cáo provider

> **Vị trí trong chuỗi:** 1 file trong loạt báo cáo AI provider (xem [README.md](README.md) — trang chủ, quy ước & 7 tiêu chí chung).
> Provider này: **Claude — trọng tâm Claude Code.**
>
> **Tài liệu chia 3 lớp** để sếp đọc nhanh và phân biệt rõ:
> - **Lớp A — Đã xác minh:** dữ kiện có nguồn (`[FACT]`, link ở §Nguồn). Verify web 2026-06-20.
> - **Lớp B — Góc nhìn người viết:** nhận định (`[INFERENCE]`/ý kiến) — *không phải dữ kiện*, có thể tranh luận.
> - **Lớp C — Cần sếp phản hồi:** câu hỏi mở để quyết phạm vi triển khai.
>
> Quy ước: `[FACT]` có link · `[INFERENCE]` kèm giả định + điều kiện đảo ngược · THẬT/GIẢ ĐỊNH cho bối cảnh cty.

---

# LỚP A — THÔNG TIN ĐÃ XÁC MINH

> Mục này là **dữ kiện** — các khẳng định quan trọng đều có nguồn `[FACT]` (§Nguồn). Tham chiếu 2026-06-20.

## A1. Claude & Claude Code là gì

- **Claude** — nền tảng AI của Anthropic, dùng qua nhiều bề mặt (chat, code, agent cho non-dev, API).
- **Claude Code** — `[FACT]` "công cụ lập trình agentic đọc codebase, sửa file, chạy lệnh, tích hợp với công cụ dev"; hiểu toàn bộ codebase, làm việc xuyên nhiều file và công cụ [S3].

## A2. Bản đồ sản phẩm Claude

| Sản phẩm / bề mặt | Là gì (ngắn) | Người dùng tự nhiên |
|---|---|---|
| **Claude apps (Chat)** | Trò chuyện web/desktop/mobile, có Projects & Artifacts | Mọi phòng ban |
| **Claude Code** ⭐ | Agent lập trình chạy trong terminal/IDE/desktop/web | Dev |
| **Cowork** | "Sức mạnh Claude Code cho công việc tri thức" — agent tự làm việc nhiều bước (nghiên cứu, soạn tài liệu, xử lý file) cho người *không* code, chạy trên app desktop [S5] | HR, kinh doanh, phân tích |
| **Claude in Chrome** | Tiện ích trình duyệt, thao tác/đọc trên web | Mọi phòng ban |
| **Claude Design** | Tính năng có trong gói Pro trở lên [S1] | Thiết kế/sản phẩm |
| **Agent SDK / API** | Để dev *tự build* sản phẩm tích hợp Claude | Dev / sản phẩm |

`[FACT]` Cowork = "same capability [as Claude Code] with a simplified experience, designed for non-technical knowledge work"; ra đời vì các nhóm phi kỹ thuật (Marketing, Data) đã bỏ chat để chuyển sang Claude Code [S5].

## A3. Claude Code — bề mặt & năng lực

**Bề mặt** `[FACT]` (cùng engine, dùng chung `CLAUDE.md`/cài đặt/MCP) [S3]:
- **Terminal (CLI)** — macOS / Linux / WSL / Windows
- **VS Code / Cursor** (extension) và **JetBrains** (IntelliJ, PyCharm, WebStorm…)
- **App desktop** (macOS, Windows, Windows ARM64)
- **Web** — claude.ai/code (task dài chạy trên hạ tầng Anthropic; có cả trên iOS app)

**Năng lực chính** `[FACT]` [S3]:
- Build feature / fix bug đa file (tự lập kế hoạch → viết code → kiểm chứng)
- Tự động hoá việc lặp: viết test, sửa lint, giải merge conflict, cập nhật dependency, release notes
- Làm việc trực tiếp với git: commit, tạo branch, mở pull request
- Kết nối công cụ ngoài qua **MCP**
- Tuỳ biến qua `CLAUDE.md` / skills / hooks; chạy nhiều sub-agent song song
- Tích hợp CI/CD (GitHub Actions, GitLab), review PR tự động, định tuyến task từ Slack

## A4. Hệ sinh thái mở rộng

> Một số dùng chung toàn nền tảng, không riêng Claude Code.

| Tính năng | Là gì | Ghi chú |
|---|---|---|
| **Schedule / Routines** | Tự động hoá Claude Code: cấu hình 1 lần (prompt + repo + connector) rồi **chạy theo lịch** (giờ/đêm/tuần), theo API call, hoặc theo sự kiện [S14] | Chạy trên hạ tầng Anthropic — máy tắt vẫn chạy |
| **Dispatch** | Giao task cho Claude **từ điện thoại**; Claude làm việc trên *máy tính của bạn* rồi báo khi xong [S15] | Thuộc Cowork/mobile; có thể thành scheduled |
| **Connector** | Kết nối Claude tới Google Drive, Gmail, Slack, DocuSign… [S16] | Catalog trong directory hợp nhất |
| **Skills** | Đóng gói quy trình / best-practice / tri thức nội bộ để Claude làm việc nhất quán; chuẩn mở; directory đối tác (Notion, Canva, Figma, Atlassian…) [S16][S18] | Quản trị cấp tổ chức cho admin |
| **Plugin** | Gói gộp **skills + connectors + sub-agents** thành 1 bộ cài sẵn theo vai trò/team/cty; có marketplace (Knowledge Work mặc định; thêm Financial/Legal hoặc từ GitHub repo) [S16][S17] | "Cài 1 phát chạy ngay" |

`[FACT]` Cả ba — skills, connectors, plugins — gom trong **một directory hợp nhất**; skills/plugins là **chuẩn mở (open protocol)**, đối tác (Box, Thomson Reuters…) đã ship gói riêng [S16].

## A5. Giá & cơ chế giới hạn/reset

**Gói thuê bao (USD/người/tháng) — `[FACT]` Claude Code có trong MỌI gói [S1][S7]:**

| Gói | Giá | Ghi chú |
|---|---|---|
| **Free** | $0 | Chat + Claude Code mức cơ bản |
| **Pro** | $20/th ($17 trả năm) | + Cowork, Claude Design, projects không giới hạn |
| **Max 5x** | $100/th | 5× usage so với Pro [S2] |
| **Max 20x** | $200/th | 20× usage so với Pro [S2] |
| **Team (standard)** | $20/ghế (năm) · $25 (tháng) | + enterprise search, SSO, admin controls |
| **Team (premium)** | $100/ghế (năm) · $125 (tháng) | 5× usage so với standard |
| **Enterprise** | $20/ghế **+ usage tính theo model & tác vụ ở API rates** | + SCIM, audit logs, ZDR (đủ điều kiện), HIPAA-ready [S6] |

**API** (trả theo token, khi tự build): giá theo model — chưa lấy chi tiết, bổ sung khi cần.

**Cơ chế giới hạn & reset** `[FACT]` [S12][S13]:
- **Không có con số token cố định công bố** cho từng gói — giới hạn đo bằng token nội bộ nhưng phụ thuộc model/effort/độ phức tạp, nên biểu thị bằng **bội số + cửa sổ thời gian**.
- **Hai tầng reset:** phiên **5 giờ** (reset mỗi 5 tiếng) + giới hạn **tuần** (reset mốc cố định hằng tuần). Pro: 1 giới hạn tuần; Max: 2 (mọi model + Sonnet). Enterprise: pool tổ chức, rolling window.
- Theo dõi tại **Settings > Usage**.

| | Pro $20 | Max 5x $100 | Max 20x $200 |
|---|---|---|---|
| Usage tương đối | 1× | **5× Pro** | **20× Pro** |
| Con số token cụ thể | không công bố | không công bố | không công bố |
| Giới hạn tuần | 1 (mọi model) | 2 (mọi model + Sonnet) | 2 (mọi model + Sonnet) |

## A6. Bảo mật & dữ liệu

- `[FACT]` **Zero Data Retention (ZDR)** cho Claude Code: prompt + phản hồi xử lý thời gian thực, **không lưu** sau khi trả kết quả (trừ khi luật yêu cầu / xử lý lạm dụng) [S4].
- `[FACT]` ZDR **chỉ có trên Claude for Enterprise**, tài khoản đủ điều kiện, **không bật từ admin settings** — phải liên hệ Anthropic/sales; **không nằm trong Enterprise chuẩn** [S4].
- `[FACT]` **Phạm vi ZDR hẹp:** chỉ bao *Claude Code inference*. **KHÔNG** bao Chat trên claude.ai, **Cowork**, tích hợp/**MCP bên thứ ba**, metadata analytics, quản lý seat — những thứ này theo chính sách lưu trữ chuẩn [S4].
- `[FACT]` Khi bật ZDR, **một số tính năng bị tắt** (vì cần lưu trữ): Claude Code on Web, Cloud sessions (Desktop), Artifacts, gửi `/feedback`; ngoài ra **Fable 5 không khả dụng** dưới ZDR [S4].
- `[FACT]` ZDR bật **theo từng tổ chức** (org mới phải bật lại); nếu phiên bị gắn cờ vi phạm Usage Policy, dữ liệu có thể bị giữ tới **2 năm** [S4].
- `[FACT]` Enterprise (kể cả không ZDR): custom data retention, audit logs, SSO/SCIM, IP allowlisting, HIPAA-ready [S1][S6].
- `[FACT]` **Rủi ro vận hành ghi nhận** [S9]: prompt injection (lệnh ẩn trong file/web/tool); agent chạy lệnh/sửa file; **MCP bên thứ ba Anthropic không audit**; WebDAV trên Windows có thể vượt phân quyền.
- `[FACT]` **Phòng vệ tích hợp** [S9]: mặc định read-only + xin phép; chỉ ghi trong thư mục dự án; phát hiện command-injection (fail-closed); lệnh mạng không auto-approve; sandbox filesystem/mạng; bản web chạy VM cô lập + audit log; chứng nhận **SOC 2 Type 2, ISO 27001**.
- `[FACT]` **Người dùng chịu trách nhiệm review code & lệnh trước khi duyệt** — agent chỉ có quyền được cấp [S9].

## A7. Bản quyền & sở hữu code tạo sinh

- `[FACT]` **Sở hữu output:** khách hàng *giữ quyền sở hữu* output tạo ra [S8].
- `[FACT]` **Bồi thường bản quyền (indemnity):** Anthropic *bảo vệ khách hàng* trước khiếu nại bên thứ ba (bản quyền / bằng sáng chế / nhãn hiệu / bí mật KD) cho việc dùng dịch vụ/output hợp lệ, và trả dàn xếp/phán quyết được duyệt [S8].
- `[FACT]` Indemnity thuộc **Commercial Terms** → áp dụng **Team, Enterprise, API** [S8][S10].
- `[FACT]` **Consumer Terms (Free/Pro/Max) KHÔNG có** điều khoản indemnity bảo vệ người dùng: Mục 4 chỉ *chuyển quyền sở hữu output* cho người dùng; Mục 11 là indemnity **ngược** (người dùng bồi thường Anthropic) [S11]. → Pro/Max **không** được Anthropic bảo vệ trước khiếu nại IP bên thứ ba. *(Nên để Legal xác nhận diễn giải trước khi dùng làm tiêu chí mua hàng.)*
- `[FACT]` **Loại trừ indemnity (Commercial Terms §K.3)** [S10]: không áp dụng khi khiếu nại đến từ — khách *sửa đổi* output; *kết hợp* output với công nghệ ngoài Anthropic; từ prompt/dữ liệu khách cấp; dùng theo cách biết là xâm phạm quyền người khác; **thực hành sáng chế chứa trong Output**; **vi phạm nhãn hiệu do dùng Output trong thương mại**. (Nghĩa vụ chung còn loại trừ phần phát sinh từ gian lận / cố ý / vi phạm luật / vi phạm hợp đồng [S8].)

---

# LỚP B — GÓC NHÌN NGƯỜI VIẾT

> Đây là **nhận định**, không phải dữ kiện — sếp có thể phản biện. Mỗi điểm tựa trên Lớp A.

## B1. Điều đáng chú ý

- `[INFERENCE]` **Cowork là cầu nối cho non-dev.** Cowork = engine Claude Code đóng gói cho người không code (đã xác nhận, A2) → HR/kinh doanh "hưởng sức mạnh Claude Code" mà không cần CLI. *Điều kiện đảo ngược:* Cowork không đủ năng lực thực tế cho việc của họ.
- `[INFERENCE]` **Hệ sinh thái mở có thể là lý do chọn lớn hơn cả giá.** Skills/Plugin/Connector + directory hợp nhất cho phép cty *đóng gói quy trình riêng* và *phân phối nội bộ* — thứ công cụ chỉ-chat không có. Với cty đa phòng ban, đây là khác biệt chiến lược. *Điều kiện đảo ngược:* cty chỉ cần hỏi-đáp đơn lẻ, không có quy trình lặp để đóng gói.
- `[INFERENCE]` **Một engine, nhiều bề mặt** (CLAUDE.md/MCP dùng chung) → cấu hình 1 lần dùng được khắp terminal/IDE/desktop/web, giảm chi phí học lại.

## B2. Phù hợp công ty ở đâu (ánh xạ đối tượng → bề mặt)

`[INFERENCE]` Mỗi nhóm dùng *bề mặt khác nhau* của cùng năng lực Claude:

| Phòng ban | Bề mặt phù hợp | Ví dụ công việc tối ưu |
|---|---|---|
| **Dev** | Claude Code (CLI/IDE), API, Agent SDK | Đọc/sửa codebase, viết test, fix bug, review, tự động hoá |
| **HR** | Chat + Projects, Cowork | Soạn JD, tóm tắt CV, trả lời chính sách nội bộ, dựng tài liệu |
| **Kinh doanh** | Chat + Projects, Cowork, Claude in Chrome | Soạn email/đề xuất, tóm tắt cuộc gọi, phân tích đối thủ, ghi chú CRM |

`[INFERENCE]` **Gói khởi đầu gợi ý:** đa số phòng ban dùng tool sẵn → **Team standard $20/ghế**; **Pro $20** để thử cá nhân; lên **Enterprise** khi cần ZDR/kiểm soát bảo mật. *Điều kiện đảo ngược:* dev dùng Claude Code nặng → Max/Team premium; hướng tự-build → tính theo API.

## B3. Lo ngại / rủi ro cần cân nhắc

- `[INFERENCE]` **Bảo hộ pháp lý IP đẩy về Team/Enterprise/API.** Đã rà: Consumer Terms (Pro/Max) không có indemnity (A7) → các gói này không được Anthropic bảo vệ trước khiếu nại IP. Nếu cty coi rủi ro bản quyền của code tạo sinh là đáng kể → buộc dùng Team/Enterprise/API, và nên để Legal xác nhận. *Điều kiện đảo ngược:* Legal đánh giá rủi ro IP là thấp/không liên quan tới use-case của cty.
- `[INFERENCE]` **Yêu cầu bảo mật cao đẩy về Enterprise — nhưng ZDR không phải "viên đạn bạc".** Nếu cty hạn chế gửi mã nguồn ra dịch vụ ngoài, cần đối chiếu chính sách nội bộ. Enterprise + ZDR đáp ứng *không lưu inference của Claude Code*, **nhưng không** giải quyết trường hợp cấm *xử lý* dữ liệu bên ngoài hoàn toàn, và **không** bao Chat/Cowork/MCP bên thứ ba (A6). *Điều kiện đảo ngược:* chính sách nội bộ chỉ cấm "lưu trữ" chứ không cấm "xử lý".
- `[INFERENCE]` **Agent chạy lệnh ⇒ cần quy trình, không "bật là xong".** Prompt injection + thực thi lệnh (A6) đòi hỏi review trước khi duyệt + môi trường cô lập (VM/dev container), nhất là khi xử lý nội dung không tin cậy.
- `[INFERENCE]` **Khó dự toán trước.** Không có hạn mức token công bố (A5) → không thể tính "gói nào đủ" trên giấy; bắt buộc pilot + theo dõi Settings > Usage.
- **THẬT/GIẢ ĐỊNH:** giá là **USD/thị trường US** — VN có thể khác; cần kiểm trước khi báo số cho sếp.
- `[INFERENCE]` HR/kinh doanh **không** dùng Claude Code (CLI) trực tiếp — phải đi qua Cowork/Chat; đừng hứa "ai cũng dùng Claude Code" theo nghĩa đen.

## B4. Trải nghiệm cá nhân

> Trải nghiệm trực tiếp của người viết (chủ quan, không phải số liệu chuẩn) — bổ sung "chất" thực tế cho dữ kiện ở Lớp A.

**Theo gói đã dùng (cảm nhận về usage/token):**
- **Free** — rất giới hạn, nhanh hết token; chỉ đủ dùng thử.
- **Pro** — hợp việc nhẹ, code ít phức tạp; nhưng làm code thì token vẫn nhanh hết.
- **Max 5x** — hợp code và tác vụ phức tạp, chạy được nhiều sub-agent song song.

→ Khớp với A5 (không có hạn mức token in sẵn — mức "đủ" chỉ rõ khi dùng thật). Với công việc code thực sự, trải nghiệm cá nhân **nghiêng về Max hơn Pro**, đúng với điều kiện đảo ngược đã nêu ở B2/B3.

**Theo sản phẩm:**
- **Chat** — tìm hiểu kiến thức mới (*có lưu ý nguy cơ ảo giác / hallucination*); soạn tài liệu như PRD rồi chuyển sang Claude Code làm tiếp.
- **Cowork** — việc không liên quan code: soạn CV, soạn báo cáo (vd khung đánh giá năng lực).
- **Claude Code** —
  - Tạo **blog cá nhân** (kết hợp Claude Design cho UI).
  - Tạo **thư viện tổng hợp kiến thức từ sách** (kết hợp Claude Design cho UI).
  - **Rèn tư duy**: thiết lập quy tắc trao đổi, luyện tư duy thiết kế hệ thống + phản biện.
- **Claude Design** — thiết kế blog; tạo infographic để tiếp thu kiến thức nhanh hơn.

**Hệ sinh thái (Scheduled / Routines đang dùng thật):**
- Nhắc sự kiện sắp đến (Google Calendar).
- Kiểm tra email, LinkedIn.
- Tổng hợp xu thế công nghệ (vd top 10 GitHub repo).

**Ví dụ thành quả cụ thể:**
- Blog cá nhân — https://lam-td.github.io/my-blog/
- Thư viện kiến thức — https://my-blog-j3y8.vercel.app/

> _Tự nhắc — bổ sung/xoá dòng này trước khi gửi (để cân bằng, tránh giống quảng cáo):_ nó giúp **nhanh hơn ở đâu** (một ước lượng cụ thể); chỗ **chưa tốt / gây khó chịu**; **có phải sửa nhiều** code nó tạo ra không; **giá trị thực** so với cách làm cũ.

> Phần thuyết phục nhất — bằng chứng thực tế, không phải tính năng trên giấy. Dàn ý cần trả lời:
> 1. Đã dùng Claude Code cho **công việc nào**?
> 2. Một **ví dụ thành quả cụ thể** (repo / đoạn code / tài liệu…).
> 3. Nó giúp **nhanh hơn ở đâu**?
> 4. Nó làm **chưa tốt / gây khó chịu** ở đâu?
> 5. Có phải **sửa nhiều** code do nó tạo ra không?
> 6. So với cách làm bình thường, **giá trị thực tế** ra sao?

## B5. Đề xuất cách ra quyết định

`[INFERENCE]` Chưa nên chốt "chọn gói nào" — thiếu số liệu cty (Lớp C). Thay vào đó:
- **Pilot có đo:** chọn 2–3 tác vụ thật/phòng ban, đo thời gian *trước* (baseline) và *sau*, báo delta thay vì cảm tính.
- Gợi ý: dev — fix bug/viết test; HR — soạn JD/tóm tắt CV; kinh doanh — soạn đề xuất/email.
- Sau pilot mới chọn gói theo số người × mức dùng thực tế (+ cân trục bảo mật/pháp lý ở B3).

---

# LỚP C — CÂU HỎI CẦN SẾP PHẢN HỒI

> Trả lời 5 nhóm này sẽ thu hẹp được phạm vi và cho phép chốt đề xuất.

1. **Mục tiêu:** tối ưu năng suất **dev**, phổ cập AI **toàn công ty**, hay cả hai?
2. **Đối tượng:** những phòng ban nào sẽ dùng, mỗi nơi bao nhiêu người?
3. **Ngân sách:** định hướng chi /người/tháng (để khoanh vùng Pro/Team/Max/Enterprise)?
4. **Dữ liệu & bảo mật:** có ràng buộc gửi mã nguồn/tài liệu ra dịch vụ ngoài không? Có cần ZDR và/hoặc bảo hộ bản quyền (indemnity) không? → quyết định có buộc Enterprise hay không.
5. **Mức độ triển khai:** chạy **pilot** trước hay rollout luôn? Một provider thống nhất hay chấp nhận đa provider theo phòng ban? Dùng gói thuê bao (tool sẵn) hay hướng API (tự build)?

---

## Kết luận

Tôi chưa đề xuất lựa chọn gói hoặc rollout ở thời điểm hiện tại. Bước tiếp theo là xác nhận phạm vi với cấp trên; sau đó mới đào sâu use case, phương án triển khai, chi phí và pilot tương ứng.

## Nguồn

> Truy xuất 2026-06-20.

- **[S1]** Plans & Pricing — https://claude.com/pricing
- **[S2]** What is the Max plan? — https://support.claude.com/en/articles/11049741-what-is-the-max-plan
- **[S3]** Claude Code — Overview (docs) — https://code.claude.com/docs/en/overview
- **[S4]** Zero data retention (Claude Code) — https://code.claude.com/docs/en/zero-data-retention
- **[S5]** Claude Cowork — https://claude.com/product/cowork · https://www.anthropic.com/product/claude-cowork
- **[S6]** What is the Enterprise plan? — https://support.claude.com/en/articles/9797531-what-is-the-enterprise-plan
- **[S7]** Use Claude Code with your Pro or Max plan — https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan
- **[S8]** Expanded legal protections & API improvements — https://www.anthropic.com/news/expanded-legal-protections-api-improvements
- **[S9]** Claude Code — Security (docs) — https://code.claude.com/docs/en/security
- **[S10]** Commercial Terms of Service (Team/Enterprise/API) — https://www.anthropic.com/legal/commercial-terms
- **[S11]** Consumer Terms (Free/Pro/Max) — https://www.anthropic.com/legal/consumer-terms
- **[S12]** How do usage and length limits work? — https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work
- **[S13]** Models, usage, and limits in Claude Code — https://support.claude.com/en/articles/14552983-models-usage-and-limits-in-claude-code
- **[S14]** Introducing routines in Claude Code — https://claude.com/blog/introducing-routines-in-claude-code
- **[S15]** Dispatch in Claude Cowork — https://claude.com/resources/tutorials/dispatch-in-claude-cowork
- **[S16]** Browse skills, connectors, and plugins in one directory — https://support.claude.com/en/articles/14328846-browse-skills-connectors-and-plugins-in-one-directory
- **[S17]** Use plugins in Claude — https://support.claude.com/en/articles/13837440-use-plugins-in-claude
- **[S18]** Use skills in Claude — https://support.claude.com/en/articles/12512180-use-skills-in-claude
