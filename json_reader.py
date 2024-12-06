import json
from typing import Dict

def load_messages(file_path: str) -> Dict[str, Dict[str, str]]:
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)