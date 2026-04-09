from app.rag.prompt_templates import SYSTEM_PROMPT, build_prompt
from app.rag.provenance_formatter import format_context


class RAGAnswerer:
    def __init__(self, retriever, llm_client):
        self.retriever = retriever
        self.llm_client = llm_client

    def answer(self, question, top_k=5):
        results = self.retriever.retrieve(question, top_k=top_k)
        prompt = build_prompt(question, format_context(results))
        return {"answer": self.llm_client.generate(SYSTEM_PROMPT, prompt), "retrieved": results}
