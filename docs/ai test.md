Test Strategy & Automation Plan cho dự án API RAG

1. Bối cảnh dự án

Tài liệu này tổng hợp chiến lược kiểm thử cho một dự án API RAG với các thành phần điển hình như:

* Backend API: FastAPI
* Database: PostgreSQL + pgvector
* File extraction: Apache Tika hoặc service tương đương
* Embedding service: external hoặc internal provider
* LLM service: OpenAI / local model / provider abstraction
* Pipeline chính: upload document → extract text → chunk → embedding → store vector → retrieve → answer with citations
* Yêu cầu quan trọng:
    * Trả lời dựa trên tài liệu
    * Có citation rõ ràng
    * Không biết thì phải trả lời “không biết”
    * Không leak dữ liệu giữa collection/user/document
    * Hỗ trợ nhiều ngôn ngữ như Vietnamese, English, Japanese

⸻

2. Tỷ lệ phân bổ test đề xuất

Baseline đề xuất:

Unit Test: 40%
Integration Test: 30%
API / Contract Test: 10%
RAG Evaluation: 10%
End-to-End Test: 5%
Security + Performance Smoke Test: 5%

Loại test	Tỷ lệ nên chiếm	Mục tiêu chính
Unit test	35–45%	Kiểm tra logic nhỏ, chạy nhanh, dễ debug
Integration test	25–35%	Kiểm tra các service thật phối hợp đúng
API / Contract test	10–15%	Đảm bảo endpoint đúng schema, status code, error response
RAG eval / Retrieval quality test	10–15%	Đánh giá chất lượng retrieval, citation, grounded answer
End-to-end test	5–10%	Kiểm tra flow thật từ upload đến answer
Security / abuse test	5–10%	Prompt injection, data leakage, file upload attack
Performance / load test	khoảng 5%	Đo latency, throughput, vector search, ingestion throughput

⸻

3. Mức độ automation theo từng loại test

Loại test	Có thể automation không?	Mức độ automation nên đạt	Chạy khi nào?	Gợi ý tool
Unit test	Có	90–100%	Mỗi commit / merge request	pytest, pytest-cov
Integration test	Có	70–90%	Merge request + nightly	pytest, Docker Compose
API / Contract test	Có	80–100%	Mỗi merge request	Schemathesis, OpenAPI
RAG eval / Retrieval quality test	Có, cần dataset chuẩn	60–80%	Nightly + trước release	custom eval script
E2E test	Có	50–70%	Trước release / nightly	pytest, API client
Security test	Có một phần	50–70%	Nightly + trước release	OWASP ZAP, custom prompt-injection tests
Performance test	Có	60–80%	Nightly / weekly / trước release	k6, Locust
Manual exploratory test	Không hoàn toàn	0–30%	Trước release lớn	manual checklist

⸻

4. Nhóm nên automation trước

Must automate

Unit test
Integration test core pipeline
API contract test
DB migration test
Collection isolation test

Should automate

RAG eval
Citation accuracy
Unknown handling
Prompt injection regression
Multi-language retrieval

Automate by schedule

Performance test
Security scan
Dependency scan
Full E2E
Large file ingestion
Long-running stability test

⸻

5. CI/CD Pipeline đề xuất

Tầng 1 — Mỗi commit

lint
type check
unit test
small API contract test
coverage report

Tool gợi ý:

Check	Tool
Lint	ruff
Type check	ty hoặc mypy
Unit test	pytest
Coverage	pytest-cov
API schema smoke	Schemathesis subset

Tầng 2 — Merge request

unit test full
integration test core
contract test full
migration test
docker compose test environment

Tầng 3 — Nightly

full integration
full RAG eval
security regression
performance baseline
large document test
multi-language test

Tầng 4 — Trước release

E2E full flow
security review
load test
rollback test
data isolation test
acceptance test

⸻

6. Checklist test case cụ thể cho API RAG

A. Upload & Ingestion

valid PDF upload
valid DOCX upload
valid TXT upload
unsupported file type
empty file
file > size limit
Tika extraction failed
document status changes correctly
retry failed ingestion
duplicate file handling
deleted document không còn search được

B. Chunking

chunk không rỗng
chunk overlap đúng
không mất text đầu/cuối
không tạo chunk quá dài
metadata có document_id
metadata có collection_id
metadata có page/source nếu có

C. Embedding

embedding đúng dimension
provider timeout được handle
rate limit được handle
embedding failed thì document status = failed
retry embedding không tạo duplicate record
model dimension mismatch bị phát hiện sớm

D. Retrieval

query đúng collection
top_k trả đúng số lượng
không trả chunk ngoài collection
similarity score được sort đúng
không leak document đã deleted
filter theo document_id đúng
filter theo collection_id đúng
empty result được xử lý đúng

E. Ask API

question hợp lệ
question rỗng
collection không tồn tại
document chưa ingest xong
answer có citations
answer không có context thì nói không biết
answer không dùng citation giả
usage token được log nếu có
latency được log nếu có

F. Citation

citation có document_id
citation có chunk_id
citation có page/source nếu có
citation content thật sự support answer
không có citation giả
citation không trỏ sang collection khác
citation vẫn đúng sau khi document update/delete

G. Prompt Injection

document chứa instruction độc hại
user hỏi yêu cầu bỏ qua system instruction
document yêu cầu reveal system prompt
document yêu cầu trả lời ngoài context
document yêu cầu lấy dữ liệu từ collection khác
answer vẫn tuân thủ system/developer instruction

H. Multi-language

Vietnamese question → English document
English question → Japanese document
Japanese question → English document
mixed language query
Vietnamese answer with English source
Japanese source citation mapping

I. Authorization / Data Isolation

user A không thấy collection của user B
collection A không retrieve document của collection B
document deleted không còn trong search
private document không xuất hiện trong public collection
invalid token bị reject
missing token bị reject
wrong role bị reject

J. Performance

Ask API p95 latency
retrieval p95 latency
embedding latency
LLM latency
upload response latency
ingestion throughput
vector search với 10k chunks
vector search với 50k chunks
vector search với 100k chunks
DB connection pool saturation

⸻

7. Acceptance Metrics đề xuất

Nhóm	Metric	Target gợi ý
Unit	Code coverage cho core logic	≥ 80%
Integration	Core pipeline pass rate	100%
API contract	Undocumented response	0 critical
Retrieval	Top-3 hit rate	≥ 85%
Citation	Citation correctness	≥ 90%
Unknown handling	Correct refusal / “không biết”	≥ 95%
Security	Cross-collection leakage	0 case
Prompt injection	Injection success rate	0 critical
Performance	Ask p95 latency	Theo SLA dự án
Reliability	Nightly pass rate	≥ 95%

⸻

8. Báo cáo ngắn cho manager

Với dự án API RAG, test strategy cần kết hợp giữa test pyramid truyền thống và RAG quality evaluation. Baseline đề xuất là 40% unit test, 30% integration test, 10% API/contract test, 10% RAG evaluation, 5% E2E và 5% security/performance smoke test. Điểm khác biệt của RAG so với API thông thường là cần kiểm tra thêm retrieval quality, citation correctness, grounded answer, unknown handling và data isolation. Automation nên được chia thành nhiều tầng: commit-level cho unit/contract smoke, merge-level cho integration và migration, nightly cho full RAG eval/security regression, và release-level cho E2E/performance/load test.

⸻

9. Kết luận

Chiến lược test phù hợp cho API RAG không chỉ trả lời câu hỏi:

API có chạy không?

Mà phải trả lời được các câu hỏi quan trọng hơn:

RAG có tìm đúng tài liệu không?
Answer có dựa trên context không?
Citation có đúng nguồn không?
Không có thông tin thì có biết từ chối không?
Có leak dữ liệu giữa collection/user/document không?
Hệ thống có chống được prompt injection cơ bản không?
Latency có nằm trong SLA không?

Recommendation cuối cùng:

40% Unit Test
30% Integration Test
10% API / Contract Test
10% RAG Evaluation
5% End-to-End Test
5% Security + Performance Smoke Test