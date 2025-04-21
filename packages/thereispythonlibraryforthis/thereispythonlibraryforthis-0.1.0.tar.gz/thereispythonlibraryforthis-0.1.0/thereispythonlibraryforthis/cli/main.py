import sys
from ..core import find_libraries
from ..sarcasm import sarcastic_response

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m thereispythonlibraryforthis <your-task-prompt>")
        return

    prompt = " ".join(sys.argv[1:])
    libs = find_libraries(prompt)
    print(sarcastic_response(prompt, libs))
