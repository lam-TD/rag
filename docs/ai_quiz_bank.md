# Ngân hàng câu hỏi đánh giá năng lực AI — 80 câu

> 8 nhóm × 10 câu. Mỗi câu đánh dấu mức độ [L1/L2/L3], đáp án đúng **(✓)**, và nguồn trích dẫn.
> Đối tượng: team engineers. Dùng kèm file khung trắc nghiệm để chấm theo nhóm.

**Lưu ý nguồn:** Các URL Anthropic dùng domain hiện hành `platform.claude.com/docs` (đã xác minh 06/2026). Nội dung câu hỏi bám theo tài liệu chính chủ; vẫn nên mở link rà soát trước khi phát hành vì tài liệu thay đổi nhanh.

-----

## Nhóm 1 — Nền tảng AI/LLM

**1. [L1]** “Token” trong LLM là gì?

- A. Một câu hoàn chỉnh
- B. Đơn vị văn bản nhỏ (từ/mảnh từ/ký tự) mà mô hình xử lý **(✓)**
- C. Một tham số mạng neural
- D. Một khóa API

> Nguồn: Anthropic Glossary — `platform.claude.com/docs/en/about-claude/glossary`

**2. [L1]** Embedding biểu diễn văn bản dưới dạng gì?

- A. Chuỗi ký tự nén
- B. Vector số trong không gian nhiều chiều, nơi văn bản gần nghĩa nằm gần nhau **(✓)**
- C. Cây cú pháp
- D. Bảng băm

> Nguồn: HF — Semantic similarity LoRA: `huggingface.co/docs/peft/main/en/task_guides/semantic-similarity-lora`

**3. [L1]** Độ tương đồng giữa hai embedding thường được đo bằng?

- A. Khoảng cách Hamming
- B. Cosine similarity **(✓)**
- C. Số từ chung
- D. Độ dài chuỗi

> Nguồn: HF — Semantic similarity LoRA (cosine similarity: score 1 = liên quan, ≤ 0 = không liên quan)

**4. [L1]** LLM decoder-only sinh văn bản chủ yếu bằng cơ chế nào?

- A. Tra cứu cơ sở dữ liệu
- B. Dự đoán token kế tiếp dựa trên xác suất **(✓)**
- C. So khớp mẫu chính xác
- D. Dịch quy tắc

> Nguồn: khái niệm next-token prediction (LLM Systems Engineering Roadmap, GitHub h9-tec)

**5. [L2]** Vì sao LLM có thể “hallucinate” (bịa thông tin sai nhưng nghe hợp lý)?

- A. Vì thiếu RAM
- B. Vì sinh văn bản theo xác suất thống kê, không tra cứu sự thật cố định **(✓)**
- C. Vì temperature luôn bằng 0
- D. Vì context window quá lớn

> Nguồn: Anthropic — Reduce hallucinations: `platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations`

**6. [L2]** Vì sao embedding cho phép semantic search tốt hơn so khớp từ khóa?

- A. Vì loại bỏ stopwords
- B. Vì biểu diễn ý nghĩa thành vector nên bắt được văn bản gần nghĩa dù khác từ **(✓)**
- C. Vì nén dữ liệu
- D. Vì luôn chính xác tuyệt đối

> Nguồn: HF — Semantic similarity LoRA

**7. [L2]** “Context window” của LLM là gì?

- A. Giao diện chat
- B. Lượng token tối đa mô hình xử lý được trong một lần (input + output) **(✓)**
- C. Số mô hình chạy song song
- D. Thời gian phản hồi

> Nguồn: Anthropic Glossary

**8. [L2]** Tham số “temperature” ảnh hưởng đầu ra thế nào?

- A. Tăng tốc độ
- B. Điều chỉnh độ ngẫu nhiên/đa dạng của đầu ra (thấp = xác định hơn) **(✓)**
- C. Giảm chi phí token
- D. Tăng context window

> Nguồn: Anthropic Glossary / Messages API docs

**9. [L3]** Một mô hình đạt training loss rất thấp. Kết luận nào ĐÚNG?

- A. Đầu ra luôn đúng sự thật
- B. Loss thấp không đảm bảo đầu ra đúng sự thật; mô hình vẫn có thể hallucinate **(✓)**
- C. Mô hình không cần đánh giá thêm
- D. Mô hình đã hết overfitting

> Nguồn: Anthropic — Reduce hallucinations (ngay mô hình tiên tiến vẫn sinh thông tin sai)

**10. [L3]** Vì sao tính toán trên embedding (vector) hiệu quả cho tìm kiếm quy mô lớn?

- A. Vì vector luôn nhỏ hơn văn bản gốc
- B. Vì có thể đánh chỉ mục và so độ tương đồng nhanh giữa hàng triệu vector **(✓)**
- C. Vì không cần lưu trữ
- D. Vì vector không đổi theo mô hình

> Nguồn: HF — Semantic similarity LoRA (tạo search index từ embedding sản phẩm)

-----

## Nhóm 2 — Prompt Engineering

**11. [L1]** Trước khi prompt engineering, Anthropic khuyên cần có sẵn 3 thứ. Đâu là một trong số đó?

- A. Một mô hình fine-tuned
- B. Tiêu chí thành công rõ ràng cho use case **(✓)**
- C. GPU riêng
- D. Vector database

> Nguồn: Anthropic — Prompt engineering overview: `platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview`

**12. [L1]** “Few-shot / multishot prompting” nghĩa là gì?

- A. Gọi mô hình nhiều lần
- B. Cung cấp ví dụ mẫu trong prompt để định hướng đầu ra **(✓)**
- C. Giảm số token
- D. Tắt system prompt

> Nguồn: Anthropic — Effective context engineering: `anthropic.com/engineering/effective-context-engineering-for-ai-agents`

**13. [L1]** Anthropic khuyến nghị cấu trúc prompt bằng kỹ thuật nào?

- A. Viết liền một đoạn không xuống dòng
- B. Dùng XML tags hoặc Markdown headers để phân tách các phần **(✓)**
- C. Viết hoa toàn bộ
- D. Chỉ dùng emoji

> Nguồn: Anthropic — Effective context engineering (tổ chức thành `<background>`, `<instructions>`…)

**14. [L2]** Khi nào prompt engineering KHÔNG phải giải pháp tốt nhất?

- A. Khi cần định dạng đầu ra
- B. Khi vấn đề là latency/chi phí — đôi khi đổi mô hình hiệu quả hơn **(✓)**
- C. Khi cần vai trò cho mô hình
- D. Khi viết hướng dẫn rõ ràng

> Nguồn: Anthropic — Prompt engineering overview (“When to prompt engineer”)

**15. [L2]** Để giảm hallucination, kỹ thuật prompt cơ bản nào được khuyến nghị?

- A. Tăng temperature
- B. Cho phép mô hình nói “tôi không biết” **(✓)**
- C. Yêu cầu trả lời dài hơn
- D. Bỏ system prompt

> Nguồn: Anthropic — Reduce hallucinations (“Allow Claude to say I don’t know”)

**16. [L2]** Với tài liệu dài (>20k token), cách grounding nào được khuyến nghị để giảm bịa?

- A. Tóm tắt thật ngắn
- B. Yêu cầu trích nguyên văn (word-for-word quotes) trước khi xử lý **(✓)**
- C. Chia mô hình nhỏ
- D. Tăng max_tokens

> Nguồn: Anthropic — Reduce hallucinations (“Use direct quotes for factual grounding”)

**17. [L2]** Một lỗi thường gặp khi thiết kế tool cho agent là gì?

- A. Quá ít tool
- B. Bộ tool phình to, gây mơ hồ về việc nên dùng tool nào **(✓)**
- C. Tool có tên rõ ràng
- D. Tool có mô tả đầy đủ

> Nguồn: Anthropic — Effective context engineering (bloated tool sets)

**18. [L3]** “Chain-of-thought verification” để giảm hallucination hoạt động thế nào?

- A. Chạy nhiều mô hình
- B. Yêu cầu mô hình giải thích lập luận từng bước trước khi kết luận, để lộ logic sai **(✓)**
- C. Tăng temperature
- D. Nén prompt

> Nguồn: Anthropic — Reduce hallucinations (“Advanced techniques”)

**19. [L3]** “Best-of-N verification” phát hiện hallucination bằng cách nào?

- A. Chọn câu trả lời dài nhất
- B. Chạy cùng prompt nhiều lần và so sánh; mâu thuẫn giữa các đầu ra báo hiệu hallucination **(✓)**
- C. Giảm số lần gọi
- D. Dùng mô hình nhỏ hơn

> Nguồn: Anthropic — Reduce hallucinations (“Best-of-N verification”)

**20. [L3]** Để câu trả lời “auditable” (kiểm chứng được), Anthropic gợi ý gì?

- A. Ẩn nguồn
- B. Buộc mô hình trích dẫn nguồn/quote cho mỗi luận điểm; nếu không tìm được quote thì rút lại luận điểm **(✓)**
- C. Trả lời thật nhanh
- D. Tránh trích dẫn để ngắn gọn

> Nguồn: Anthropic — Reduce hallucinations (“Verify with citations”)

-----

## Nhóm 3 — RAG

**21. [L1]** RAG là viết tắt của?

- A. Rapid AI Generation
- B. Retrieval-Augmented Generation **(✓)**
- C. Recursive Agent Grounding
- D. Ranked Answer Generation

> Nguồn: Google Codelab — Building Agents with RAG

**22. [L1]** “Grounding” trong RAG nghĩa là gì?

- A. Tắt mô hình khi lỗi
- B. Cung cấp ngữ cảnh factual cho LLM để bám vào khi trả lời **(✓)**
- C. Huấn luyện lại mô hình
- D. Nén vector

> Nguồn: Google Codelab — Building Agents with RAG (“providing factual context = grounding”)

**23. [L1]** Vai trò chính của vector database trong RAG?

- A. Huấn luyện mô hình
- B. Lưu và truy xuất embedding theo độ tương đồng ngữ nghĩa **(✓)**
- C. Thay thế LLM
- D. Quản lý người dùng

> Nguồn: LLM Systems Engineering Roadmap (GitHub h9-tec)

**24. [L1]** Thứ tự đúng của pipeline RAG cơ bản?

- A. embedding → chunking → retrieval → generation
- B. documents → chunking → embedding → indexing → retrieval → generation **(✓)**
- C. retrieval → embedding → chunking → generation
- D. generation → retrieval → chunking

> Nguồn: LLM Systems Engineering Roadmap (GitHub h9-tec)

**25. [L2]** Vì sao RAG thường giảm được thông tin sai/lỗi thời so với LLM thuần?

- A. Vì mô hình lớn hơn
- B. Vì đưa ngữ cảnh factual cập nhật vào, như một “bài thi mở sách” **(✓)**
- C. Vì tăng temperature
- D. Vì bỏ qua retrieval

> Nguồn: Google Codelab — Building Agents with RAG (“open-book exam”)

**26. [L2]** Với tài liệu pháp lý dài nhiều điều khoản, chiến lược chunking nào phù hợp hơn?

- A. Cắt cố định 100 ký tự bất kể nội dung
- B. Chunk theo cấu trúc ngữ nghĩa (theo điều/khoản) kèm overlap **(✓)**
- C. Một chunk cho cả tài liệu
- D. Chunk ngẫu nhiên

> Nguồn: LLM Systems Engineering Roadmap (chunking kém gây mất ngữ cảnh)

**27. [L2]** Khi nào nên dùng hybrid search (keyword + semantic)?

- A. Khi truy vấn chứa mã ID, tên riêng, tham chiếu chính xác cần so khớp từ khóa **(✓)**
- B. Chỉ khi thiếu vector database
- C. Khi muốn giảm chi phí embedding
- D. Không bao giờ

> Nguồn: LLM Systems Engineering Roadmap

**28. [L3]** Hệ RAG trả lời sai dù tài liệu CÓ chứa câu trả lời đúng. Nguyên nhân gốc khả dĩ nhất?

- A. Temperature quá thấp
- B. Chunking kém khiến retriever không lấy được đoạn chứa đáp án **(✓)**
- C. LLM quá lớn
- D. Quá nhiều dữ liệu trong DB

> Nguồn: LLM Systems Engineering Roadmap (chunking kém → truy xuất sai, hallucination)

**29. [L3]** Mục đích của bước reranking sau retrieval?

- A. Giảm số tài liệu index
- B. Sắp xếp lại các đoạn đã truy xuất theo độ liên quan thực sự với truy vấn **(✓)**
- C. Tạo embedding mới
- D. Thay generation

> Nguồn: LLM Systems Engineering Roadmap (pipeline có bước reranking)

**30. [L3]** Trong ngành quản lý chặt, vì sao citation/trích nguồn trong RAG đặc biệt quan trọng?

- A. Để câu trả lời dài hơn
- B. Để câu trả lời kiểm chứng được, truy vết về nguồn đáng tin **(✓)**
- C. Để tăng tốc
- D. Để giảm token

> Nguồn: Anthropic — Reduce hallucinations (“Verify with citations”)

-----

## Nhóm 4 — Fine-tuning

**31. [L1]** PEFT là viết tắt của?

- A. Pre-trained Embedding Fine-Tuning
- B. Parameter-Efficient Fine-Tuning **(✓)**
- C. Partial Encoder Fine-Tuning
- D. Predictive Feature Training

> Nguồn: HF PEFT — `huggingface.co/docs/peft`

**32. [L1]** Ý tưởng cốt lõi của PEFT so với full fine-tuning?

- A. Huấn luyện lại toàn bộ tham số
- B. Chỉ huấn luyện một phần nhỏ tham số (adapter), giữ đông phần còn lại **(✓)**
- C. Không cần dữ liệu
- D. Chỉ chạy trên CPU

> Nguồn: HF PEFT — wrap model bằng PeftModel, chỉ train adapter

**33. [L1]** LoRA giảm số tham số huấn luyện bằng cách nào?

- A. Xóa bớt layer
- B. Phân rã ma trận cập nhật trọng số thành hai ma trận nhỏ (low-rank) **(✓)**
- C. Lượng tử hóa toàn bộ
- D. Cắt dữ liệu

> Nguồn: HF PEFT — LoRA methods: `huggingface.co/docs/peft/en/task_guides/lora_based_methods`

**34. [L2]** Tham số “rank (r)” trong LoRA ảnh hưởng gì?

- A. Không ảnh hưởng
- B. Rank cao hơn = nhiều tham số huấn luyện hơn và khả năng học lớn hơn **(✓)**
- C. Chỉ ảnh hưởng tốc độ inference
- D. Quyết định context window

> Nguồn: HF PEFT — LoRA methods (rank quyết định kích thước ma trận low-rank)

**35. [L2]** “target_modules” trong LoraConfig dùng để làm gì?

- A. Chọn dataset
- B. Xác định vị trí (layer) chèn các ma trận LoRA, ví dụ q_proj, v_proj **(✓)**
- C. Đặt learning rate
- D. Chọn tokenizer

> Nguồn: HF PEFT — LoRA methods / TRL PEFT integration

**36. [L2]** Khi nào nên ưu tiên fine-tuning hơn RAG?

- A. Khi dữ liệu thay đổi hằng ngày
- B. Khi cần mô hình học phong cách/định dạng đặc thù ổn định mà prompt khó ép **(✓)**
- C. Khi chỉ cần cập nhật kiến thức sự thật mới
- D. Khi muốn tránh mọi chi phí train

> Nguồn: IBM — RAG vs fine-tuning vs prompt engineering (2025)

**37. [L3]** QLoRA tiết kiệm bộ nhớ bằng cách nào?

- A. Bỏ qua huấn luyện
- B. Dùng base model lượng tử hóa (quantized) làm nền rồi áp LoRA lên trên **(✓)**
- C. Chỉ dùng CPU
- D. Xóa dữ liệu

> Nguồn: HF Transformers — PEFT: `huggingface.co/docs/transformers/en/peft`

**38. [L3]** Lợi ích lưu trữ khi fine-tune bằng LoRA/PEFT là gì?

- A. Phải lưu cả mô hình đầy đủ mỗi lần
- B. Chỉ lưu adapter (vài MB) thay vì toàn mô hình (nhiều GB) **(✓)**
- C. Không lưu được
- D. Lưu gấp đôi

> Nguồn: HF TRL — PEFT integration (save adapters ~few MB)

**39. [L3]** Một nhược điểm có thể gặp khi inference với LoRA?

- A. Không thể load mô hình
- B. Có thể tăng latency do load riêng base model và adapter **(✓)**
- C. Luôn chậm hơn 10 lần
- D. Mất toàn bộ kiến thức gốc

> Nguồn: HF PEFT — LoRA developer guide (latency khi load riêng base + adapter)

**40. [L2]** PEFT có hỗ trợ kỹ thuật nào ngoài LoRA?

- A. Không, chỉ LoRA
- B. Có: prompt tuning, prefix tuning, adapter tuning, AdaLoRA… **(✓)**
- C. Chỉ full fine-tuning
- D. Chỉ quantization

> Nguồn: HF PEFT — LoRA methods (LoHa, LoKr, AdaLoRA, prompt/prefix tuning)

-----

## Nhóm 5 — AI Agents

**41. [L1]** “Tool calling / function calling” trong agent là gì?

- A. Gọi một mô hình thay thế
- B. LLM quyết định gọi hàm/công cụ bên ngoài (API, search, tính toán) **(✓)**
- C. Một loại prompt cố định
- D. Cách nén mô hình

> Nguồn: Anthropic — Tool use docs / Effective context engineering

**42. [L1]** “Context engineering” khác “prompt engineering” ở điểm nào?

- A. Giống hệt nhau
- B. Là chiến lược quản lý toàn bộ tập token (context) trong inference, rộng hơn việc viết prompt **(✓)**
- C. Chỉ áp dụng khi train
- D. Không liên quan agent

> Nguồn: Anthropic — Effective context engineering for AI agents

**43. [L2]** Nguyên tắc thiết kế bộ tool tốt cho agent?

- A. Càng nhiều tool càng tốt
- B. Curate bộ tool tối thiểu khả dụng, tránh chồng chéo gây mơ hồ **(✓)**
- C. Mỗi tool làm nhiều việc
- D. Đặt tên tool mơ hồ cho linh hoạt

> Nguồn: Anthropic — Effective context engineering (“minimal viable set of tools”)

**44. [L2]** Bài toán nhiều bước (tra cứu → tính toán → tổng hợp) hợp với pattern agent nào?

- A. Một prompt duy nhất không chia bước
- B. Vòng lặp reasoning + action (gọi tool) lặp đến khi đủ thông tin **(✓)**
- C. Tăng max_tokens
- D. Fine-tune lại

> Nguồn: khái niệm reasoning-action loop (Agent benchmarks, arXiv 2508.18646)

**45. [L2]** Phép thử “nếu kỹ sư người không xác định được nên dùng tool nào thì…” dẫn đến kết luận gì?

- A. Agent sẽ tự suy ra được
- B. Agent cũng không thể làm tốt hơn — cần thiết kế tool rõ ràng **(✓)**
- C. Thêm nhiều tool hơn
- D. Tăng temperature

> Nguồn: Anthropic — Effective context engineering

**46. [L2]** AgentBench dùng để đánh giá agent ở các môi trường nào?

- A. Chỉ toán học
- B. Coding, gaming, web (đa môi trường) **(✓)**
- C. Chỉ dịch thuật
- D. Chỉ tóm tắt

> Nguồn: Agent benchmarks (arXiv 2508.18646)

**47. [L3]** Self-correction loop trong agent có tác dụng gì?

- A. Tăng tốc phản hồi
- B. Cho agent tự rà soát/đánh giá đầu ra trước khi trả về, giảm lỗi **(✓)**
- C. Giảm token
- D. Thay evaluation

> Nguồn: khái niệm self-correction (LLM Systems Engineering Roadmap)

**48. [L3]** API-Bank là benchmark tập trung đánh giá điều gì?

- A. Tốc độ embedding
- B. Khả năng agent gọi tool/API trong các kịch bản **(✓)**
- C. Chất lượng dịch
- D. Kích thước mô hình

> Nguồn: Agent benchmarks (arXiv 2508.18646)

**49. [L3]** Vì sao quản lý context qua các lượt tương tác dài lại quan trọng với agent?

- A. Không quan trọng
- B. Vì cần cắt tỉa/duy trì context tối ưu để agent ổn định qua nhiều bước **(✓)**
- C. Vì giảm số tool
- D. Vì tăng temperature

> Nguồn: Anthropic — Effective context engineering (pruning context over long interactions)

**50. [L3]** AgentBoard nhấn mạnh đo lường khía cạnh nào của agent?

- A. Chỉ độ dài đầu ra
- B. Đa nhiệm và độ chính xác grounding **(✓)**
- C. Chi phí GPU
- D. Tốc độ mạng

> Nguồn: Agent benchmarks (arXiv 2508.18646)

-----

## Nhóm 6 — Evaluation

**51. [L1]** “LLM-as-a-Judge” nghĩa là gì?

- A. Một benchmark chuẩn
- B. Dùng một LLM để chấm điểm đầu ra theo tiêu chí định sẵn **(✓)**
- C. Một loại fine-tuning
- D. Một vector database

> Nguồn: Adaline — Guide to LLM & Agent Evaluation (2026)

**52. [L1]** Anthropic khuyên trước khi cải thiện prompt cần có gì để đánh giá?

- A. GPU lớn
- B. Cách kiểm thử thực nghiệm (eval) đối chiếu tiêu chí thành công **(✓)**
- C. Vector DB
- D. Fine-tuned model

> Nguồn: Anthropic — Prompt engineering overview / Define success and build evaluations

**53. [L1]** Trong Eval Tool của Anthropic Console, prompt cần có yếu tố nào để tạo test set?

- A. Ít nhất 5 tool
- B. Ít nhất 1–2 biến động dạng `{{variable}}` **(✓)**
- C. Một fine-tuned model
- D. Một API key trả phí

> Nguồn: Anthropic — Using the Evaluation Tool: `platform.claude.com/docs/en/test-and-evaluate/eval-tool`

**54. [L2]** Vì sao đánh giá LLM khó hơn classifier nhị phân?

- A. LLM chạy chậm
- B. Đầu ra là văn bản mở, cần đo nhiều chiều (liên quan, mạch lạc, trung thực) **(✓)**
- C. Không có metric nào
- D. LLM không đo được

> Nguồn: Adaline — Guide to LLM & Agent Evaluation (2026)

**55. [L2]** Đánh giá RAG phức tạp hơn vì sao?

- A. Vì chỉ có một thành phần
- B. Vì phải kiểm cả hai phần: retrieval và generation **(✓)**
- C. Vì không cần human review
- D. Vì không đo được

> Nguồn: Adaline — Guide to LLM & Agent Evaluation (2026)

**56. [L2]** “Faithfulness / groundedness” đo điều gì trong hệ RAG?

- A. Tốc độ phản hồi
- B. Mức độ đầu ra bám sát context đã truy xuất **(✓)**
- C. Số token
- D. VRAM

> Nguồn: Adaline (2026) / LLM Monitoring Best Practices
> **57. [L2]** Khi nào nên kết hợp LLM-as-judge với human review?

- A. Không bao giờ kết hợp
- B. Tự động chấm bằng LLM-as-judge, dùng human review cho phán đoán chủ quan **(✓)**
- C. Chỉ human, không máy
- D. Chỉ máy, không người

> Nguồn: Adaline — Guide to LLM & Agent Evaluation (2026)

**58. [L3]** Công cụ nào được nêu để tự động kiểm tra retrieval grounding của RAG?

- A. Photoshop
- B. TruLens hoặc Ragas **(✓)**
- C. Excel
- D. Git

> Nguồn: LLM Monitoring Best Practices

**59. [L3]** Khi mới đưa hệ RAG vào vận hành, nên làm gì trong vài tuần đầu?

- A. Bỏ qua giám sát
- B. Thiết lập baseline tỷ lệ hallucination để theo dõi **(✓)**
- C. Tắt logging
- D. Tăng temperature

> Nguồn: LLM Monitoring Best Practices

**60. [L3]** Cách dùng quote để mô hình tự kiểm chứng (giảm hallucination) hoạt động ra sao?

- A. Bỏ trích dẫn
- B. Sau khi trả lời, buộc mô hình tìm quote hỗ trợ; không có quote thì rút luận điểm **(✓)**
- C. Trả lời nhanh hơn
- D. Dùng mô hình nhỏ

> Nguồn: Anthropic — Reduce hallucinations (“Verify with citations”)

-----

## Nhóm 7 — Deployment & Optimization

**61. [L1]** Quantization (lượng tử hóa) mô hình nhằm mục đích chính gì?

- A. Tăng số tham số
- B. Giảm bộ nhớ/kích thước và tăng tốc inference, đổi lại có thể giảm nhẹ chất lượng **(✓)**
- C. Huấn luyện nhanh hơn từ đầu
- D. Tăng context window

> Nguồn: LLM Systems Engineering Roadmap (GitHub h9-tec)

**62. [L1]** “Prompt caching” của Anthropic giúp gì?

- A. Tăng độ dài đầu ra
- B. Tái sử dụng phần context để tối ưu hiệu năng và giảm chi phí **(✓)**
- C. Đổi mô hình tự động
- D. Mã hóa dữ liệu

> Nguồn: Anthropic Academy — Build with Claude (prompt caching): `anthropic.com/learn/build-with-claude`

**63. [L1]** “Batch API” phù hợp cho trường hợp nào?

- A. Phản hồi thời gian thực
- B. Xử lý khối lượng lớn yêu cầu không cần phản hồi tức thì **(✓)**
- C. Streaming từng token
- D. Fine-tuning

> Nguồn: Anthropic Docs — Batch API (nêu trong Build with Claude)

**64. [L2]** Khi nào cân nhắc mô hình open-source fine-tuned chạy nội bộ thay vì API proprietary đắt?

- A. Luôn luôn bất kể chất lượng
- B. Khi mô hình nhỏ đã fine-tune đạt độ chính xác đủ cho tác vụ với chi phí thấp hơn **(✓)**
- C. Chỉ khi mất internet
- D. Không bao giờ

> Nguồn: IBM — RAG vs fine-tuning vs prompt engineering (2025); LLM Systems Engineering Roadmap

**65. [L2]** Anthropic lưu ý latency và cost đôi khi giải quyết tốt hơn bằng cách nào (thay vì prompt)?

- A. Tăng temperature
- B. Chọn một mô hình khác phù hợp hơn **(✓)**
- C. Thêm nhiều ví dụ
- D. Bỏ system prompt

> Nguồn: Anthropic — Prompt engineering overview (“When to prompt engineer”)

**66. [L2]** Lợi ích triển khai của adapter LoRA nhỏ là gì?

- A. Phải deploy lại toàn bộ mô hình
- B. Có thể lưu/triển khai adapter nhẹ (vài MB), hoán đổi linh hoạt **(✓)**
- C. Không deploy được
- D. Tăng gấp đôi dung lượng

> Nguồn: HF TRL — PEFT integration (save adapters ~few MB)

**67. [L2]** “Streaming” đầu ra của LLM cải thiện trải nghiệm thế nào?

- A. Giảm độ chính xác
- B. Trả token dần khi sinh ra, giảm độ trễ cảm nhận **(✓)**
- C. Tăng chi phí gấp đôi
- D. Tắt tool use

> Nguồn: Anthropic Docs — Messages/streaming (Build with Claude)

**68. [L3]** Vì sao không nên chỉ dùng perplexity để đánh giá mô hình đã quantize?

- A. Perplexity không tính được
- B. Cần eval theo domain/tác vụ thực tế để biết chất lượng thực sự thay đổi ra sao **(✓)**
- C. Perplexity luôn sai
- D. Quantization không ảnh hưởng gì

> Nguồn: LLM Systems Engineering Roadmap (GitHub h9-tec)

**69. [L3]** Khi quantize để giảm chi phí, đánh đổi cần theo dõi là gì?

- A. Không có đánh đổi
- B. Khả năng giảm nhẹ chất lượng đầu ra — cần đo bằng eval thực tế **(✓)**
- C. Tăng context window
- D. Mất khả năng tool use

> Nguồn: LLM Systems Engineering Roadmap

**70. [L3]** Để chọn mô hình triển khai, cách tiếp cận hợp lý là gì?

- A. Luôn chọn mô hình lớn nhất
- B. Đối chiếu chất lượng/chi phí/latency theo eval của chính tác vụ **(✓)**
- C. Chọn ngẫu nhiên
- D. Chỉ dựa benchmark công khai

> Nguồn: Anthropic — Prompt engineering overview (cost/latency) + LLM Monitoring Best Practices

-----

## Nhóm 8 — Đạo đức & Quản trị

**71. [L1]** Đâu là các chiều đạo đức cốt lõi khi triển khai AI?

- A. Chỉ chi phí
- B. Bias, fairness, privacy, accountability, transparency/explainability **(✓)**
- C. Chỉ tốc độ
- D. Không có

> Nguồn: AI literacy & competency frameworks — Taylor & Francis (2025)

**72. [L1]** “Transparency / explainability” trong AI nghĩa là gì?

- A. Mô hình chạy nhanh
- B. Khả năng giải thích được cách/lý do hệ thống đưa ra kết quả **(✓)**
- C. Dùng mô hình mã nguồn mở
- D. Giá rẻ

> Nguồn: AI literacy & competency frameworks — Taylor & Francis (2025)

**73. [L2]** Vì sao “bias” trong dữ liệu/mô hình là vấn đề đạo đức?

- A. Vì làm chậm mô hình
- B. Vì có thể dẫn đến kết quả không công bằng cho một số nhóm **(✓)**
- C. Vì tăng chi phí
- D. Vì giảm context window

> Nguồn: AI literacy & competency frameworks — Taylor & Francis (2025)

**74. [L2]** Trong ngành quản lý chặt (y tế/tài chính), yêu cầu nào với đầu ra AI là tối quan trọng?

- A. Đầu ra dài hơn
- B. Truy vết/grounding chặt vào nguồn đáng tin và giải thích được quyết định **(✓)**
- C. Phản hồi nhanh nhất
- D. Dùng mô hình lớn nhất

> Nguồn: Anthropic — Reduce hallucinations (citations) + Taylor & Francis (2025)

**75. [L2]** “Accountability” trong quản trị AI đề cập điều gì?

- A. Tốc độ inference
- B. Trách nhiệm giải trình về quyết định/hậu quả của hệ thống AI **(✓)**
- C. Số tham số
- D. Giá API

> Nguồn: AI literacy & competency frameworks — Taylor & Francis (2025)

**76. [L2]** Vì sao “privacy” là mối quan tâm khi xây hệ AI dùng dữ liệu người dùng?

- A. Vì làm tăng latency
- B. Vì dữ liệu cá nhân cần được bảo vệ, tránh rò rỉ/lạm dụng **(✓)**
- C. Vì giảm độ chính xác
- D. Vì tốn GPU

> Nguồn: AI literacy & competency frameworks — Taylor & Francis (2025)

**77. [L1]** “Fairness” (công bằng) trong AI hướng tới điều gì?

- A. Chia đều GPU
- B. Hệ thống không phân biệt đối xử bất công giữa các nhóm người dùng **(✓)**
- C. Giá đồng nhất
- D. Tốc độ như nhau

> Nguồn: AI literacy & competency frameworks — Taylor & Francis (2025)

**78. [L2]** “Autonomy” như một chiều đạo đức AI liên quan đến điều gì?

- A. Mô hình tự train
- B. Mức độ AI hành động/tự quyết và tác động tới quyền tự chủ của con người **(✓)**
- C. Tự động scale server
- D. Tự đặt giá

> Nguồn: AI literacy & competency frameworks — Taylor & Francis (2025)

**79. [L3]** Khi agent có thể tự gọi tool và hành động, rủi ro quản trị nào tăng lên?

- A. Không có rủi ro mới
- B. Hành động ngoài ý muốn/khó kiểm soát — cần ràng buộc, giám sát và trách nhiệm giải trình **(✓)**
- C. Chỉ tăng chi phí
- D. Chỉ giảm tốc độ

> Nguồn: Taylor & Francis (2025) + Anthropic — Effective context engineering (tool design)

**80. [L3]** Cách kỹ thuật nào vừa giảm hallucination vừa hỗ trợ minh bạch/kiểm chứng?

- A. Tăng temperature
- B. Bắt buộc trích dẫn nguồn và cho mô hình tự rút luận điểm không có quote hỗ trợ **(✓)**
- C. Ẩn nguồn để gọn
- D. Bỏ qua đánh giá

> Nguồn: Anthropic — Reduce hallucinations (“Verify with citations”)

-----

## Nguồn trích dẫn (tổng hợp)

1. Anthropic — Prompt engineering overview: `platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview`
1. Anthropic — Prompting best practices: `platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices`
1. Anthropic — Reduce hallucinations: `platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations`
1. Anthropic — Using the Evaluation Tool: `platform.claude.com/docs/en/test-and-evaluate/eval-tool`
1. Anthropic — Effective context engineering for AI agents: `anthropic.com/engineering/effective-context-engineering-for-ai-agents`
1. Anthropic Academy — Build with Claude (prompt caching, batch, vision): `anthropic.com/learn/build-with-claude`
1. Google Codelab — Building Agents with Retrieval-Augmented Generation
1. Hugging Face PEFT — LoRA methods: `huggingface.co/docs/peft/en/task_guides/lora_based_methods`
1. Hugging Face Transformers — PEFT/QLoRA: `huggingface.co/docs/transformers/en/peft`
1. Hugging Face — Semantic similarity LoRA: `huggingface.co/docs/peft/main/en/task_guides/semantic-similarity-lora`
1. Hugging Face TRL — PEFT integration: `huggingface.co/docs/trl/en/peft_integration`
1. IBM — RAG vs fine-tuning vs prompt engineering (2025)
1. Agent benchmarks — arXiv 2508.18646 (AgentBench, API-Bank, AgentBoard)
1. Adaline — Guide to LLM & Agent Evaluation (2026)
1. AI literacy & competency frameworks — Taylor & Francis (2025)
1. LLM Systems Engineering Roadmap — GitHub (h9-tec)

> **Khuyến nghị rà soát:** một số câu (Batch API, streaming, AgentBoard/API-Bank chi tiết) bám theo mô tả nguồn nhưng nên mở link xác nhận trước khi phát hành chính thức, vì tài liệu chính chủ thay đổi nhanh. Câu nhóm 8 dựa trên khung khái niệm học thuật — diễn đạt lại theo ngữ cảnh công ty bạn nếu cần.