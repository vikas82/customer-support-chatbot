from config import EMBEDDINGS_PROVIDER, HF_EMBEDDINGS_MODEL, OPENAI_API_KEY, OPENAI_EMBEDDINGS_MODEL

def get_embeddings():
    if EMBEDDINGS_PROVIDER == "openai":
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY missing but EMBEDDINGS_PROVIDER=openai")
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(model=OPENAI_EMBEDDINGS_MODEL, api_key=OPENAI_API_KEY)

    # default: local HF embeddings
    from langchain_huggingface import HuggingFaceEmbeddings
    return HuggingFaceEmbeddings(model_name=HF_EMBEDDINGS_MODEL)

    # from chromadb.utils import embedding_functions
    # return embedding_functions.SentenceTransformerEmbeddingFunction(
    #         model_name='sentence-transformers/all-MiniLM-L6-v2'
    #     )
