from llama_cpp import Llama
from autogen import ConversableAgent


class LlamaCppWrapper:
    def __init__(self, model_path: str, max_tokens: int = 256):
        self.llm = Llama(model_path=model_path, n_ctx=2048)
        self.max_tokens = max_tokens

    def create(self, messages, **kwargs):
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

    # Agent powered by llama.cpp
    agent = ConversableAgent(
        name="Alien Overlord",
        system_message="You are a frustrated alien overlord who can't understand humans.",
        llm_config=None,
        human_input_mode="NEVER",   # disables asking user
        code_execution_config=False # disables code execution
    )
    agent.auto_reply = False  # <--- force-disable auto reply


    # Dummy user agent
    user = ConversableAgent(
        name="Human Tester",
        system_message="A curious human.",
        llm_config=None
    )

    # Register reply specifically for when sender is "Human Tester"
    # def local_reply_func(self, messages, sender, config):
    #     print("🚀 Local LLM called with messages:", messages)
    #     result = llm_client.create(messages)
    #     reply_text = result["choices"][0]["message"]["content"]

    #     # Must be a list of role/content dicts
    #     #reply_message = [{"role": "assistant", "content": reply_text}]
    #     #print("🚀 Local LLM responded with messages:", reply_message)
    #     reply_text = result["choices"][0]["message"]["content"]
    #     print("⚡ Returning reply:", reply_text)        

    #     #return False, reply_message
    #     return False, reply_text

    def local_reply_func(self, messages, sender, config):
        print("⚡ Custom reply function triggered!")
        return False, "This is a test reply from local_reply_func."



    agent.register_reply("Human Tester", reply_func=local_reply_func)
    #agent.register_reply("default", reply_func=local_reply_func)
    print("🔍 Registered reply functions:", agent._reply_func_list)

    # Run a test exchange
    history = [
        {"role": "system", "content": "You are a frustrated alien overlord."},
        {"role": "user", "content": "Why do humans eat pizza?"}
    ]

    final, reply = agent.generate_reply(messages=history, sender=user)
    print("\n🤖 Agent reply:\n", reply)



if __name__ == "__main__":
    main()
