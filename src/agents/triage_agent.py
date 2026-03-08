from agno.agent import Agent

TRIAGE_INSTRUCTIONS = """
You are a support triage agent.
Classify the user's intent and extract any IDs.

Return STRICT JSON with keys:
{
  "intent": one of ["order_tracking","refund_status","return_policy","shipping_policy","general_faq","complaint","other"],
  "order_id": string or "",
  "refund_id": string or "",
  "needs_retrieval": true/false,
  "needs_order_api": true/false,
  "needs_refund_api": true/false
}

Rules:
- If user asks "where is my order", "track", "delivery", "late", set intent=order_tracking and needs_order_api=true (if order_id present).
- If user asks "refund status", set intent=refund_status and needs_refund_api=true (if refund_id present).
- If user asks policy questions, needs_retrieval=true.
- If missing required ID, keep the intent but leave ID empty and set needs_order_api/needs_refund_api=false.
Only output valid JSON. No commentary.
"""

def build_triage_agent(model):
    return Agent(
        name="Triage Agent",
        role="Classify intent and extract identifiers",
        model=model,
        instructions=TRIAGE_INSTRUCTIONS,
    )
