from autogen import AssistantAgent, UserProxyAgent

def main():
    # Create a user agent (no Docker)
    user = UserProxyAgent("user", code_execution_config={"use_docker": False})

    # Create an assistant agent
    assistant = AssistantAgent("assistant")

    # Register dummy reply for assistant
    assistant.register_reply(
        "message",
        lambda sender, message, *args, **kwargs: {
            "role": "assistant",
            "content": f"⚡ Dummy reply received your message: {message['content']}"
        }
    )

    # User sends a message to assistant
    reply = user.send("Hello, can you hear me?", assistant)

    print("🤖 Agent reply:", reply)

if __name__ == "__main__":
    main()
