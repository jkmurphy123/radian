import json

def load_config(path: str) -> dict:
    """Load the JSON configuration file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
