import os
import json
import random
from datetime import datetime
from autogen import AssistantAgent, UserProxyAgent
from llama_cpp import Llama
from config_loader import load_config

LOGS_DIR = "logs"


class LlamaAssistant(AssistantAgent):
    """AssistantAgent subclass backed by llama.cpp"""

    def __init__(self, name: str, persona_prompt: str, model_path: str):
        super().__init__(name)
        self.llm = Llama(model_path=model_path, n_ctx=2048)
        self.persona_prompt = persona_prompt

    def generate_reply(self, sender, message, **kwargs):
        """Override to call local llama.cpp"""
        print(f"🚀 {self.name} (LLM) called with message from {sender.name}: {message['content']}")

        response = self.llm.create_chat_completion(
            messages=[
                {"role": "system", "content": self.persona_prompt},
                {"role": message["role"], "content": message["content"]},
            ],
            max_tokens=kwargs.get("max_tokens", 256),
            temperature=kwargs.get("temperature", 0.7),
        )

        reply_text = response["choices"][0]["message"]["content"].strip()

        return {
            "role": "assistant",
            "name": self.name,
            "content": reply_text,
        }


def ensure_logs_dir():
    os.makedirs(LOGS_DIR, exist_ok=True)


def generate_conversation(config: dict, chat_id: int):
    """Generate one conversation and save as JSON log."""

    # Pick 2 personalities
    personalities = random.sample(config["personalities"], 2)
    turns = random.randint(config["min_turns"], config["max_turns"])

    # Create assistants
    agent_a = LlamaAssistant(
        name=personalities[0]["name"],
        persona_prompt=personalities[0]["prompt"],
        model_path=config["model_path"],
    )

    agent_b = LlamaAssistant(
        name=personalities[1]["name"],
        persona_prompt=personalities[1]["prompt"],
        model_path=config["model_path"],
    )

    # Dummy user (always the sender)
    user = UserProxyAgent("user", code_execution_config={"use_docker": False})

    messages = []

    # Kick off conversation
    last_message = {"role": "user", "content": f"Let's start chatting, {agent_a.name}!", "name": "user"}
    current_speaker, next_speaker = agent_a, agent_b

    for i in range(turns):
        reply = current_speaker.generate_reply(sender=user, message=last_message)
        messages.append({"speaker": current_speaker.name, "text": reply["content"]})

        # Prepare next input message
        last_message = {
            "role": "assistant",
            "content": reply["content"],
            "name": current_speaker.name,
        }
        current_speaker, next_speaker = next_speaker, current_speaker

    # Build log
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
            },
        ],
        "messages": messages,
    }

    # Save to file
    existing = [f for f in os.listdir(LOGS_DIR) if f.startswith("chat_") and f.endswith(".json")]
    next_id = len(existing) + 1
    filename = os.path.join(LOGS_DIR, f"chat_{next_id:03d}.json")

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved conversation to {filename}")


def main():
    config = load_config("config.json")
    ensure_logs_dir()

    num_chats = config.get("num_chats", 5)
    for i in range(1, num_chats + 1):
        generate_conversation(config, chat_id=i)


if __name__ == "__main__":
    main()
