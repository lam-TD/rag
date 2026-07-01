                          ┌─────────────────┐
                          │   Test Dataset  │
                          │ (câu hỏi đa dạng│
                          │  độ dài + ground│
                          │      truth)     │
                          └────────┬────────┘
                                   │
            ┌──────────────────────┼──────────────────────┐
            │                      │                      │
            ▼                      ▼                      ▼
   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
   │  FUNCTIONAL/     │   │  QUALITY (RAG)  │   │  LOAD / STRESS  │
   │  API TEST        │   │                 │   │                 │
   │  pytest + httpx  │   │  Ragas /        │   │  Locust / k6    │
   │                  │   │  DeepEval       │   │                 │
   └────────┬─────────┘   └────────┬────────┘   └────────┬────────┘
            │                      │                      │
            │  gọi endpoint        │  chấm điểm           │  bắn tải
            │                      │  faithfulness,       │  N users đồng thời
            │                      │  relevancy...        │
            └──────────────────────┼──────────────────────┘
                                   │
                                   ▼
              ┌──────────────────────────────────────────┐
              │            FASTAPI RAG SERVICE            │
              │  ┌────────────┐   ┌──────────────────┐    │
              │  │  /query    │──▶│  Retriever       │    │
              │  │  endpoint  │   │  (Vector DB)     │    │
              │  └────────────┘   └────────┬─────────┘    │
              │         │                  │ context      │
              │         │                  ▼              │
              │         │         ┌──────────────────┐    │
              │         └────────▶│  LLM Generation  │    │
              │                   │  (stream/token)  │    │
              │                   └──────────────────┘    │
              └──────────────────────────────────────────┘
                                   │
                                   ▼
              ┌──────────────────────────────────────────┐
              │              CI / CD PIPELINE             │
              │  - chạy pytest (gate logic)               │
              │  - chạy quality eval (gate chất lượng)    │
              │  - chạy load test với threshold p95<2s    │
              │  - fail build nếu vượt ngưỡng             │
              └──────────────────────────────────────────┘
