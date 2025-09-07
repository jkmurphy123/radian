from autogen import ConversableAgent


def main():
    agent_a = ConversableAgent(
        name="Agent A",
        system_message="You are Agent A.",
        llm_config=None,
        human_input_mode="NEVER",
        code_execution_config=False,
    )

    agent_b = ConversableAgent(
        name="Agent B",
        system_message="You are Agent B.",
        llm_config=None,
        human_input_mode="NEVER",
        code_execution_config=False,
    )

    def dummy_reply(self, messages, sender, config):
        print("⚡ Dummy reply function triggered!")
        return False, {"role": "assistant", "content": "Hello from dummy"}

    agent_a.register_reply("Agent B", reply_func=dummy_reply)

    history = [{"role": "user", "content": "Hi Agent A, how are you?"}]
    reply = agent_a.generate_reply(messages=history, sender=agent_b)

    print("🤖 Agent A reply:", repr(reply))


if __name__ == "__main__":
    main()
