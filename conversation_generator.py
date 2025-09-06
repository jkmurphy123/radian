import os
import json
import random
from datetime import datetime
from config_loader import load_config
from llm_wrapper import LlamaCppWrapper
from autogen import ConversableAgent

LOGS_DIR = "logs"


def ensure_logs_dir():
    os.makedirs(LOGS_DIR, exist_ok=True)


def create_agent(persona: dict, llm_client: LlamaCppWrapper) -> ConversableAgent:
    """Create an AutoGen agent tied to the local LLM with a fixed persona."""

    agent = ConversableAgent(
        name=persona["name"],
        system_message=persona["prompt"],
        llm_config=None  # avoid OpenAI schema validation
    )

    def local_reply_func(messages, sender, config):
        result = llm_client.create(messages)
        return result["choices"][0]["message"]["content"]

    agent.register_reply("default", reply_func=local_reply_func)
    return agent


def generate_conversation(config: dict, llm_client: LlamaCppWrapper, chat_id: int):
    """Generate one conversation and save as JSON log."""
    personalities = random.sample(config["personalities"], 2)
    turns = random.randint(config["min_turns"], config["max_turns"])

    # Create agents
    agent_a = create_agent(personalities[0], llm_client)
    agent_b = create_agent(personalities[1], llm_client)

    messages = []
    current_agent, next_agent = agent_a, agent_b

    # First user prompt to kick off conversation
    history = [{"role": "user", "content": f"Start a conversation with {next_agent.name}."}]
    response = current_agent.generate_reply(messages=history, sender=next_agent)
    messages.append({"speaker": current_agent.name, "text": response})

    # Alternate turns
    for _ in range(turns - 1):
        history = [{"role": "assistant", "content": messages[-1]["text"]}]
        response = next_agent.generate_reply(messages=history, sender=current_agent)
        messages.append({"speaker": next_agent.name, "text": response})
        current_agent, next_agent = next_agent, current_agent

    # Prepare log structure
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "participants": [
            {
                "name": personalities[0]["name"],
                "image": personalities[0]["image_file_name"],
                "color": personalities[0]["color"],
            },
            {
                "name": personalities[1]["name"],
                "image": personalities[1]["image_file_name"],
                "color": personalities[1]["color"],
            }
        ],
        "messages": messages,
    }

    # Save to file
    filename = os.path.join(LOGS_DIR, f"chat_{chat_id:03d}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved conversation to {filename}")


def main():
    config = load_config("config.json")
    ensure_logs_dir()

    model_path = config.get("model_path")
    if not model_path:
        raise ValueError("❌ No 'model_path' found in config.json")

    llm_client = LlamaCppWrapper(model_path=model_path)

    num_chats = config.get("num_chats", 5)  # default 5 if not in config
    for i in range(1, num_chats + 1):
        generate_conversation(config, llm_client, chat_id=i)


if __name__ == "__main__":
    main()
