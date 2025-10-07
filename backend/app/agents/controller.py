#  for fater use rule based agent, falls back to Groq LLM
import os, json
# Remove all OpenAI imports and usage; only use ChatGroq for LLM calls and embeddings
from langchain_groq.chat_models import ChatGroq

# from langchain_community.chat_models import ChatGroq, ChatOpenAI
# from langchain.chat_models import ChatGroq, ChatOpenAI  # ChatGroq if available in your stack
from app.utils.logging_utils import append_raw_log
from langchain_groq import ChatGroq


import os
print("🔑 GROQ_API_KEY (from env at controller):", os.getenv("GROQ_API_KEY"))

GROQ_KEY = os.getenv("GROQ_API_KEY")

class Controller:
    def __init__(self):
        # Only use ChatGroq from Groq Cloud; no OpenAI fallback
        if not GROQ_KEY:
            raise ValueError("GROQ_API_KEY environment variable not set.")
        self.llm = ChatGroq(
            api_key=GROQ_KEY,
            model="llama-3.1-70b-versatile",
            temperature=0
            )

    def decide(self, text, pdf_doc_id=None, prefer_agent=None):
        t = text.lower().strip()
        if prefer_agent:
            reason = f"User requested agent {prefer_agent}"
            decision = prefer_agent.upper()
            return decision, reason

        # Fast rules
        if pdf_doc_id or "pdf" in t or "analyze this document" in t:
            return "PDF_RAG", "Rule: contains PDF reference or pdf_doc_id supplied"
        if any(word in t for word in ["recent paper", "arxiv", "paper on", "latest research"]):
            return "ARXIV", "Rule: user asked specifically about papers or arXiv"
        if any(word in t for word in ["who", "what", "when", "where", "news", "search", "recent"]):
            return "WEB_SEARCH", "Rule: general web query indicators"

        # Fallback to Groq Cloud LLM for nuanced decision
        prompt = f"""
        You are an agent router. Options: PDF_RAG, WEB_SEARCH, ARXIV.
        Decide which agent fits best for the user input. Return strict JSON: {{ "decision":"AGENT", "reason":"short reason" }}.
        Input: \"\"\"{text}\"\"\"
        """

        # Use ChatGroq's invoke method
        resp = self.llm.invoke(prompt)

        # Extract string content (very important)
        if hasattr(resp, "content"):
            resp_text = resp.content
        else:
            resp_text = str(resp)

        try:
            parsed = json.loads(resp_text)
            decision = parsed.get("decision", "WEB_SEARCH")
            reason = parsed.get("reason", "LLM fallback")
        except Exception:
            decision, reason = "WEB_SEARCH", "LLM responded non-JSON; fallback to WEB_SEARCH"

        # Save reasoning
        append_raw_log({
            "input": text,
            "decision": decision,
            "reason": reason,
            "llm_raw": resp_text
        })

        return decision, reason


# import os
# print("Groq key loaded:", os.getenv("GROQ_API_KEY"))
