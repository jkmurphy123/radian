from llama_cpp import Llama
from autogen import ConversableAgent


class LlamaCppWrapper:
    """Wrapper around llama.cpp that mimics OpenAI's ChatCompletion.create"""

    def __init__(self, model_path: str, max_tokens: int = 256):
        self.llm = Llama(model_path=model_path, n_ctx=2048)
        self.max_tokens = max_tokens

    def create(self, messages, **kwargs):
        """Emulate OpenAI's ChatCompletion response structure"""
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
                {
                    "message": {
                        "role": "assistant",
                        "content": text
                    }
                }
            ]
        }

    def _format_messages(self, messages):
        return "\n".join(f"{m['role'].upper()}: {m['content']}" for m in messages)


def main():
    # Load your local model
    model_path = "/home/ubuntu/models/qwen2-7b-instruct-q5_k_m.gguf"
    llm_client = LlamaCppWrapper(model_path)

    # Create agent WITHOUT llm_config (so no OpenAI validation)
    agent = ConversableAgent(
        name="Alien Overlord",
        system_message="You are a frustrated alien overlord who can't understand humans.",
        llm_config=None
    )

    # Register custom reply function
    def local_reply_func(messages, sender, config):
        print("🚀 Local LLM called with messages:", messages)
        result = llm_client.create(messages)
        return result["choices"][0]["message"]["content"]

    agent.register_reply("default", reply_func=local_reply_func)

    # Run a simple conversation
    history = [{"role": "user", "content": "Why do humans eat pizza?"}]
    reply = agent.generate_reply(messages=history)

    print("\n🤖 Agent reply:\n", reply)


if __name__ == "__main__":
    main()
