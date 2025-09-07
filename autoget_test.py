from autogen import ConversableAgent


def main():
    # Agent A
    agent_a = ConversableAgent(
        name="Agent A",
        system_message="You are Agent A.",
        llm_config=None,
        human_input_mode="NEVER",
        code_execution_config=False,
    )

    # Agent B
    agent_b = ConversableAgent(
        name="Agent B",
        system_message="You are Agent B.",
        llm_config=None,
        human_input_mode="NEVER",
        code_execution_config=False,
    )

    # Register dummy reply function for when B sends messages
    def dummy_reply(self, messages, sender, config):
        print("⚡ Dummy reply function triggered!")
        return False, "Hello from dummy"

    agent_a.register_reply("Agent B", reply_func=dummy_reply)

    # History to kick off
    history = [{"role": "user", "content": "Hi Agent A, how are you?"}]

    # Ask Agent A to reply to Agent B
    reply = agent_a.generate_reply(messages=history, sender=agent_b)

    print("🤖 Agent A reply:", repr(reply))


if __name__ == "__main__":
    main()
