from autogen import AssistantAgent, UserProxyAgent

def main():
    # Create an assistant agent
    assistant = AssistantAgent("assistant")

    # Register a dummy reply handler for normal "message" events
    assistant.register_reply(
        "message",   # <-- required first argument
        lambda sender, message, *args, **kwargs: ("⚡ Dummy reply function triggered!", "This is a test response.")
    )

    # Create a simple user agent
    user = UserProxyAgent("user")

    # Send a test message
    reply = user.send("Hello, can you hear me?", assistant)

    print("🤖 Agent reply:", reply)

if __name__ == "__main__":
    main()
