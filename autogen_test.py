from autogen import AssistantAgent, UserProxyAgent

def main():
    # Create agents
    user = UserProxyAgent("user", code_execution_config={"use_docker": False})
    assistant = AssistantAgent("assistant")

    # Register dummy reply
    assistant.register_reply(
        "message",
        lambda sender, message, *args, **kwargs: (
            True,
            {"role": "assistant", "content": f"⚡ Dummy reply received: {message['content']}"}
        )
    )

    # User sends a message
    user.send("Hello, can you hear me?", assistant)

    # Force assistant to generate reply
    reply = assistant.generate_reply(sender=user, message={"role": "user", "content": "Hello, can you hear me?"})

    print("🤖 Assistant reply:", reply)

if __name__ == "__main__":
    main()
