from autogen import AssistantAgent, UserProxyAgent

# Minimal fake backend
class FakeLLM:
    def create(self, messages, **kwargs):
        # Always reply with a fixed string
        return {"choices": [{"message": {"role": "assistant", "content": "⚡ Fake LLM says hello!"}}]}

def main():
    user = UserProxyAgent("user", code_execution_config={"use_docker": False})

    # Assistant with fake LLM backend
    assistant = AssistantAgent(
        "assistant",
        llm_config={
            "config_list": [
                {
                    "model": "fake-llm",
                    "api_key": "none",
                    "client": FakeLLM(),   # 👈 plug in fake client
                }
            ]
        },
    )

    # Send a message
    user.send("Hello, can you hear me?", assistant)
    reply = assistant.generate_reply(sender=user, message={"role": "user", "content": "Hello, can you hear me?", "name": "user"})

    print("🤖 Assistant reply:", reply)

if __name__ == "__main__":
    main()
