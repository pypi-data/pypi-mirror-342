from langchain_core.language_models.llms import LLM
from typing import Optional, List
from .client import EuriaiClient

class EuriaiLangChainLLM(LLM):
    """
    LangChain-compatible wrapper for euriai.EuriaiClient
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4.1-nano",
        temperature: float = 0.7,
        max_tokens: int = 300
    ):
        self.client = EuriaiClient(api_key=api_key, model=model)
        self.temperature = temperature
        self.max_tokens = max_tokens

    @property
    def _llm_type(self) -> str:
        return "euriai"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        response = self.client.generate_completion(
            prompt=prompt,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            stop=stop
        )
        return response.get("choices", [{}])[0].get("message", {}).get("content", "")
