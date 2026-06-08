# Bộ trắc nghiệm đánh giá năng lực AI cho team Engineers

> Mục tiêu: chẩn đoán năng lực AI của team theo từng nhóm kiến thức, từ đó xây lộ trình nâng cấp.
> Quy mô: ~45 câu | Đối tượng: team thiên về xây dựng/code AI.

-----

## 1. Tổng quan thiết kế

Bài test dựa trên cách tiếp cận đánh giá AI literacy theo 3 chiều (khái niệm – thực hành – đạo đức), kết hợp bộ kỹ năng cốt lõi của AI Engineer (prompting, RAG, agents, fine-tuning, deployment, evaluation).

Nguyên tắc quan trọng:

- **Dùng câu kiểm tra khách quan**, không lấy câu tự đánh giá làm điểm chính (tự đánh giá thường lệch xa năng lực thực tế).
- **Chấm theo từng nhóm**, không gộp tổng — để mỗi người ra một “radar” 8 trục.
- **Phân tầng 3 mức** để định vị vị trí trên lộ trình thay vì chỉ pass/fail.

-----

## 2. Phân bổ câu hỏi (45 câu)

|#|Nhóm                     |Số câu|Trọng số|Phân tầng (L1/L2/L3)|
|-|-------------------------|------|--------|--------------------|
|1|Nền tảng AI/LLM          |6     |13%     |3 / 2 / 1           |
|2|Prompt Engineering       |5     |11%     |2 / 2 / 1           |
|3|RAG                      |9     |20%     |4 / 3 / 2           |
|4|Fine-tuning              |5     |11%     |2 / 2 / 1           |
|5|AI Agents                |6     |13%     |2 / 3 / 1           |
|6|Evaluation               |6     |13%     |2 / 2 / 2           |
|7|Deployment & Optimization|5     |11%     |2 / 2 / 1           |
|8|Đạo đức & Quản trị       |3     |7%      |2 / 1 / 0           |

**Thang mức độ:**

- **L1 – Cơ bản:** nhận biết khái niệm, định nghĩa.
- **L2 – Trung cấp:** áp dụng, chọn kỹ thuật đúng cho tình huống.
- **L3 – Nâng cao:** xử lý lỗi, đánh đổi kiến trúc, tối ưu.

-----

## 3. Bộ câu hỏi mẫu

> Mỗi nhóm có 3 câu mẫu (L1, L2, L3) để bạn nhân bản cho đủ số lượng. Đáp án đúng được đánh dấu **(✓)**.

### Nhóm 1 — Nền tảng AI/LLM

**[L1]** Trong một LLM, “token” là gì?

- A. Một câu hoàn chỉnh
- B. Đơn vị văn bản nhỏ (từ/mảnh từ/ký tự) mà mô hình xử lý **(✓)**
- C. Một tham số trong mạng neural
- D. Một lệnh API

**[L2]** Vì sao embedding lại cho phép tìm kiếm theo ngữ nghĩa (semantic search) tốt hơn so với so khớp từ khóa?

- A. Vì embedding nén văn bản để tiết kiệm bộ nhớ
- B. Vì embedding biểu diễn ý nghĩa dưới dạng vector, nên văn bản gần nghĩa nằm gần nhau trong không gian vector **(✓)**
- C. Vì embedding loại bỏ stopwords
- D. Vì embedding luôn chính xác hơn

**[L3]** Một LLM decoder-only được huấn luyện chủ yếu bằng next-token prediction. Hệ quả nào sau đây là đúng?

- A. Mô hình có kho kiến thức sự thật cố định và không bao giờ sai
- B. Mô hình sinh văn bản hợp lý về mặt thống kê, nên có thể “ảo giác” (hallucinate) thông tin sai nhưng nghe hợp lý **(✓)**
- C. Mô hình chỉ trả lời được câu hỏi có trong tập huấn luyện
- D. Loss thấp đảm bảo đầu ra luôn đúng

-----

### Nhóm 2 — Prompt Engineering

**[L1]** Sự khác nhau giữa system prompt và user prompt là gì?

- A. Không có khác biệt
- B. System prompt thiết lập vai trò/ngữ cảnh và ràng buộc hành vi; user prompt là yêu cầu cụ thể của người dùng **(✓)**
- C. User prompt luôn được ưu tiên tuyệt đối hơn system prompt
- D. System prompt chỉ dùng khi fine-tune

**[L2]** Khi nào kỹ thuật few-shot (multi-shot) prompting có lợi nhất?

- A. Khi cần mô hình tuân theo một định dạng/đầu ra cụ thể mà mô tả bằng lời khó diễn đạt **(✓)**
- B. Luôn luôn, vì càng nhiều ví dụ càng tốt
- C. Chỉ khi mô hình đã được fine-tune
- D. Khi muốn giảm độ trễ

**[L3]** Bạn cần một prompt buộc mô hình chỉ trả lời dựa trên tài liệu được cung cấp, không bịa. Cách tiếp cận nào hợp lý nhất?

- A. Tăng temperature để mô hình sáng tạo hơn
- B. Ràng buộc rõ trong prompt (“chỉ dùng context, nếu không có thì nói không biết”) + yêu cầu trích dẫn nguồn + đánh giá đầu ra **(✓)**
- C. Lặp lại câu hỏi nhiều lần
- D. Chuyển sang mô hình lớn hơn

-----

### Nhóm 3 — RAG

**[L1]** Vai trò chính của vector database trong một hệ RAG là gì?

- A. Lưu trữ và truy xuất nhanh các embedding theo độ tương đồng ngữ nghĩa **(✓)**
- B. Huấn luyện lại mô hình
- C. Thay thế hoàn toàn LLM
- D. Nén mô hình

**[L1]** Sắp xếp đúng thứ tự pipeline RAG cơ bản:

- A. embedding → chunking → retrieval → generation
- B. documents → chunking → embedding → indexing → retrieval → generation **(✓)**
- C. retrieval → embedding → chunking → generation
- D. generation → retrieval → chunking

**[L2]** Với tài liệu pháp lý dài có nhiều điều khoản đánh số, chiến lược chunking nào thường phù hợp hơn?

- A. Cắt cố định 100 ký tự bất kể nội dung
- B. Chunk theo cấu trúc ngữ nghĩa (theo điều/khoản) kèm overlap để giữ ngữ cảnh **(✓)**
- C. Đưa cả tài liệu vào một chunk duy nhất
- D. Chunk ngẫu nhiên

**[L2]** Khi nào nên dùng hybrid search (kết hợp keyword + semantic)?

- A. Khi truy vấn chứa thuật ngữ chính xác, mã ID, tên riêng, tham chiếu pháp lý — nơi so khớp từ khóa quan trọng **(✓)**
- B. Chỉ khi không có vector database
- C. Khi muốn giảm chi phí embedding
- D. Không bao giờ cần

**[L3]** Hệ RAG của bạn trả lời sai/bịa dù tài liệu có chứa câu trả lời đúng. Nguyên nhân gốc khả dĩ nhất nằm ở đâu?

- A. Temperature quá thấp
- B. Chunking kém khiến retriever không tìm được đoạn chứa câu trả lời (thiếu ngữ cảnh, đoạn bị cắt vụn) **(✓)**
- C. LLM quá lớn
- D. Vector database lưu quá nhiều dữ liệu

**[L3]** Mục đích của bước reranking sau retrieval là gì?

- A. Giảm số tài liệu cần index
- B. Sắp xếp lại các đoạn đã truy xuất theo độ liên quan thực sự với truy vấn, để đưa đoạn tốt nhất vào prompt **(✓)**
- C. Tạo embedding mới
- D. Thay thế bước generation

-----

### Nhóm 4 — Fine-tuning

**[L1]** PEFT (Parameter-Efficient Fine-Tuning) khác full fine-tuning ở điểm cốt lõi nào?

- A. Chỉ cập nhật một phần nhỏ tham số (ví dụ qua adapter), tiết kiệm bộ nhớ/chi phí **(✓)**
- B. Huấn luyện lại toàn bộ mô hình từ đầu
- C. Không cần dữ liệu
- D. Chỉ áp dụng cho mô hình nhỏ

**[L2]** Tình huống nào nên ưu tiên fine-tuning hơn là RAG hoặc prompt engineering?

- A. Khi cần mô hình học một phong cách/định dạng đầu ra ổn định, đặc thù domain mà prompt khó ép được **(✓)**
- B. Khi dữ liệu thay đổi liên tục hằng ngày
- C. Khi chỉ cần bổ sung kiến thức sự thật cập nhật
- D. Khi muốn tránh chi phí huấn luyện

**[L3]** QLoRA cho phép fine-tune tiết kiệm bộ nhớ bằng cách nào?

- A. Bỏ qua bước huấn luyện
- B. Dùng base weights được lượng tử hóa (quantized) làm nền cho fine-tuning hiệu quả bộ nhớ **(✓)**
- C. Chỉ dùng CPU
- D. Xóa bớt dữ liệu huấn luyện

-----

### Nhóm 5 — AI Agents

**[L1]** “Tool calling” (function calling) trong agent nghĩa là gì?

- A. Gọi một mô hình khác để thay thế
- B. LLM quyết định gọi một hàm/công cụ bên ngoài (API, tìm kiếm, tính toán) để hoàn thành tác vụ **(✓)**
- C. Một loại prompt cố định
- D. Cách nén mô hình

**[L2]** Một agent cần giải bài toán nhiều bước (tra cứu → tính toán → tổng hợp). Pattern nào phù hợp?

- A. Một prompt duy nhất, không chia bước
- B. Vòng lặp reasoning + hành động (gọi tool) lặp lại cho đến khi đủ thông tin, rồi mới trả lời **(✓)**
- C. Tăng max_tokens
- D. Fine-tune lại mô hình

**[L3]** Self-correction loop trong agent dùng để làm gì?

- A. Tăng tốc độ phản hồi
- B. Cho agent tự rà soát/đánh giá đầu ra của mình trước khi trả về, giúp giảm lỗi và ảo giác **(✓)**
- C. Giảm chi phí token
- D. Thay thế evaluation

-----

### Nhóm 6 — Evaluation

**[L1]** “LLM-as-a-Judge” là gì?

- A. Dùng một mô hình mạnh hơn để chấm điểm đầu ra của mô hình khác theo các tiêu chí (liên quan, mạch lạc, đúng sự thật) **(✓)**
- B. Một benchmark chuẩn của ngành
- C. Cách fine-tune
- D. Một loại vector database

**[L2]** Vì sao đánh giá LLM khó hơn đánh giá một classifier nhị phân?

- A. Vì LLM chạy chậm hơn
- B. Vì đầu ra là văn bản mở, không chỉ đúng/sai — cần đo nhiều chiều như độ liên quan, mạch lạc, độ trung thực với nguồn **(✓)**
- C. Vì không có metric nào tồn tại
- D. Vì LLM không thể đo được

**[L3]** Với một hệ RAG, metric nào phản ánh trực tiếp việc đầu ra có “bám” vào tài liệu truy xuất hay không?

- A. Latency
- B. Faithfulness/groundedness (độ trung thực với context đã truy xuất) **(✓)**
- C. Throughput
- D. VRAM sử dụng

-----

### Nhóm 7 — Deployment & Optimization

**[L1]** Quantization (lượng tử hóa) mô hình nhằm mục đích gì?

- A. Tăng độ chính xác tuyệt đối
- B. Giảm kích thước/bộ nhớ và tăng tốc inference, đổi lại có thể giảm nhẹ chất lượng **(✓)**
- C. Huấn luyện nhanh hơn
- D. Tăng số tham số

**[L2]** Khi nào nên cân nhắc dùng mô hình open-source fine-tuned chạy nội bộ thay vì gọi API proprietary đắt tiền?

- A. Khi mô hình nhỏ đã fine-tune đạt độ chính xác đủ cho tác vụ với chi phí thấp hơn nhiều **(✓)**
- B. Luôn luôn, bất kể chất lượng
- C. Chỉ khi không có internet
- D. Không bao giờ

**[L3]** Chỉ đánh giá một mô hình đã quantize bằng perplexity là chưa đủ. Vì sao?

- A. Perplexity không tính được
- B. Cần so với các eval theo domain/tác vụ thực tế để biết chất lượng thực sự thay đổi ra sao **(✓)**
- C. Perplexity luôn sai
- D. Vì quantization không ảnh hưởng chất lượng

-----

### Nhóm 8 — Đạo đức & Quản trị

**[L1]** Đâu là các vấn đề đạo đức cốt lõi khi triển khai AI?

- A. Chỉ có chi phí
- B. Thiên kiến (bias), công bằng, quyền riêng tư, trách nhiệm giải trình, tính minh bạch/giải thích được **(✓)**
- C. Chỉ có tốc độ
- D. Không có vấn đề nào

**[L2]** Trong ngành được quản lý chặt (y tế, tài chính), yêu cầu nào với đầu ra AI là tối quan trọng?

- A. Đầu ra dài hơn
- B. Khả năng truy vết/grounding chặt vào nguồn đáng tin và giải thích được quyết định **(✓)**
- C. Tốc độ phản hồi nhanh nhất
- D. Dùng mô hình lớn nhất

-----

## 4. Chấm điểm & lập lộ trình

Chấm điểm **theo từng nhóm** (tỷ lệ % đúng trong nhóm), không gộp tổng.

|Mức điểm nhóm|Ý nghĩa                    |Hành động                        |
|-------------|---------------------------|---------------------------------|
|< 50%        |Hổng nền tảng nhóm này     |Ưu tiên đào tạo cơ bản (L1) trước|
|50–75%       |Nắm cơ bản, thiếu chiều sâu|Bổ sung nội dung L2/L3           |
|> 75%        |Đủ năng lực                |Có thể làm mentor nhóm đó        |

**Lộ trình team:** nhóm có điểm trung bình thấp nhất toàn team → đào tạo chung trước.
**Lộ trình cá nhân:** mỗi người dựa trên radar 8 trục của riêng mình.

**Gợi ý bổ sung:** giữ riêng 1–2 câu tự đánh giá (“bạn tự tin mức nào với RAG?”) để so sánh độ lệch giữa tự đánh giá và điểm khách quan — độ lệch lớn là tín hiệu cần lưu ý khi giao việc.

-----

## 5. Bảng tra cứu nguồn biên soạn câu hỏi

> Dùng làm checklist khi soạn ngân hàng câu hỏi cho từng nhóm. Ưu tiên tài liệu chính chủ (Anthropic / Google / Hugging Face). **Lưu ý:** URL tài liệu chính chủ có thể thay đổi theo thời gian (ví dụ domain docs Anthropic đang dịch chuyển) — hãy mở link xác nhận trước khi trích dẫn.

|Nhóm                        |Chủ đề con nên ra câu                                                                          |Nguồn ưu tiên (đã xác minh)                                                                                                                                                                                                                                                     |
|----------------------------|-----------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|1. Nền tảng AI/LLM          |tokens, embeddings, transformer, next-token prediction, hallucination                          |HF – Semantic similarity LoRA (cosine similarity): `huggingface.co/docs/peft/main/en/task_guides/semantic-similarity-lora` · LLM Systems Engineering Roadmap (GitHub h9-tec)                                                                                                    |
|2. Prompt Engineering       |clarity, multishot, XML, role prompting, CoT, prompt chaining                                  |Anthropic – Prompt engineering overview: `docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview` · Prompting best practices: `.../prompt-engineering/claude-4-best-practices` · Interactive tutorial: `github.com/anthropics/prompt-eng-interactive-tutorial`|
|3. RAG                      |grounding, chunking, embedding/indexing, retrieval, reranking, citation                        |Google Codelab – Building Agents with RAG: `codelabs.developers.google.com/.../building-agents-with-retrieval-augmented-generation` · LLM Systems Engineering Roadmap (GitHub h9-tec)                                                                                           |
|4. Fine-tuning              |PEFT vs full, LoRA, QLoRA, target_modules, rank                                                |HF PEFT – LoRA methods: `huggingface.co/docs/peft/en/task_guides/lora_based_methods` · HF Transformers – PEFT/QLoRA: `huggingface.co/docs/transformers/en/peft` · PEFT repo: `github.com/huggingface/peft`                                                                      |
|5. AI Agents                |tool/function calling, reasoning-action loop, multi-agent, self-correction, context engineering|Anthropic – Effective context engineering: `anthropic.com/engineering/effective-context-engineering-for-ai-agents` · Agent benchmarks (arXiv 2508.18646): AgentBench, API-Bank, AgentBoard                                                                                      |
|6. Evaluation               |LLM-as-judge, RAG eval (2 tầng), faithfulness/grounding, hallucination baseline                |Anthropic – Eval Tool: `docs.anthropic.com/en/docs/test-and-evaluate/eval-tool` · Adaline – Guide to LLM & Agent Evaluation 2026 · LLM Monitoring Best Practices (TruLens/Ragas)                                                                                                |
|7. Deployment & Optimization|quantization, proprietary vs open-source, prompt caching, batch, rate limit                    |Anthropic Academy – Build with Claude: `anthropic.com/learn/build-with-claude` · LLM Systems Engineering Roadmap (GitHub h9-tec)                                                                                                                                                |
|8. Đạo đức & Quản trị       |bias, fairness, privacy, accountability, transparency/explainability                           |AI literacy & competency frameworks – Taylor & Francis (2025)                                                                                                                                                                                                                   |

**Nguyên tắc biên soạn:**

1. Mỗi câu nên truy được về một nguồn chính chủ hoặc học thuật; ghi chú nguồn cạnh đáp án để dễ rà soát.
1. Lĩnh vực thay đổi nhanh — review ngân hàng câu hỏi mỗi 6 tháng (đặc biệt nhóm Deployment/Agents: tên mô hình, giá, best practices lỗi thời nhanh).
1. Tránh blog SEO không nguồn cho câu hỏi cốt lõi; chỉ dùng để tham khảo cách diễn đạt rồi đối chiếu lại tài liệu chính chủ.
1. *Chưa có URL OpenAI cụ thể trong tài liệu này* — nếu cần nguồn OpenAI cho nhóm 1/7, tra trực tiếp tại `platform.openai.com/docs`.

-----

## 6. Nguồn tham khảo

- AI Literacy Assessment Matrix & Development Canvas — ScienceDirect (2025): khung 3 chiều khái niệm/thực hành/đạo đức, phân hóa theo vai trò.
- AI literacy and competency frameworks — Taylor & Francis (2025): các chiều đạo đức (bias, fairness, privacy, accountability, transparency).
- “How to Assess AI Literacy: Misalignment Between Self-Reported and Objective-Based Measures” — arXiv: cảnh báo lệch giữa tự đánh giá và đo khách quan.
- LLM Systems Engineering Roadmap — GitHub (h9-tec): pipeline RAG, chunking, reranking, faithfulness, quantization.
- “How to Become an LLM Engineer: Skills & Roadmap” — Applied AI Course (2026): RAG, fine-tuning, LLM-as-a-Judge, tokenomics.
- IBM — RAG vs fine-tuning vs prompt engineering (2025): phân biệt 3 kỹ thuật tối ưu LLM.
- Anthropic Docs — Prompt engineering, Eval Tool, Effective context engineering for AI agents.
- Google Codelabs — Building Agents with Retrieval-Augmented Generation (khái niệm grounding).
- Hugging Face Docs — PEFT (LoRA/QLoRA), semantic similarity LoRA.
- Beyond Benchmark (arXiv 2508.18646) — benchmark đánh giá Agent (AgentBench, API-Bank, AgentBoard).
- Adaline (2026) & LLM Monitoring Best Practices — RAG evaluation 2 tầng, hallucination baseline, TruLens/Ragas.