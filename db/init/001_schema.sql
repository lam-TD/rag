-- Enable pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- Analyze so planner biết dùng index
ANALYZE;