SYSTEM_PROMPT = """
You are an ocean data assistant. Answer only using the retrieved context.
If uncertain, say so clearly.
"""

def build_prompt(question, contexts):
    return f"Question:\n{question}\n\nRetrieved Context:\n" + "\n\n".join(contexts)
