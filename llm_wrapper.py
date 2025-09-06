from llama_cpp import Llama


class LlamaCppWrapper:
    """Wrapper around llama_cpp that mimics OpenAI's ChatCompletion"""

    def __init__(self, model_path: str, max_tokens: int = 256):
        self.llm = Llama(model_path=model_path, n_ctx=2048)
        self.max_tokens = max_tokens

    def create(self, messages, **kwargs):
        """Use llama_cpp's chat completion API"""
        response = self.llm.create_chat_completion(
            messages=messages,
            max_tokens=kwargs.get("max_tokens", self.max_tokens),
            temperature=kwargs.get("temperature", 0.7),
        )

        text = response["choices"][0]["message"]["content"].strip()
        return {
            "choices": [
                {"message": {"role": "assistant", "content": text}}
            ]
        }
