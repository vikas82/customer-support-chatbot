import json
from typing import Dict, Any, List

from agno.team import Team
from config import MIN_SCORE
from agents.tools import tool_retrieve, tool_order_status, tool_refund_status
from agents.triage_agent import build_triage_agent
from agents.rag_agent import build_rag_agent
from agents.escalation_agent import build_escalation_agent

def _safe_json(text: str) -> Dict[str, Any]:
    try:
        return json.loads(text)
    except Exception:
        return {}

def _context_quality(matches: List[dict]) -> bool:
    """
    Chroma returns a "score" that's distance-like (lower often better).
    We'll treat score <= MIN_SCORE as "good enough".
    """
    if not matches:
        return False
    best = matches[0].get("score", 999.0)
    return float(best) <= float(MIN_SCORE)

def build_team(model):
    triage = build_triage_agent(model)
    escalation = build_escalation_agent(model)

    # RAG agent gets tool functions
    rag_tools = [tool_retrieve, tool_order_status, tool_refund_status]
    rag = build_rag_agent(model, tools=rag_tools)

    return Team(
        name="Support Team",
        members=[triage, rag, escalation],
        model=model,
        show_members_responses=True,

    )

def run_support(team: Team, user_message: str, history: List[Dict[str, str]]) -> str:
    """
    Orchestrates multi-agent flow:
    1) triage -> intent
    2) retrieval/tools
    3) rag answer
    4) escalation check if needed
    """
    print("Running support flow...")
    print("===================================")
    print("team.members:", [m.name for m in team.members])
    

    triage_agent = team.members[0]
    rag_agent = team.members[1]
    escalation_agent = team.members[2]

    # print("User message:", user_message)
    # print("Running triage agent...")
    # print("-----")
    # print("triage_agent:", triage_agent)
    # print("rag_agent:", rag_agent)
    # print("escalation_agent:", escalation_agent)


    

    triage_resp = triage_agent.run(user_message)
    triage_json = _safe_json(triage_resp.content)
    print("Triage JSON:", triage_json)

    intent = triage_json.get("intent", "other")
    order_id = triage_json.get("order_id", "")
    refund_id = triage_json.get("refund_id", "")
    needs_retrieval = bool(triage_json.get("needs_retrieval", True))
    needs_order_api = bool(triage_json.get("needs_order_api", False))
    needs_refund_api = bool(triage_json.get("needs_refund_api", False))

    tool_outputs = {}

    # Tool calls
    if needs_order_api and order_id:
        try:
            tool_outputs["order_status"] = tool_order_status(order_id)
        except Exception as e:
            tool_outputs["order_status_error"] = str(e)

    if needs_refund_api and refund_id:
        try:
            tool_outputs["refund_status"] = tool_refund_status(refund_id)
        except Exception as e:
            tool_outputs["refund_status_error"] = str(e)

    retrieved = {"matches": []}
    if needs_retrieval:
        retrieved = tool_retrieve(user_message)

    good_context = _context_quality(retrieved.get("matches", []))

    # If user needs ID but didn't provide, ask for it nicely
    if intent == "order_tracking" and not order_id:
        return "I can help track it — could you share your **Order ID** (like A1001)? Once I have it, I’ll pull the latest status."
    if intent == "refund_status" and not refund_id:
        return "I can check that for you — please share your **Refund ID** (like R2001), and I’ll look it up."

    # RAG response prompt
    history_text = "\n".join([f"{m['role']}: {m['content']}" for m in history][-12:])
    context_text = "\n\n".join(
        [f"[source: {m['source']}, score: {m['score']}] {m['content']}" for m in retrieved.get("matches", [])]
    )

    rag_prompt = f"""
    CONVERSATION HISTORY:
    {history_text}

    TRIAGE JSON:
    {json.dumps(triage_json, ensure_ascii=False)}

    TOOL OUTPUTS (if any):
    {json.dumps(tool_outputs, ensure_ascii=False)}

    CONTEXT (if any):
    {context_text}

    USER MESSAGE:
    {user_message}
    """

    answer = rag_agent.run(rag_prompt).content.strip()

    # Escalation check if no good context + no useful tools
    if (needs_retrieval and not good_context) and ("order_status" not in tool_outputs) and ("refund_status" not in tool_outputs):
        esc_prompt = f"""
        USER MESSAGE:
        {user_message}

        WHAT WE HAVE:
        - triage: {json.dumps(triage_json)}
        - retrieved_matches_count: {len(retrieved.get("matches", []))}
        - context_good: {good_context}
        - tool_outputs: {json.dumps(tool_outputs)}
        """
        print("Running escalation agent...")
        print("-----")
        print("esc_prompt:", esc_prompt)

        esc = escalation_agent.run(esc_prompt).content
        esc_json = _safe_json(esc)
        print("Escalation JSON:", esc_json)

        if esc_json.get("should_escalate", True):
            ticket = esc_json.get("ticket", {})
            details_needed = ticket.get("details_needed", [])
            bullets = "\n".join([f"- {d}" for d in details_needed]) or "- Order ID / Refund ID\n- Registered email/phone\n- Short description"
            return (
                f"I want to handle this carefully — I don’t have enough confirmed info yet.\n\n"
                f"Here’s what I’ll need to resolve it fast:\n{bullets}\n\n"
                f"If you share these, I’ll either solve it right here or draft a clean ticket for human support."
            )

    return answer
