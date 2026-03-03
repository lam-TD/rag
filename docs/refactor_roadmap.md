# Roadmap Refactor FastAPI (Incremental & Ship-able)

> Mục tiêu: refactor theo **giai đoạn**, giảm rủi ro, **mỗi phase đều ship được**, tránh “big‑bang refactor”.

---

## 1) Phạm vi & giả định

### Phạm vi (Scope)
- FastAPI app (hoặc monorepo nhiều service FastAPI) + Docker Compose
- Alembic migrations, PostgreSQL (có thể kèm pgvector)
- Test: pytest + integration test (call API) + seed/cleanup dữ liệu test
- Chuẩn hóa: config/env, error handling, logging/observability, auth (nếu có)

### Không làm trong roadmap này (Out of scope – có thể tách task)
- Re-write toàn bộ sang kiến trúc mới 100%
- Thay DB engine / thay framework
- Re-implement toàn bộ domain logic

### Nguyên tắc vận hành
- **Incremental**: PR nhỏ, merge liên tục
- **Vertical slice**: refactor theo *feature/endpoints* thay vì “dọn hết layer”
- **Backward compatible**: ưu tiên giữ API/behavior ở các phase đầu
- **Có safety net**: test + observability trước khi “mổ sâu”

---

## 2) KPI/Success Metrics (đo được)

Chọn 3–6 chỉ số (tối thiểu 3):

- **Build/Test time**: tổng thời gian CI (mục tiêu giảm/ổn định)
- **Flaky tests**: số test flaky/tuần (mục tiêu giảm về 0)
- **Error rate**: 5xx, exception unhandled (mục tiêu giảm)
- **p95 latency** (nếu có monitor): ổn định hoặc cải thiện
- **Dev cycle time**: thời gian từ PR -> merge (mục tiêu giảm)
- **Bug regressions** sau refactor (mục tiêu không tăng)

---

## 3) Roadmap theo Phase (mỗi phase có deliverable + exit criteria)

### Phase 0 — Baseline & kế hoạch (1–3 ngày làm việc)
**Mục tiêu**: biết “đang đau ở đâu”, chốt cách đo.
- [ ] Liệt kê 5–10 pain points (VD: error response không thống nhất, DI rối, test chạy lâu, config trùng lặp…)
- [ ] Chốt KPI tối thiểu (3 KPI)
- [ ] Chốt chiến lược PR: kích thước PR, naming, review checklist
- [ ] Tạo doc: `docs/refactor/roadmap.md` + `ADR-Refactor-Strategy.md`

**Exit criteria**
- Có baseline (CI time, test time, error format hiện tại)
- Có plan & nguyên tắc merge

---

### Phase 1 — Safety Net (1–2 tuần)
**Mục tiêu**: refactor mà không “mù”.

#### 1.1 Integration test harness + seed/cleanup
- [ ] Tạo docker-compose-test (hoặc profile) để spin up DB + app
- [ ] Implement seed data (alembic seed / SQL script / API seed)
- [ ] Implement cleanup (truncate schema / recreate DB / transaction rollback chiến lược)
- [ ] Fixtures: base URL, auth token (nếu có), DB reset

#### 1.2 Observability tối thiểu
- [ ] Logging chuẩn (JSON hoặc structured), có `request_id/correlation_id`
- [ ] Health check `/health` + readiness (DB ping)
- [ ] Standard log fields: service, env, trace_id/request_id, user_id (nếu hợp lệ)

#### 1.3 CI Quality gates
- [ ] lint/format (ruff/black), type-check (mypy/pyright nếu phù hợp)
- [ ] chạy smoke integration test tối thiểu (1–3 endpoint critical)
- [ ] coverage tối thiểu cho critical modules (không cần 100%)

**Exit criteria**
- Integration tests chạy ổn định, có seed/cleanup repeatable
- Log có request_id và dễ trace lỗi
- CI có gate cơ bản, giảm rủi ro regression

---

### Phase 2 — Chuẩn hóa Cross‑cutting (1–2 tuần)
**Mục tiêu**: nhất quán những thứ “đụng nhiều chỗ”, ROI cao.

#### 2.1 Settings/Config “single source of truth”
- [ ] Chuẩn hóa `Settings` (pydantic settings)
- [ ] Quy ước .env layering (local/dev/test/prod)
- [ ] Validate config lúc startup; fail fast nếu thiếu

#### 2.2 Error handling thống nhất
- [ ] Chuẩn error envelope (ví dụ)
  - `code`, `message`, `details`, `request_id`, `timestamp`
- [ ] Map exception -> HTTP (validation, not found, forbidden, conflict, unexpected)
- [ ] Viết test cho 5 case lỗi phổ biến

#### 2.3 Dependency injection conventions
- [ ] Quy ước dependency: `Depends(get_db)`, `Depends(get_current_user)`, …
- [ ] Tách “wiring” (providers) khỏi business logic
- [ ] Tối ưu import vòng: module boundary rõ ràng

**Exit criteria**
- 100% endpoint mới dùng error format chuẩn
- 70% endpoint cũ được migrate error handler mà không đổi behavior
- Settings & env không còn trùng/đè không kiểm soát

---

### Phase 3 — Modularization theo Feature/Domain (2–4 tuần, làm incremental)
**Mục tiêu**: dễ mở rộng, dễ đọc, giảm coupling.

#### Chiến lược: “Strangler / Branch by Abstraction”
- Tạo interface / service mới bọc code cũ
- Migrate dần từng feature

#### Deliverables
- [ ] Định nghĩa module boundary (theo domain/feature)
  - `modules/<feature>/router.py`
  - `modules/<feature>/schemas.py`
  - `modules/<feature>/service.py` (use-cases)
  - `modules/<feature>/repository.py` (data access)
- [ ] Migrate theo *vertical slice*:
  - 1 feature = router + service + repository + tests
- [ ] Shared libs:
  - `common/errors`, `common/logging`, `common/settings`, `common/security`

**Exit criteria**
- Ít nhất 2–4 feature critical đã migrate hoàn chỉnh
- Mỗi feature có integration tests tối thiểu
- Giảm import vòng và “god module”

---

### Phase 4 — Data layer & Transactions (1–3 tuần, tuỳ độ phức tạp)
**Mục tiêu**: correctness + performance + maintainability.

#### 4.1 Transaction boundary & Unit of Work
- [ ] Quy ước “1 request = 1 transaction” (tuỳ use-case)
- [ ] Session lifecycle rõ ràng (async SQLAlchemy / sync)
- [ ] Xử lý retry/serialization failure (nếu cần)

#### 4.2 Migrations backward compatible
- [ ] Quy trình migration 2 bước (add -> backfill -> switch -> cleanup)
- [ ] Script backfill an toàn (batching)
- [ ] Test migration basic (upgrade/downgrade nếu có)

#### 4.3 Performance hotspots
- [ ] Audit N+1, index thiếu, query chậm
- [ ] Add index dựa trên query thực tế
- [ ] Cache (nếu cần) — nhưng chỉ sau khi đo

**Exit criteria**
- Không có lỗi transaction leak
- Migration strategy chuẩn, rollback rõ
- p95 latency ổn định hoặc cải thiện (nếu có đo)

---

### Phase 5 — Cleanup & Hardening (1–2 tuần)
**Mục tiêu**: chốt nợ kỹ thuật, dễ vận hành lâu dài.

- [ ] Xóa code chết / deprecated paths
- [ ] Chuẩn hóa naming & folder structure
- [ ] Docs-as-code:
  - `README` (run local/dev/test)
  - `RUNBOOK` (incident basics)
  - `ARCHITECTURE` (C4 high-level, module map)
- [ ] Add minimal load/stress test cho endpoints critical
- [ ] Security pass: dependency audit, secrets, auth checks

**Exit criteria**
- Docs đủ để dev mới chạy dự án + chạy test
- Nợ kỹ thuật được đóng theo danh sách
- Không còn dual-path (cũ/mới) không kiểm soát

---

## 4) Timeline mẫu 8 tuần (có thể co giãn)

> Đây là timeline gợi ý để bạn “có nhịp”. Nếu dự án lớn, hãy giữ **thứ tự phase** nhưng kéo dài số tuần.

### Tuần 1 — Phase 0 + bắt đầu Phase 1
- [ ] Baseline metrics + pain points
- [ ] Tạo docker-compose-test / profile test
- [ ] Seed/cleanup v1 (có thể còn thô)

### Tuần 2 — Phase 1 hoàn chỉnh
- [ ] Integration tests cho 2–3 endpoint critical
- [ ] Logging có request_id + health check
- [ ] CI gates cơ bản (lint + 1 bộ integration test)

### Tuần 3 — Phase 2 (Config/Settings)
- [ ] Settings chuẩn + env layering
- [ ] Startup validation
- [ ] Refactor config usage tại 2–3 module quan trọng

### Tuần 4 — Phase 2 (Error handling + DI conventions)
- [ ] Error envelope + exception mapping + tests
- [ ] Chuẩn hóa dependency injection cho auth/db
- [ ] Migrate 30–50% endpoints vào chuẩn lỗi

### Tuần 5 — Phase 3 (Feature modularization – slice 1)
- [ ] Chốt module map theo domain
- [ ] Migrate Feature A end-to-end + tests
- [ ] Tạo shared `common/*` dùng chung

### Tuần 6 — Phase 3 (slice 2–3)
- [ ] Migrate Feature B/C + tests
- [ ] Dọn import vòng, tách utilities

### Tuần 7 — Phase 4 (Data layer)
- [ ] Chuẩn transaction/session lifecycle
- [ ] Migration backward compatible guideline + áp dụng 1 thay đổi mẫu
- [ ] Audit query 1–2 endpoint chậm

### Tuần 8 — Phase 5 (Cleanup & hardening)
- [ ] Remove deprecated code paths
- [ ] Runbook + docs + architecture notes
- [ ] Smoke load test + dependency audit

---

## 5) Checklist “Definition of Done” cho mỗi PR refactor
- [ ] PR nhỏ (dễ review), có mô tả “behavior unchanged” (nếu đúng)
- [ ] Có test (unit hoặc integration) cho phần thay đổi
- [ ] Log/metrics không bị giảm chất lượng (request_id vẫn hoạt động)
- [ ] Không tăng thời gian CI đáng kể (hoặc có lý do)
- [ ] Không phá public API (hoặc có migration plan)
- [ ] Có rollback / toggle (nếu thay đổi rủi ro)

---

## 6) Rủi ro thường gặp & cách giảm
- **Refactor kéo dài vô hạn** → chia slice, mỗi tuần ship 1 phần
- **PR quá lớn** → giới hạn file/module, “migrate 1 feature/PR”
- **Thiếu safety net** → Phase 1 bắt buộc, tối thiểu 2–3 endpoint critical
- **Đụng data layer sớm** → chỉ làm sau khi error/config/test ổn
- **Thay đổi behavior không chủ ý** → snapshot tests (contract) + integration tests

---

## 7) Template backlog item (để bạn copy vào Jira/GitLab Issue)
**Title**: Refactor <Feature/Module> to new module structure  
**Goal**: <tại sao làm>  
**Scope**:
- Router:
- Service/use-case:
- Repository:
- Schemas:
- Tests:
**Non-goals**:
- …
**DoD**:
- Tests pass, no behavior change, docs updated  
**Rollback**:
- …

---

### Gợi ý cấu trúc thư mục (tham khảo)
```
app/
  common/
    settings.py
    errors.py
    logging.py
    security.py
  modules/
    feature_a/
      router.py
      schemas.py
      service.py
      repository.py
    feature_b/
      ...
tests/
  integration/
  unit/
docker/
  compose.test.yml
docs/
  refactor/
    roadmap.md
    adr/
```

---

**Bạn có thể chỉnh roadmap này theo thực tế dự án** bằng cách:
1) liệt kê danh sách feature/domain quan trọng nhất (top 5),  
2) gán chúng vào Phase 3 theo mức độ ưu tiên,  
3) chọn endpoints “critical” để làm integration tests trước.

