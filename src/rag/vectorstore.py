import os
import sys
from typing import Optional
#from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
sys.path.append(os.path.abspath('config'))
from config import CHROMA_DIR, COLLECTION_NAME
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from rag.embeddings import get_embeddings
print("CHROMA_DIR:", CHROMA_DIR)
print("COLLECTION_NAME:", COLLECTION_NAME)

def get_vectorstore(persist_directory: Optional[str] = None) -> Chroma:
    persist_directory = persist_directory or CHROMA_DIR
    embeddings = get_embeddings()
    #print("Embeddings:", embeddings)
    print("Persist Directory:", persist_directory)
    
    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(persist_directory)
    )
    print("Vector Store:", vector_store)
    return vector_store



if __name__ == "__main__":
    get_vectorstore()
