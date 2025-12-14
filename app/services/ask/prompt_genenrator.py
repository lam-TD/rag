from app.schemas.embedding import EmbeddingItem, EmbeddingItemReponse


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


def user_prompt():
    """
    You will answer a question based ONLY on the CONTEXT below.

    [QUESTION - ORIGINAL]
    {question}

    [METADATA]
    - Detected_question_language: {question_lang}      # e.g. "vi", "en", "ja"
    - answer_language: {answer_language}               # e.g. "auto", "vi", "en", "ja"

    [CONTEXT]
    You are given a list of context chunks from the user's documents.
    Each chunk has an ID and text content.

    {context_blocks}

    Each context block is formatted as:

    [ID] {context_id}
    SOURCE: {source_metadata}
    TEXT:
    {snippet}

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
    """


def build(query: str, hits: list[EmbeddingItem], min_sim: float = 0.25, max_chars: int = 4000):
    hits_filter = []
    for hit in hits:
        if hit.similarity >= min_sim:
            hits_filter.append(hit)

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]
    return messages, kept
