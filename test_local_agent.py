from llama_cpp import Llama
from autogen import ConversableAgent


class LlamaCppWrapper:
    def __init__(self, model_path: str, max_tokens: int = 256):
        self.llm = Llama(model_path=model_path, n_ctx=2048)
        self.max_tokens = max_tokens

    def create(self, messages, **kwargs):
        prompt = self._format_messages(messages)
        response = self.llm(
            prompt,
            max_tokens=kwargs.get("max_tokens", self.max_tokens),
            temperature=kwargs.get("temperature", 0.7),
            stop=["</s>", "###"],
        )
        text = response["choices"][0]["text"].strip()
        return {
            "choices": [
                {"message": {"role": "assistant", "content": text}}
            ]
        }

    def _format_messages(self, messages):
        return "\n".join(f"{m['role'].upper()}: {m['content']}" for m in messages)


def main():
    model_path = "/home/ubuntu/models/qwen2-7b-instruct-q5_k_m.gguf"
    llm_client = LlamaCppWrapper(model_path)

    # Agent powered by llama.cpp
    agent = ConversableAgent(
        name="Alien Overlord",
        system_message="You are a frustrated alien overlord who can't understand humans.",
        llm_config=None
    )

    def local_reply_func(messages, sender, config):
        print("🚀 Local LLM called with messages:", messages)
        result = llm_client.create(messages)
        return result["choices"][0]["message"]["content"]

    agent.register_reply("default", reply_func=local_reply_func)

    # Dummy sender (user proxy)
    user = ConversableAgent(
        name="Human Tester",
        system_message="A curious human.",
        llm_config=None
    )

    # Run one exchange
    history = [{"role": "user", "content": "Why do humans eat pizza?"}]
    reply = agent.generate_reply(messages=history, sender=user)

    print("\n🤖 Agent reply:\n", reply)


if __name__ == "__main__":
    main()
