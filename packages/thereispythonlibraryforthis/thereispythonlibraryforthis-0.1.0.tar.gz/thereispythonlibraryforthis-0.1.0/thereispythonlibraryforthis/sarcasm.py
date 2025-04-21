from .config import SARCASM_MAP

def sarcastic_response(prompt: str, libraries: list[str]) -> str:
    if not libraries:
        return "Oh wow. No libraries found. Truly a groundbreaking idea. 🧠"

    for keyword, tone in SARCASM_MAP.items():
        if keyword in prompt.lower():
            break
    else:
        tone = "Here's what I found. Don't blame me if it's cursed."

    return f"{tone}\n\n" + "\n".join(f"- {lib}" for lib in libraries)
