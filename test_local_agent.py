from llama_cpp import Llama
from autogen import ConversableAgent


class LlamaCppWrapper:
    """Wrapper around llama_cpp that mimics OpenAI's ChatCompletion API."""

    def __init__(self, model_path: str, max_tokens: int = 256):
        self.llm = Llama(model_path=model_path, n_ctx=2048)
        self.max_tokens = max_tokens

    def create(self, messages, **kwargs):
        """Directly call llama_cpp's chat completion API."""
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


def main():
    model_path = "/home/ubuntu/models/qwen2-7b-instruct-q5_k_m.gguf"
    llm_client = LlamaCppWrapper(model_path)

    # Create agent backed by local llama.cpp
    agent = ConversableAgent(
        name="Alien Overlord",
        system_message="You are a frustrated alien overlord who can't understand humans.",
        llm_config=None
    )

    # Register custom reply func that uses our wrapper
    def local_reply_func(messages, sender, config):
        print("🚀 Local LLM called with messages:", messages)
        result = llm_client.create(messages)
        return result["choices"][0]["message"]["content"]

    agent.register_reply("default", reply_func=local_reply_func)

    # Dummy sender (acts like a user)
    user = ConversableAgent(
        name="Human Tester",
        system_message="A curious human.",
        llm_config=None
    )

    # Run a test exchange
    history = [
        {"role": "system", "content": "You are a frustrated alien overlord."},
        {"role": "user", "content": "Why do humans eat pizza?"}
    ]

    reply = agent.generate_reply(messages=history, sender=user)

    print("\n🤖 Agent reply:\n", reply)


if __name__ == "__main__":
    main()
