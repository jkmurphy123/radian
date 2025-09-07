from autogen import AssistantAgent, UserProxyAgent
from llama_cpp import Llama


class LlamaAssistant(AssistantAgent):
    """AssistantAgent subclass backed by llama.cpp"""

    def __init__(self, name: str, model_path: str):
        super().__init__(name)
        self.llm = Llama(model_path=model_path, n_ctx=2048)

    def generate_reply(self, sender, message, **kwargs):
        """Override to call local llama.cpp instead of OpenAI"""
        print(f"🚀 Local LLM called with message from {sender.name}: {message['content']}")

        response = self.llm.create_chat_completion(
            messages=[
                {"role": "system", "content": "You are a frustrated alien overlord who can't understand humans."},
                {"role": message["role"], "content": message["content"]}
            ],
            max_tokens=256,
            temperature=0.7,
        )

        reply_text = response["choices"][0]["message"]["content"].strip()

        return {
            "role": "assistant",
            "name": self.name,
            "content": reply_text,
        }


def main():
    model_path = "/home/ubuntu/models/qwen2-7b-instruct-q5_k_m.gguf"

    user = UserProxyAgent("user", code_execution_config={"use_docker": False})
    assistant = LlamaAssistant("assistant", model_path=model_path)

    # User sends message
    user.send("Why do humans eat pizza?", assistant)

    # Assistant replies
    reply = assistant.generate_reply(
        sender=user,
        message={"role": "user", "content": "Why do humans eat pizza?", "name": "user"},
    )

    print("🤖 Assistant reply:", reply)


if __name__ == "__main__":
    main()
