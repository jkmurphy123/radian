import os
import json
import random
from datetime import datetime
from config_loader import load_config
from llm_wrapper import LlamaCppWrapper

# AutoGen agents
from autogen import ConversableAgent

LOGS_DIR = "logs"

def ensure_logs_dir():
    os.makedirs(LOGS_DIR, exist_ok=True)

def create_agent(name: str, prompt: str, llm_client: LlamaCppWrapper) -> ConversableAgent:
    agent = ConversableAgent(
        name=name,
        system_message=prompt,
        llm_config=None
    )

    def custom_reply_func(messages, sender, config):
        response = llm_client.create(messages)
        return response["choices"][0]["message"]["content"]

    agent.register_reply(reply_func=custom_reply_func)
    return agent

def generate_conversation(config: dict, llm_client: LlamaCppWrapper, chat_id: int):
    """Generate one conversation and save as JSON log."""
    personalities = random.sample(config["personalities"], 2)

    turns = random.randint(config["min_turns"], config["max_turns"])

    # Create agents
    agent_a = create_agent(personalities[0]["name"], personalities[0]["prompt"], llm_client)
    agent_b = create_agent(personalities[1]["name"], personalities[1]["prompt"], llm_client)

    # Start conversation
    messages = []
    current_speaker = agent_a
    next_speaker = agent_b

    first_message = f"Let's begin a conversation between {personalities[0]['name']} and {personalities[1]['name']}."
    response = current_speaker.generate_reply(messages=[{"role": "user", "content": first_message}])
    messages.append({"speaker": current_speaker.name, "text": response})

    for _ in range(turns - 1):
        response = next_speaker.generate_reply(messages=[{"role": "assistant", "content": messages[-1]["text"]}])
        messages.append({"speaker": next_speaker.name, "text": response})
        current_speaker, next_speaker = next_speaker, current_speaker

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

    # Save log
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

    num_chats = 5  # could also make this a config value
    for i in range(1, num_chats + 1):
        generate_conversation(config, llm_client, chat_id=i)

if __name__ == "__main__":
    main()
