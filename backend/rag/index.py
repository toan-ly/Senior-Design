from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
from backend.utils.setup_config import load_paths_config

INDEX_ID = "vector"


def build_vector_index(nodes, paths_config="configs/paths.yaml"):
    cfg = load_paths_config(paths_config)
    index_store_path = cfg["storage"]["index_store"]
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
