from langchain_community.embeddings import OllamaEmbeddings

def get_embeddings():
    embeddings = OllamaEmbeddings(model="llama3.2")
    return embeddings