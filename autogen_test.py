from autogen import AssistantAgent, UserProxyAgent

def main():
    # Create an assistant agent (pretend LLM)
    assistant = AssistantAgent("assistant")

    # Override the reply function so we don't need an API key or model
    assistant.register_reply(
        lambda *args, **kwargs: ("⚡ Dummy reply function triggered!", "This is a test response.")
    )

    # Create a simple user agent
    user = UserProxyAgent("user")

    # Send a test message
    reply = user.send("Hello, can you hear me?", assistant)

    print("🤖 Agent reply:", reply)

if __name__ == "__main__":
    main()
