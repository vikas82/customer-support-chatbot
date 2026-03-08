import requests
from typing import Dict, Any
from config import ORDER_API_URL, REFUND_API_URL
from rag.retriever_tool import retrieve_context

def tool_retrieve(query: str) -> Dict[str, Any]:
    return retrieve_context(query)

def tool_order_status(order_id: str) -> Dict[str, Any]:
    r = requests.post(ORDER_API_URL, json={"order_id": order_id}, timeout=10)
    r.raise_for_status()
    return r.json()

def tool_refund_status(refund_id: str) -> Dict[str, Any]:
    r = requests.post(REFUND_API_URL, json={"refund_id": refund_id}, timeout=10)
    r.raise_for_status()
    return r.json()
