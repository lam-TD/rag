# Claude Code `settings.json` cho dự án FastAPI + Docker Compose

File này dùng để cấu hình Claude Code khi làm việc trong một dự án backend FastAPI chạy qua Docker Compose. Nên đặt tại `.claude/settings.json` (commit vào repo, chia sẻ cho cả team) hoặc `.claude/settings.local.json` (chỉ dùng riêng, không commit).

## File cấu hình đầy đủ

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "model": "claude-sonnet-5",
  "permissions": {
    "allow": [
      "Bash(docker compose up *)",
      "Bash(docker compose down *)",
      "Bash(docker compose logs *)",
      "Bash(docker compose exec *)",
      "Bash(docker compose build *)",
      "Bash(docker compose ps)",
      "Bash(uvicorn *)",
      "Bash(pytest *)",
      "Bash(ruff check *)",
      "Bash(ruff format *)",
      "Bash(alembic *)",
      "Bash(pip install *)",
      "Bash(python -m *)"
    ],
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(**/*.pem)",
      "Bash(docker compose down -v*)",
      "Bash(rm -rf *)"
    ],
    "ask": [
      "Bash(docker system prune *)",
      "Bash(docker compose exec db *)",
      "Bash(git push *)"
    ]
  },
  "env": {
    "COMPOSE_PROJECT_NAME": "myapp",
    "PYTHONDONTWRITEBYTECODE": "1"
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "ruff format $CLAUDE_FILE_PATH 2>/dev/null || true"
          }
        ]
      }
    ]
  },
  "cleanupPeriodDays": 20,
  "includeCoAuthoredBy": false
}
```

## Giải thích từng phần

### `$schema`
Trỏ tới JSON Schema chính thức của Claude Code. Không ảnh hưởng đến hành vi runtime, chỉ giúp editor (VS Code, Cursor...) gợi ý autocomplete và báo lỗi cú pháp khi bạn gõ sai key.

### `model`
Model mặc định khi khởi động session. Đặt `claude-sonnet-5` là lựa chọn cân bằng tốc độ/chi phí cho công việc code hằng ngày; có thể đổi sang model mạnh hơn khi cần review kiến trúc phức tạp bằng lệnh `/model` giữa chừng mà không cần sửa file này.

### `permissions.allow` — lệnh được chạy tự động, không cần hỏi
| Lệnh | Lý do cho phép |
|---|---|
| `docker compose up/down/logs/build/ps/exec` | Vòng đời container cơ bản, thao tác thường xuyên khi dev/debug |
| `uvicorn *` | Chạy server FastAPI trực tiếp (ngoài container) khi cần |
| `pytest *` | Chạy test — an toàn, không thay đổi trạng thái hệ thống |
| `ruff check/format *` | Lint và format code, không phá vỡ logic |
| `alembic *` | Quản lý migration DB — cần thiết cho dev loop, nhưng xem thêm lưu ý ở phần `ask` nếu môi trường có dữ liệu thật |
| `pip install *` | Cài dependency Python |
| `python -m *` | Chạy script/module Python tùy ý (seed data, tool nội bộ...) |

### `permissions.deny` — chặn tuyệt đối, không thể ghi đè bằng "allow" ở scope thấp hơn
| Rule | Lý do |
|---|---|
| `Read(./.env)`, `Read(./.env.*)` | File `.env` trong dự án FastAPI thường chứa `DATABASE_URL`, `SECRET_KEY`, API key bên thứ ba — không nên để Claude đọc được |
| `Read(./secrets/**)`, `Read(**/*.pem)` | Chặn đọc thư mục bí mật và khóa chứng chỉ (SSL/JWT private key) |
| `Bash(docker compose down -v*)` | Cờ `-v` xóa luôn **volume**, tức là mất toàn bộ dữ liệu database trong container — cực kỳ nguy hiểm nếu chạy nhầm |
| `Bash(rm -rf *)` | Lệnh xóa đệ quy không thể hoàn tác, chặn để tránh xóa nhầm thư mục |

### `permissions.ask` — luôn hỏi xác nhận trước khi chạy
| Rule | Lý do |
|---|---|
| `docker system prune *` | Dọn image/container không dùng — có thể ảnh hưởng tới project khác ngoài dự án hiện tại, không chỉ riêng repo này |
| `docker compose exec db *` | Thao tác trực tiếp vào container database (VD: `psql`, `mysql`). Rất dễ chứa lệnh `DROP`/`DELETE` — an toàn hơn nếu luôn cần xác nhận thủ công, đặc biệt khi môi trường có dữ liệu thật |
| `git push *` | Đẩy code lên remote là hành động khó hoàn tác, nên giữ quyền quyết định cuối cùng ở người |

> **Lưu ý:** `deny` có độ ưu tiên cao nhất và không thể bị ghi đè. `ask` sẽ luôn hỏi kể cả khi có `allow` ở scope khác. Thứ tự ưu tiên đầy đủ: Managed > Command line > Project local > Shared project > User settings — nhưng riêng trong 1 file, **deny > ask > allow**.

### `env`
Biến môi trường được áp dụng cho **mọi session, mọi lệnh Bash, mọi hook, và mọi MCP server** mà Claude Code khởi chạy — khác với việc export trong `.zshrc` chỉ có tác dụng nếu bạn mở terminal từ đúng shell đó.

- `COMPOSE_PROJECT_NAME`: đặt tên project cố định cho Docker Compose, tránh xung đột container name khi có nhiều bản checkout của cùng repo trên máy.
- `PYTHONDONTWRITEBYTECODE`: tắt việc Python sinh file `.pyc`, giữ thư mục làm việc sạch khi Claude chạy script nhiều lần.

### `hooks.PostToolUse`
Tự động chạy `ruff format` trên file vừa được Claude sửa (`Edit` hoặc `Write`), ngay sau khi thao tác hoàn tất — đảm bảo code luôn đúng style mà không cần nhắc lại mỗi lần. `$CLAUDE_FILE_PATH` là biến Claude Code cung cấp, trỏ đến file vừa bị thay đổi. Phần `|| true` để hook không làm gián đoạn nếu `ruff` chưa cài hoặc file không phải `.py`.

### `cleanupPeriodDays`
Số ngày giữ lịch sử transcript chat cục bộ trước khi tự xóa (mặc định 30). Giảm xuống 20 nếu muốn dọn dẹp nhanh hơn, không ảnh hưởng đến code hay git history.

### `includeCoAuthoredBy`
Đặt `false` nếu team không muốn dòng `Co-authored-by: Claude` tự động xuất hiện trong commit message/PR do Claude tạo.

## Gợi ý tùy biến thêm

- Nếu DB là **PostgreSQL**, có thể đổi rule `ask` thành cụ thể hơn: `Bash(docker compose exec postgres *)` (thay `db` bằng đúng tên service trong `docker-compose.yml`).
- Nếu dự án dùng **Alembic** với DB production thật (không chỉ local), nên chuyển `alembic *` từ `allow` sang `ask` để tránh chạy migration ngoài ý muốn.
- Có thể thêm `Bash(docker compose exec web pytest *)` riêng nếu test luôn chạy trong container thay vì máy host.
- Cân nhắc thêm `additionalDirectories` trong `permissions` nếu Claude cần đọc/ghi ra ngoài thư mục repo (VD: thư mục shared volume).

## Cách áp dụng

1. Tạo thư mục `.claude/` ở gốc repo nếu chưa có.
2. Lưu nội dung JSON ở trên vào `.claude/settings.json`.
3. Commit file để cả team dùng chung, hoặc đặt vào `.claude/settings.local.json` nếu chỉ muốn dùng riêng.
4. Trong Claude Code, chạy `/status` để xác nhận file đã được load đúng.
