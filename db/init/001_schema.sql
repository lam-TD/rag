-- Enable pgvector
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS embeddings(
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  document_id VARCHAR NOT NULL,
  embedding vector(1024),
  content TEXT,
  token_count INT,
  metadata JSON,
  chunk_metadata JSON
);

-- Analyze so planner biết dùng index
ANALYZE;