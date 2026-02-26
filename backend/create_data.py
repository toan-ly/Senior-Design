from backend.rag.index import build_vector_index
from backend.rag.ingest import ingest_docs


def main():
    nodes = ingest_docs()
    build_vector_index(nodes)


if __name__ == "__main__":
    main()
    print("✅ Data ingestion and index building complete!")
