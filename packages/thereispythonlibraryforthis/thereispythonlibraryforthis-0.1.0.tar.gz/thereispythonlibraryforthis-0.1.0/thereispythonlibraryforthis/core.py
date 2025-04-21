from .data import load_libraries
from .utils import normalize
from rapidfuzz import process

def find_libraries(prompt: str, limit: int = 10) -> list[str]:
    libs = load_libraries()
    prompt_norm = normalize(prompt)
    matches = process.extract(prompt_norm, libs, limit=limit, score_cutoff=30)
    return [match[0] for match in matches]
