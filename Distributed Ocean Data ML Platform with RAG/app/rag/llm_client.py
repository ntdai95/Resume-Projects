import os
import requests


class LLMClient:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "ollama")
        self.model = os.getenv("LLM_MODEL", "llama3")
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        if self.provider != "ollama":
            raise ValueError(
                f"Only Ollama is supported in this configuration. Got LLM_PROVIDER={self.provider}"
            )

    def generate(self, system_prompt, user_prompt):
        resp = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": system_prompt + "\n\n" + user_prompt,
                "stream": False,
            },
            timeout=600,
        )
        
        resp.raise_for_status()
        return resp.json().get("response", "")