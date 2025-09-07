from autogen import AssistantAgent, UserProxyAgent

def main():
    # Create a user agent (disable Docker)
    user = UserProxyAgent("user", code_execution_config={"use_docker": False})

    # Create an assistant agent
    assistant = AssistantAgent("assistant")

    # Proper reply handler must return (triggered, message_dict)
    assistant.register_reply(
        "message",
        lambda sender, message, *args, **kwargs: (
            True,  # means this handler is triggered
            {
                "role": "assistant",
                "content": f"⚡ Dummy reply received your message: {message['content']}"
            }
        )
    )

    # User sends a message to assistant
    reply = user.send("Hello, can you hear me?", assistant)

    print("🤖 Agent reply:", reply)

if __name__ == "__main__":
    main()
