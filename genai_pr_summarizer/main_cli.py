from termcolor import colored
from colorama import init as colorama_init
from genai_pr_summarizer.summarize_pr import summarize_pr_for_cli

colorama_init()

def print_cli_prompt():
    user = colored('genai', 'red', attrs=['bold'])
    host = colored('pr-summarizer', 'yellow', attrs=['bold'])
    path = colored('~', 'blue')
    prompt = f"{user}@{host}:{path}$ "
    return prompt

def run_cli():
    while True:
        prompt = print_cli_prompt()
        repo = input(prompt + colored("Enter GitHub repo (owner/repo) or 'q' to quit: ", "white"))
        if repo.strip().lower() == 'q':
            print(colored("Exiting.", "cyan"))
            break
        pr = input(prompt + colored("Enter PR number: ", "white"))
        if pr.strip().lower() == 'q':
            print(colored("Exiting.", "cyan"))
            break
        if not pr.isdigit():
            print(colored("[!] Please enter a valid PR number.\n", 'red'))
            continue
        summarize_pr_for_cli(repo, int(pr))
        again = input(prompt + colored("Summarize another PR? (y/n): ", "white"))
        if again.strip().lower() != 'y':
            print(colored("Thank you for using Gen AI PR Summarizer!", "cyan"))
            break