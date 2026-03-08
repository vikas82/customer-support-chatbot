# Customer Support Chatbot with RAG and Agent
# Customer Support Chatbot - RAG(Chroma) + Agno Agent/Team 

This Customer Support chatbot system is a real-world customer support chatbot built using
Retrieval-Augmented Generation (RAG) with Lang Chain, and a multi-agent architecture 
using Agno. It is designed to handle practical support flows such as FAQs, order tracking, 
refunds, shipping issues, and escalation. 
Core Architecture 
1. Data & Retrieval (RAG Layer) : 
• Knowledge sources include FAQs, policies, return and shipping rules 
• Documents are chunked, embedded, and stored in a vector database 
• On each user query, the retriever fetches the most relevant context to ground responses 
in facts 
Technology Stack: 
• Vector Database: Used Chroma DB 
• Embeddings: Used OpenAI (text-embedding-3-small) or Hugging 
Face(sentence-transformers/all-MiniLM-L6-v2) 
• Retrieval: Used Similarity search with optional reranking 
2. Multi-Agent Support Team (Agno): 
The chatbot behaves like a small support team, with specialized agents: 
• Support Triage Agent – Identifies user intent (refund, order status, damaged product, 
payment issue, etc.) 
• RAG Answer Agent – Uses retrieved knowledge to generate accurate, helpful responses 
• Order / Account Tool Agent (optional) – Calls backend Fast APIs for live data like 
order status or refund progress 
• Escalation Agent – Creates a support ticket when confidence is low or human help is 
required. Currently showing dummy message to the user but in real chatbot we can integrate Service now API 
for ticket creation. 
Technology Stack: 
• Multi-Agent (Agno) 
• Agno Agents & Teams 
• Tools: 
o Lang Chain retriever tool 
o Backend API tools (order lookup, refunds) 
• Ticket creation tool like Service Now 

Chatbot UI :– Used Python Streamlit UI 

Project Folder Structure : 
```
customer-support-chatbot/
├── README.md
├── app.py
├── requirements.txt
├── data/
│   ├── faqs.json
│   └── policies.json
└── agents/
    ├── __init__.py
    ├── triage_agent.py
    ├── rag_agent.py
    └── escalation_agent.py
```




