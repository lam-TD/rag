-- Enable pgvector
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS collections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid (),
    name VARCHAR(255) UNIQUE NOT NULL,
    embedding_model VARCHAR(255) NOT NULL,
    embedding_dimension INT NOT NULL,
    distance_metric VARCHAR(20) NOT NULL DEFAULT 'cosine',
    cmetadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- DOCUMENT embeddings table
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid (),
    collection_id UUID REFERENCES collections (id) ON DELETE CASCADE,
    cmetadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid (),
    collection_id UUID REFERENCES collections (id) ON DELETE CASCADE,
    document_id UUID REFERENCES documents (id) ON DELETE CASCADE,
    embedding vector NOT NULL,
    content TEXT NOT NULL,
    token_count INT,
    cmetadata JSONB
);

-- Indexes for performance optimization
CREATE INDEX IF NOT EXISTS idx_embedding_collection_id ON embeddings (collection_id);

-- GIN index cho chunk_metadata để tìm kiếm nhanh hơn
CREATE INDEX IF NOT EXISTS cmetadata_gin_idx ON embeddings USING GIN (cmetadata);

-- Sử dụng ivfflat index cho vector embedding để tăng tốc tìm kiếm gần đúng
CREATE INDEX IF NOT EXISTS idx_embedding_vector ON embeddings USING ivfflat (embedding vector_l2_ops)
WITH (lists = 100);

-- Analyze so planner biết dùng index
ANALYZE;