from autogen import AssistantAgent, UserProxyAgent

def main():
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

    # User sends a message (this won’t return anything)
    user.send("Hello, can you hear me?", assistant)

    # Fetch last message in assistant’s history
    if assistant._oai_messages:  # internal conversation log
        last_msg = assistant._oai_messages[-1]
        print("🤖 Agent reply:", last_msg)
    else:
        print("No reply recorded.")

if __name__ == "__main__":
    main()
