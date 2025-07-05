from pyfiglet import Figlet
from termcolor import colored
from colorama import init as colorama_init
import requests
import sys

OLLAMA_URL = "http://localhost:11434"

def check_ollama_running():
    try:
        r = requests.get(OLLAMA_URL + "/api/tags", timeout=3)
        if r.status_code == 200:
            return True
    except Exception:
        pass
    print(colored(
        "\nError: Ollama server is not running at http://localhost:11434.\n"
        "Please start Ollama on your machine before using this tool.\n"
        "See the README for installation and startup instructions.\n",
        "red", attrs=["bold"]
    ))
    return False

def print_banner():
    f = Figlet(font='slant')
    print(colored(f.renderText('Gen AI PR Summarizer'), 'cyan'))
    f2 = Figlet(font='small')
    print(colored(f2.renderText('Offline - LLM - Vector Search'), 'yellow'))

def print_intro():
    print(colored("Welcome to the Gen AI PR Summarizer CLI!\n", 'green', attrs=['bold']))
    print(colored(
        "This tool fetches a GitHub PR, analyzes each changed file, and generates accurate, professional summaries.\n"
        "You can export results as Markdown, text, or JSON.\n", "white"
    ))
    print(colored("How to use:", "yellow", attrs=['bold']))
    print(colored("  - Enter the GitHub repo (owner/repo), e.g., llvm/llvm-project", "white"))
    print(colored("  - Enter the pull request number", "white"))
    print(colored("  - Choose export format: Markdown, text, or JSON", "white"))
    print(colored("  - Type 'q' at any prompt to exit\n", "white"))

def main():
    colorama_init()
    print_banner()
    print_intro()
    if not check_ollama_running():
        sys.exit(1)
    import genai_pr_summarizer.main_cli
    genai_pr_summarizer.main_cli.run_cli()

if __name__ == "__main__":
    main()