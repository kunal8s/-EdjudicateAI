import google.generativeai as genai
import yaml
import json
import os
from edjudicate_ai_app.app.core.retriever import retrieve_chunks

api_key = None
try:
    with open("config/config.yaml") as f:
        cfg = yaml.safe_load(f)
        api_key = cfg.get("gemini_api_key")
except Exception:
    api_key = None

if not api_key:
    api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("Gemini API key not configured. Set config/config.yaml or GEMINI_API_KEY env var.")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.0-flash")

COT = """
You are a claims evaluation assistant. You are provided with:
- A customer query
- Retrieved policy document clauses

Your job is to:
1. Identify the important fields from the query (e.g., age, procedure, location, policy duration).
2. Think step-by-step to determine if the policy covers this case.
3. Reference specific clauses to justify your reasoning.
4. Give a structured JSON response with:
    - decision ("approved" or "rejected")
    - amount (if any)
    - justification

---

Query:
{query}

Retrieved Clauses:
{clauses}

---

⚠️ DO NOT return markdown, explanations, or extra text.
✅ Just return valid JSON. No triple backticks.
"""

def evaluate_decision(query, session_id):
    retrieved_chunks = retrieve_chunks(query,session_id)
    clauses = "\n\n".join(retrieved_chunks)
    prompt = COT.format(query=query, clauses=clauses)
    response = model.generate_content(prompt)
    #raw_output = 
    return response.candidates[0].content.parts[0].text

    # try:
    #     parsed_output = json.loads(raw_output)
    #     return {
    #         "query": query,
    #         "response": parsed_output,
    #         "retrieved_clauses": retrieved_chunks
    #     }
    # except json.JSONDecodeError:
    #     return {
    #         "query": query,
    #         "response": {"error": "Invalid JSON response from Gemini", "raw": raw_output},
    #         "retrieved_clauses": retrieved_chunks
    #     }
    
    
    
#


QA_PROMPT = """
You are a helpful policy QA assistant. Using ONLY the provided policy excerpts, answer the user's question concisely in 1-3 sentences.

- If the answer cannot be found in the excerpts, respond exactly with: Information not found in the provided document.
- Do not include any disclaimers, markdown, or extra formatting.

Question:
{question}

Policy Excerpts:
{clauses}
"""

def answer_question(question: str, session_id: str, k: int = 5) -> str:
    """Answer a question using retrieved chunks from the FAISS index for the given session.

    Returns plain text suitable for the HackRx expected `answers` array.
    """
    retrieved_chunks = retrieve_chunks(question, session_id, k=k)
    clauses = "\n\n".join(retrieved_chunks)
    prompt = QA_PROMPT.format(question=question, clauses=clauses)
    response = model.generate_content(prompt)
    return response.candidates[0].content.parts[0].text