INSERT INTO
    collections (
        name,
        embedding_model,
        embedding_dimension,
        distance_metric,
        metadata
    )
VALUES (
        'default',
        'jina-embeddings-v3',
        1024,
        'cosine',
        '{"description": "Default collection using Jina embeddings v3 model"}'
    )
ON CONFLICT (name) DO NOTHING;