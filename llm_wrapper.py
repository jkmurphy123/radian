from llama_cpp import Llama

class LlamaCppWrapper:
    """
    Thin wrapper around llama_cpp so it can act like an AutoGen LLM client.
    """

    def __init__(self, model_path: str, max_tokens: int = 512):
        self.llm = Llama(model_path=model_path, n_ctx=4096)
        self.max_tokens = max_tokens

    def complete(self, prompt: str) -> str:
        """Generate a completion for a given prompt."""
        response = self.llm(
            prompt,
            max_tokens=self.max_tokens,
            stop=["</s>", "###"],
        )
        return response["choices"][0]["text"].strip()
