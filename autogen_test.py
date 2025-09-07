from autogen import AssistantAgent, UserProxyAgent

class FakeAssistant(AssistantAgent):
    def generate_reply(self, sender, message, **kwargs):
        return {
            "role": "assistant",
            "name": "assistant",
            "content": f"⚡ Fake LLM responding to: {message['content']}"
        }

def main():
    user = UserProxyAgent("user", code_execution_config={"use_docker": False})
    assistant = FakeAssistant("assistant")

    # User sends
    user.send("Hello, can you hear me?", assistant)

    # Force assistant to reply
    reply = assistant.generate_reply(sender=user, message={"role": "user", "content": "Hello, can you hear me?", "name": "user"})

    print("🤖 Assistant reply:", reply)

if __name__ == "__main__":
    main()
