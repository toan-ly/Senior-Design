from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
from backend.utils.setup_config import load_yaml
from qdrant_client import QdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore


INDEX_ID = "vector"


def build_qdrant_storage_context(storage_cfg, enable_hybrid: bool = False):
    host = storage_cfg.get("host", "localhost")
    port = storage_cfg.get("port", 6333)
    collection_name = storage_cfg.get("collection_name", "mental_health_docs")

    client = QdrantClient(host=host, port=port)
    vector_store = QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        enable_hybrid=enable_hybrid,
    )
    return StorageContext.from_defaults(vector_store=vector_store)


def build_vector_index(nodes, paths_config="configs/paths.yaml"):
    cfg = load_yaml(paths_config)
    storage_cfg = cfg["storage"]
    backend = storage_cfg.get("backend", "local")

    # Qdrant
    if backend == "qdrant":
        print("Using Qdrant as vector store backend")
        storage_context = build_qdrant_storage_context(storage_cfg)

        vector_index = VectorStoreIndex(nodes, storage_context=storage_context)
        vector_index.set_index_id(INDEX_ID)
        print("✅ Qdrant-backed index built and stored in Qdrant")
        return vector_index

    index_store_path = cfg["storage"]["index_store"]
    # Local (original behavior)
    try:
        storage_context = StorageContext.from_defaults(persist_dir=index_store_path)
        vector_index = load_index_from_storage(storage_context, index_id=INDEX_ID)
        print(f"✅ Loaded existing index '{INDEX_ID}' from: {index_store_path}")
    except Exception:
        print(
            f"⚠️ No existing index found at: {index_store_path}. Building new index..."
        )
        storage_context = StorageContext.from_defaults()
        vector_index = VectorStoreIndex(nodes, storage_context=storage_context)
        vector_index.set_index_id(INDEX_ID)
        storage_context.persist(persist_dir=index_store_path)
        print(f"✅ New index '{INDEX_ID}' built and saved to: {index_store_path}")
    return vector_index
