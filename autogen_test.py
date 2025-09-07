from autogen import AssistantAgent

def main():
    assistant = AssistantAgent("assistant")

    # Override reply generation for testing
    assistant.register_reply(
        "message",
        lambda sender, message, *args, **kwargs: {
            "role": "assistant",
            "content": f"⚡ Dummy reply received your message: {message['content']}"
        }
    )

    # Directly generate a reply
    test_message = {"role": "user", "content": "Hello, can you hear me?"}
    reply = assistant.generate_reply(sender="user", message=test_message)

    print("🤖 Agent reply:", reply)

if __name__ == "__main__":
    main()
