# Rule: Integration Test (Docker Compose Spin-up)

## Mục tiêu
- Dùng **integration test** để kiểm tra “hợp đồng” giữa **service ↔ service ↔ DB ↔ config/runtime**.
- Vì **Docker Compose spin up lâu**, cần quy định rõ **khi nào thêm/cập nhật test case** và **khi nào chạy** (smoke vs full).

---

## 1) Khi nào cần thêm mới / cập nhật integration test case?

### 1.1 Bắt buộc **thêm mới** (New test)
- Có **API/route mới** hoặc **workflow mới** (happy path quan trọng).
- Có **tích hợp mới**: service mới, bảng DB mới, queue/job mới, provider/adapter mới.
- Có **critical path mới** (lỗi gây gián đoạn chính, mất dữ liệu, ảnh hưởng khách hàng).

### 1.2 Bắt buộc **cập nhật** (Update test)
- Thay đổi **request/response schema**, status code, validation.
- Thay đổi **DB schema/migration** ảnh hưởng dữ liệu/luồng.
- Thay đổi **side effects**: ghi log/audit, enqueue job, update state, tạo file.
- Có **bug production / incident** → thêm test regression để “khóa” bug.

### 1.3 Thường **không cần** thêm (chỉ chạy lại)
- Refactor nội bộ **không đổi contract** (ưu tiên unit/contract test; integration chỉ cần re-run).
- Thay đổi UI/text nhỏ, không ảnh hưởng luồng backend/runtime.

> Nguyên tắc gọn: Mỗi critical workflow nên có **happy path + 1–2 failure mode quan trọng** (còn edge cases dồn xuống unit/property test).

---

## 2) Khi nào nên chạy integration test (vì compose spin up lâu)?

### 2.1 Trên mỗi PR/MR: chạy **Smoke Integration** (nhẹ)
Mục tiêu: bắt lỗi “stack không lên / kết nối sai” sớm.
- `docker compose up` → chờ **healthcheck** → chạy **1 happy-path critical flow**.
- Chỉ **trigger** khi PR chạm vào vùng có rủi ro phá stack/contract, ví dụ:
  - `docker/**`, `compose/**`, `Dockerfile*`, `entrypoint*`
  - `.env*`, `config/**`
  - `migrations/**`, `alembic/**`
  - (tùy dự án) các module core: `chat/**`, `embedding/**`, `ingest/**`, `retrieval/**`

### 2.2 Khi merge vào `main/develop`: chạy **Full Integration**
- `main/develop` là **quality gate**: chạy toàn bộ integration suite (có thể retry 1 lần nếu flake).

### 2.3 Nightly / Scheduled
- Chạy full để bắt lỗi môi trường, dependency drift, flake.
- Có thể kèm “extra checks” (dataset lớn hơn, kiểm thử tương thích config).

### 2.4 Trước release
- Full integration bắt buộc (release candidate).

> Rule tóm tắt: **PR: smoke + affected** → **main: full** → **nightly: full + extra** → **release: full (must pass)**

---

## 3) Giảm thời gian Compose spin up (để rule dễ áp dụng)

- **Reuse stack trong 1 CI job**: up 1 lần, chạy nhiều test bên trong (tránh up/down nhiều lần).
- Dùng **healthcheck + wait-for-healthy**, tránh `sleep` cứng.
- **Prebuilt images + cache** (buildx cache) để giảm build time.
- Nếu được: tách **smoke stack** (ít service hơn) chỉ phục vụ PR.

---

## 4) Checklist nhanh (để quyết định “có chạy smoke trên PR không?”)
Chạy smoke nếu PR có thay đổi thuộc 1 trong các nhóm:
- Compose/Docker/Runtime config
- Migration/Schema/Seed data
- Contract giữa service (request/response)
- Module core ảnh hưởng critical workflow

Không bắt buộc smoke nếu:
- Refactor thuần nội bộ, không đổi contract/config/migration
