from langchain_community.vectorstores import Chroma
from rag_app.get_embedding_function import get_embeddings

CHROMA_PATH = "data/chroma"
CHROMA_DB_INSTANCE = None  # Reference to singleton instance of ChromaDB

def get_chroma_db():
    global CHROMA_DB_INSTANCE
    if not CHROMA_DB_INSTANCE:
        # prepare the DB
        CHROMA_DB_INSTANCE = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=get_embeddings()
        )
        print(f"✅ Init ChromaDB {CHROMA_DB_INSTANCE} from {CHROMA_PATH}")
    
    return CHROMA_DB_INSTANCE