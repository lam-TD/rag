-- Enable pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- ===== Core entities =====
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    owner_id UUID NOT NULL,
    mime TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS document_versions (
    id UUID PRIMARY KEY,
    document_id UUID NOT NULL REFERENCES documents (id) ON DELETE CASCADE,
    version INT NOT NULL,
    object_url TEXT NOT NULL, -- e.g., s3 path or URL
    sha256 TEXT NOT NULL,
    lang TEXT,
    page_count INT,
    created_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE (document_id, version)
);

CREATE TABLE IF NOT EXISTS permissions (
    user_id UUID NOT NULL,
    document_id UUID NOT NULL REFERENCES documents (id) ON DELETE CASCADE,
    can_read BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (user_id, document_id)
);

-- ===== Chunks with embeddings (OpenAI text-embedding-3-large → 3072 dims) =====
CREATE TABLE IF NOT EXISTS chunks (
    id BIGSERIAL PRIMARY KEY,
    document_id UUID NOT NULL REFERENCES documents (id) ON DELETE CASCADE,
    version_id UUID NOT NULL REFERENCES document_versions (id) ON DELETE CASCADE,
    chunk_idx INT,
    text TEXT NOT NULL,
    embedding VECTOR (3072), -- để NULL tạm thời; worker sẽ cập nhật sau
    meta JSONB DEFAULT '{}'::jsonb
);

-- ===== Summaries =====
CREATE TABLE IF NOT EXISTS summaries (
    document_id UUID PRIMARY KEY REFERENCES documents (id) ON DELETE CASCADE,
    version_id UUID NOT NULL REFERENCES document_versions (id) ON DELETE CASCADE,
    outline TEXT,
    bullets TEXT,
    tags TEXT,
    abstract TEXT,
    generated_at TIMESTAMPTZ DEFAULT now()
);

-- ===== Query logging for eval =====
CREATE TABLE IF NOT EXISTS queries_log (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID,
    question TEXT,
    answer TEXT,
    citations JSONB,
    latency_ms INT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- ===== Indexes =====
-- Vector index (cosine)
CREATE INDEX IF NOT EXISTS idx_chunks_embedding_ivf ON chunks USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

CREATE INDEX IF NOT EXISTS idx_chunks_doc ON chunks (document_id);

CREATE INDEX IF NOT EXISTS idx_chunks_version ON chunks (version_id);

CREATE INDEX IF NOT EXISTS idx_docs_owner ON documents (owner_id);

CREATE INDEX IF NOT EXISTS idx_permissions_doc ON permissions (document_id);

-- Optional keyword search (bật sau nếu cần)
-- CREATE EXTENSION IF NOT EXISTS pg_trgm;
-- CREATE INDEX IF NOT EXISTS idx_chunks_text_trgm ON chunks USING gin (text gin_trgm_ops);

-- Analyze so planner biết dùng index
ANALYZE;