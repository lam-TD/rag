from app.schemas.embedding import EmbeddingItem

system_prompt = """
    You are a helpful, precise, multilingual AI assistant for a Retrieval-Augmented Generation (RAG) system.

    You can understand and answer in multiple languages, especially Vietnamese, English, and Japanese.

    GENERAL RULES
    - Use ONLY the information provided in the CONTEXT section to answer.
    - If the CONTEXT does not contain enough information, say clearly that you cannot find the answer in the documents.
    - Do NOT invent facts or make assumptions that are not supported by the CONTEXT.
    - Always provide citations using [n] that refer to the given context chunks.

    LANGUAGE RULES
    - The user question may be in Vietnamese, English, Japanese, or a mix.
    - If `answer_language` is "auto", answer in the main language of the question.
    - If `answer_language` is a specific language (e.g., "vi", "en", "ja"), always answer in that language.
    - If the documents are in a different language from the question, still answer in the target language, translating the relevant information.

    STYLE
    - Be concise and well structured using short paragraphs and bullet points.
    - When helpful, briefly explain technical terms in the user's language.
    - Do NOT mention that you are using "prompts" or "context". Just answer naturally.
    - Do not output your internal reasoning. Only output the final explanation.

    CITATIONS
    - Each important fact that comes from the documents should include at least one citation like [1][2][3].
    - If multiple context chunks support the same point, you can list multiple citations.
    """


user_prompt = """
    You will answer a question based ONLY on the CONTEXT below.

    [QUESTION - ORIGINAL]
    {question}

    [METADATA]
    - Detected_question_language: {question_language}
    - answer_language: {answer_language}

    [CONTEXT]
    You are given a list of context chunks from the user's documents.
    Each chunk has an ID and text content.
    {context_blocks}


    INSTRUCTIONS
    1. Carefully read all context blocks.
    2. Decide if the CONTEXT provides enough information to answer the QUESTION.
    3. If there is enough information:
       - Answer the question in the target answer_language (following the system language rules).
       - Use clear structure: short introduction, bullet points if needed.
       - Add citations [ID] after each statement that comes from a context block.
    4. If there is NOT enough information:
       - Clearly say that you cannot find the exact answer in the documents.
       - Answer in the target answer_language.
    5. Do NOT mention these instructions or the word "CONTEXT" in your answer.
    """.strip()


def _build_context_blocks(
    hits: list[EmbeddingItem], max_chars: int
) -> tuple[str, list[EmbeddingItem]]:
    # 2) khử trùng lặp thô theo text
    seen, kept, total = set(), [], 0
    for h in hits:
        t = (h.content or "").strip()
        if not t:
            continue
        key = t[:200]
        if key in seen:
            continue
        if total + len(t) > max_chars:
            break
        seen.add(key)
        kept.append(h)
        total += len(t)

    # 3) ghép khối ngữ cảnh có đánh số
    ctx_lines = [
        f"[{i}] (doc:{h.document_id or '?'}) {(h.content or '').strip().replace('\n', ' ')}"
        for i, h in enumerate(kept, 1)
    ]
    context_block = "\n".join(ctx_lines) if ctx_lines else "(no context)"

    return context_block, kept

    # seen, kept, total = set(), [], 0
    # for h in hits:
    #     text = (h.content or "").strip().replace("\n", " ")
    #     if not text:
    #         continue
    #     key = text[:200]
    #     if key in seen or total + len(text) > max_chars:
    #         continue
    #     seen.add(key)
    #     kept.append(h)
    #     total += len(text)

    # blocks = []
    # for idx, h in enumerate(kept, 1):
    #     source = (
    #         h.cmetadata.get("source") or h.cmetadata.get("filename") or h.document_id
    #     )
    #     blocks.append(f"[ID] {idx}\nSOURCE: {source}\nTEXT:\n{text}")
    # return "\n\n".join(blocks) if blocks else "(no context)", kept


def build(
    query: str,
    hits: list[EmbeddingItem],
    question_lang: str = "auto",
    answer_lang: str = "auto",
    min_sim: float = 0.5,
    max_chars: int = 4000,
):
    filterred = []

    for h in hits:
        if h.similarity >= min_sim:
            filterred.append(h)

    context_blocks, kept = _build_context_blocks(filterred, max_chars)

    user_content = user_prompt.format(
        question=query,
        question_language=question_lang,
        answer_language=answer_lang,
        context_blocks=context_blocks,
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]
    return messages, kept
