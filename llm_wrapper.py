from llama_cpp import Llama


class LlamaCppWrapper:
    """
    Wrapper around llama_cpp that mimics OpenAI's response format
    so it can plug directly into AutoGen without API key errors.
    """

    def __init__(self, model_path: str, max_tokens: int = 512):
        self.llm = Llama(model_path=model_path, n_ctx=4096)
        self.max_tokens = max_tokens

    def create(self, messages, **kwargs):
        """
        Emulate the OpenAI `ChatCompletion.create` interface.
        - messages: list of dicts like [{"role": "system", "content": "..."}, ...]
        - kwargs: extra options like temperature
        """
        print("🚀 llama_cpp client invoked with:", messages)
        
        # Build prompt from messages
        prompt = self._format_messages(messages)

        # Run inference
        response = self.llm(
            prompt,
            max_tokens=kwargs.get("max_tokens", self.max_tokens),
            temperature=kwargs.get("temperature", 0.7),
            stop=["</s>", "###"],
        )

        text = response["choices"][0]["text"].strip()

        # Return OpenAI-style response
        return {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": text
                    }
                }
            ]
        }

    def _format_messages(self, messages):
        """
        Convert messages into a simple prompt string.
        Example: system + alternating user/assistant messages.
        """
        formatted = []
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            formatted.append(f"{role.upper()}: {content}")
        return "\n".join(formatted)
