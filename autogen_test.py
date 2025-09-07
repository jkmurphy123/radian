from autogen import AssistantAgent, UserProxyAgent

def main():
    # Create user
    user = UserProxyAgent("user", code_execution_config={"use_docker": False})

    # Create assistant with a dummy "echo" model
    assistant = AssistantAgent(
        "assistant",
        llm_config={
            "config_list": [
                {
                    "model": "echo",   # special built-in backend that just echoes
                    "api_key": "none"  # not used
                }
            ]
        }
    )

    # User sends
    user.send("Hello, can you hear me?", assistant)

    # Now force assistant to generate using its config
    reply = assistant.generate_reply(sender=user, message={"role": "user", "content": "Hello, can you hear me?", "name": "user"})

    print("🤖 Assistant reply:", reply)

if __name__ == "__main__":
    main()
