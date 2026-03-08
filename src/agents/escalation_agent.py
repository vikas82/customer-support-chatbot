from agno.agent import Agent

ESCALATION_INSTRUCTIONS = """
You are an escalation agent.
If the bot lacks enough info, create a concise "support ticket draft".

Return STRICT JSON:
{
  "should_escalate": true/false,
  "ticket": {
     "summary": "...",
     "details_needed": ["...","..."],
     "priority": "low|medium|high"
  }
}

Escalate if:
- user asks something that cannot be answered from context/tools
- or user is angry/complaining and needs human follow-up
Only output JSON.
"""

def build_escalation_agent(model):
    return Agent(
        name="Escalation Agent",
        role="Decide escalation and draft ticket",
        model=model,
        instructions=ESCALATION_INSTRUCTIONS
    )
