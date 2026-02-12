# Schemathesis PBT – Failure Triage List

Mục tiêu: thống nhất “fail nào chấp nhận được” trong PBT (Schemathesis) để tránh:
- che mất lỗi nghiêm trọng
- và để tech debt tồn tại vô thời hạn

Nguồn sự thật: `quality/pbt/schemathesis_allowlist.yaml`

---

## Policy

### Never accept (BLOCK)
- Any **5xx** (crash / server error)
- Security / privacy leak
- Data corruption / wrong results
- Response schema mismatch on **successful (2xx)** responses

### Accept TEMP
Chỉ chấp nhận tạm thời nếu:
- Có **guardrails** (match hẹp theo error.code / status / endpoint)
- Có **expiry date**
- Có **remediation ticket** và owner

### Accept PERM
Chỉ khi đó là expected behavior và đã **document/spec rõ ràng**.

---

## Triage Table

| ID | Service | Endpoint | Check / Failure | Accept | Guardrails (summary) | Owner | Expiry | Ticket |
|---|---|---|---|---|---|---|---|---|
| PBT-LLM-001 | llm-service | POST /v1/chat/completions | status_code_conformance: got 400 undocumented | TEMP | Only if `error.code=MODEL_NOT_ALLOWED`, never 5xx | Joyce | 2026-03-01 | JIRA-1234 |
| PBT-LLM-002 | rag-service | POST /v1/ingest | response_schema_conformance | NO | N/A | Team | N/A | JIRA-1250 |

---

## How to add a new acceptable failure (TEMP)

1. Reproduce from Schemathesis output (copy redacted curl + seed)
2. Confirm it is not in “Never accept”
3. Add a rule entry in `schemathesis_allowlist.yaml`:
   - scope (service/env/endpoint)
   - failure_signature (check + status + match)
   - guardrails (must/must_not)
   - expiry + remediation ticket
4. Add a row in this table for visibility
5. Review weekly: remove rules that are fixed or expired

---

## Review cadence
- Weekly: review `active` TEMP rules, extend only with justification
- Every release: ensure no expired allowlist remains active