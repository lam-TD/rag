# Coding Standards

> Mục tiêu: thống nhất cách viết code trong team để review dễ, giảm bug, refactor an toàn, onboarding nhanh.

## 1) Scope
Áp dụng cho toàn bộ source code Python của dự án (FastAPI + worker nếu có).
- Bắt buộc: format/lint/typecheck/test phải **pass trên CI**.
- Ưu tiên: tính nhất quán hơn “gu cá nhân”.

## 2) Tooling (Enforced by CI)
### 2.1 Python
- Python: **3.12**
- Dependency management: (TODO: poetry / pip-tools / pip + requirements.txt)

### 2.2 Formatter + Linter
- **Ruff** là tool chuẩn:
  - Format: `ruff format .`
  - Lint: `ruff check .`
  - Auto-fix: `ruff check --fix .`

**Không tranh luận format trong review**: để tool quyết định.

### 2.3 Type Checking
- Type checker: **Pyright** (hoặc mypy nếu project đã dùng)
- Quy ước:
  - Service / repository / public functions **phải có type hints**
  - Tránh `Any` tràn lan (chỉ dùng khi có lý do)

### 2.4 Pre-commit
- Bắt buộc cài `pre-commit` và chạy hooks trước khi push.
- CI sẽ fail nếu format/lint chưa đúng.

## 3) Code Style (PEP 8 + Practical)
### 3.1 Line length
- Line length: **88** (theo config Ruff).
- Nếu khó đọc vì xuống dòng quá nhiều: ưu tiên readability, tách biến, tách hàm.

### 3.2 Imports
- Import order do Ruff quản lý.
- Cấm `from x import *`.
- Tránh import vòng (circular import). Nếu gặp: refactor module boundary.

### 3.3 Naming
- file/module: `snake_case.py`
- class: `PascalCase`
- function/var: `snake_case`
- constant: `UPPER_SNAKE_CASE`
- boolean: `is_`, `has_`, `can_` (ví dụ: `is_active`, `has_access`)
- private/internal: prefix `_`

## 4) Project Structure (Folder Convention)
> Mục tiêu: ai cũng biết “để code ở đâu”.

Khuyến nghị cấu trúc (có thể điều chỉnh theo codebase hiện tại):


**Quy tắc placement**
- `api/routers`: chỉ xử lý HTTP layer (validate input, gọi service, trả response)
- `services`: business logic, không chứa FastAPI-specific (`Depends`, `Request`, `Response`)
- `repositories`: query DB, không chứa business rules
- `schemas`: Pydantic models (DTO)
- `deps`: dependency providers (DB session, current user, service factory…)

## 5) FastAPI Conventions
### 5.1 Router rules
- Router không chứa business logic phức tạp.
- Mỗi endpoint:
  - validate input (Pydantic)
  - gọi service
  - trả response theo schema
- `response_model` phải rõ ràng (giúp docs + test contract).

### 5.2 DI (Dependency Injection) – MUST READ
> Mục tiêu: team thống nhất, test dễ.

**Quy tắc vàng**
- `Depends(...)` chỉ dùng trong **router** và **dependency provider** (trong `app/deps/`).
- Service/repository **không import FastAPI**.

**Ví dụ đúng**
- Router:
  - inject service: `rag_service: RagService = Depends(get_rag_service)`
- Dependency provider:
  - `get_db()` tạo/yield session theo request
  - `get_rag_service()` tạo service từ repo + clients

**Không làm**
- Không tạo DB session global.
- Không gọi trực tiếp LLM client trong router (phải qua service).
- Không “new service” rải rác nhiều chỗ → phải qua `deps`.

### 5.3 Error handling
- Tạo custom exceptions ở service layer (vd: `NotFoundError`, `PermissionDenied`)
- Router map exception → HTTP response (hoặc middleware/exception handler)
- Với RAG: nếu retrieval không ra đủ ngữ cảnh → trả “Không tìm thấy thông tin…” (không bịa).

## 6) Database & Multi-tenant / Access Control
- Mọi query liên quan dữ liệu khách hàng phải có filter theo:
  - `tenant_id` / `customer_id` (tùy hệ thống)
- Với RAG documents/chunks/embeddings:
  - đảm bảo không leak dữ liệu cross-tenant
- Migration:
  - dùng Alembic (hoặc tool hiện tại)
  - migration phải review như code

## 7) Logging & Observability
- Log phải có: `request_id/trace_id`, `user/tenant`, `endpoint`, `latency_ms`, `status_code`.
- Không log thông tin nhạy cảm (token, secret, raw PII).
- Lỗi phải có stacktrace + context đủ để debug.

## 8) Testing Standards (Refactor-safe)
> Ưu tiên: **API contract tests** trước, rồi mới unit/integration.

### 8.1 Test pyramid (order)
1) **API contract tests**: happy path + auth + validation + “no data → don’t know”
2) **Service unit tests**: logic chính (mock repo/clients)
3) **Repository tests**: chỉ query quan trọng (filters, tenant scope)

### 8.2 Test rules
- Naming:
  - file: `test_*.py`
  - function: `test_should_<expected>_when_<condition>`
- Structure: Arrange – Act – Assert
- Không gọi LLM thật trong unit test:
  - dùng fake/stub client
- Integration test (nếu có):
  - chạy với Postgres/pgvector (docker service)

## 9) Git Workflow & PR Rules
- Không push trực tiếp `main/master`.
- Branch naming:
  - `feat/<short-desc>`
  - `fix/<short-desc>`
  - `chore/<short-desc>`
- PR phải có:
  - mô tả thay đổi + ảnh hưởng
  - link issue/task
  - test evidence (CI xanh, hoặc ghi rõ cách test local)
- “Definition of Done” tối thiểu:
  - ruff + typecheck + pytest pass
  - không giảm security/tenant isolation
  - có/điều chỉnh docs nếu ảnh hưởng onboarding

## 10) Onboarding (Quick Start)
- `docker compose up -d` (db + services)
- apply migrations: (TODO: command)
- run api: (TODO: command)
- run tests: `pytest -q`
- run lint/format:
  - `ruff format .`
  - `ruff check .`
  - `pyright`

---

## Appendix: Commands Cheat Sheet
- Format: `ruff format .`
- Lint: `ruff check .`
- Lint + fix: `ruff check --fix .`
- Typecheck: `pyright`
- Test: `pytest -q`
- Pre-commit install: `pre-commit install`