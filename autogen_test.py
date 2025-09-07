from autogen import AssistantAgent, UserProxyAgent

def main():
    # Create an assistant agent
    assistant = AssistantAgent("assistant")

    # Register a dummy reply handler for "message" events
    assistant.register_reply(
        "message",
        lambda sender, message, *args, **kwargs: {
            "role": "assistant",
            "content": "⚡ Dummy reply function triggered! This is a test response."
        }
    )

    # Create a user agent without Docker execution
    user = UserProxyAgent(
        "user",
        code_execution_config={"use_docker": False}
    )

    # Send a test message
    reply = user.send("Hello, can you hear me?", assistant)

    print("🤖 Agent reply:", reply)

if __name__ == "__main__":
    main()
