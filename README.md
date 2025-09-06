# radian
2 autogen agents chatting with each other


project/
│── config.json
│── conversation_generator.py
│── llm_wrapper.py
│── config_loader.py
│── logs/
│     └── (generated chat logs here)

# 1) Create & activate a venv (example)
cd projects
python3 -m venv llm_env
source llm_env/bin/activate  
cd radion

# 2) Install deps
pip install -r requirements.txt

# 3) To generate new conversations
python conversation_generator.py

# 4) Toplay teh conversations in a loop
python ?