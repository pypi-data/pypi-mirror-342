import re

def normalize(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9 ]", "", text.lower().strip())
