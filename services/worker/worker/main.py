import os
from .ingest import ingest_txt

def main():
    # MVP: chạy thử bằng env vars (sau này chuyển sang queue)
    doc_id = os.getenv("DOC_ID", "00000000-0000-0000-0000-000000000001")
    ver_id = os.getenv("VER_ID", "00000000-0000-0000-0000-000000000101")
    s3_key = os.getenv("S3_KEY", "samples/hello.txt")
    print(f"Ingest TXT: doc={doc_id} ver={ver_id} key={s3_key}")
    ingest_txt(document_id=doc_id, version_id=ver_id, s3_key=s3_key)

if __name__ == "__main__":
    main()
