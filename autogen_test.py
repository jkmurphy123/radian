from autogen import AssistantAgent, UserProxyAgent, Conversation

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

    # Create a conversation manager
    convo = Conversation([user, assistant])

    # Run one turn: user → assistant
    convo.post(user, "Hello, can you hear me?")

    # Print conversation log
    for turn in convo.messages:
        print(f"{turn['role']}: {turn['content']}")

if __name__ == "__main__":
    main()
