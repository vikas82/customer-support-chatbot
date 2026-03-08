from typing import Any, Dict
from rag.vectorstore import get_vectorstore
from config import TOP_K

def retrieve_context(query: str) -> Dict[str, Any]:
    """
    Returns:
      {
        "matches": [
          {"content": "...", "source": "...", "score": 0.12},
          ...
        ]
      }
    Lower score usually means closer match in Chroma (distance-like).
    We'll normalize later in agent logic.
    """
    vs = get_vectorstore()
    print("Vectorstore:", vs)
    results = vs.similarity_search_with_score(query, k=TOP_K)

    matches = []
    for doc, score in results:
        src = doc.metadata.get("source", "unknown")
        matches.append(
            {
                "content": doc.page_content,
                "source": src,
                "score": float(score),
            }
        )
        print(f"Retrieved doc from {src} with score {score}: {doc.page_content[:100]}...")
    return {"matches": matches}
