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

    # Send a message
    user.send("Hello, can you hear me?", assistant)

    # Print assistant’s chat history
    print("🤖 Assistant messages:", assistant.chat_messages)

if __name__ == "__main__":
    main()
