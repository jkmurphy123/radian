from autogen import AssistantAgent, UserProxyAgent

def main():
    user = UserProxyAgent("user", code_execution_config={"use_docker": False})
    assistant = AssistantAgent("assistant")

    # Register dummy reply
    def dummy_reply(sender, message, *args, **kwargs):
        return True, {
            "role": "assistant",
            "name": "assistant",  # <-- required in 0.5.x
            "content": f"⚡ Dummy reply received: {message['content']}"
        }

    assistant.register_reply("message", dummy_reply)

    # User sends
    user.send("Hello, can you hear me?", assistant)

    # Assistant generates
    reply = assistant.generate_reply(sender=user, message={"role": "user", "content": "Hello, can you hear me?", "name": "user"})

    print("🤖 Assistant reply:", reply)

if __name__ == "__main__":
    main()
