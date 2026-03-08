import os
import sys
from tqdm import tqdm
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from rag.vectorstore import get_vectorstore
from pathlib import Path
data = Path(__file__).parent.parent / "data"
print("Data path:", data)

def ingest(data_dir: str = data) -> None:
    if not os.path.isdir(data_dir):
        raise FileNotFoundError(f"Data folder not found: {data_dir}")

    # Load .md/.txt easily
    loader = DirectoryLoader(
        data_dir,
        glob="**/*.*",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True,
        use_multithreading=True,
    )
    docs = loader.load()
    print("Loaded documents:", len(docs))
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=30,
    )
    chunks = splitter.split_documents(docs)

    vs = get_vectorstore()
    print(f"Ingesting {len(chunks)} chunks into Chroma...")
    for i in tqdm(range(0, len(chunks), 64)):
        batch = chunks[i:i+64]
        vs.add_documents(batch)

    # vs.persist()
    print("✅ Ingestion complete. Vector DB persisted.")

if __name__ == "__main__":
    ingest()
    # get_vectorstore()
