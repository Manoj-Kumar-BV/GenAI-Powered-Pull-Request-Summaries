from dotenv import load_dotenv
load_dotenv()
import subprocess
import requests
import os
import json
import re

def fetch_pr_files(repo, pr):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr}/files"
    headers = {}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    resp = requests.get(url, headers=headers)
    if resp.status_code == 404:
        print(f"[!] PR #{pr} not found in {repo}. Please check the PR number.")
        return None
    resp.raise_for_status()
    return resp.json()

def summarize_patch_with_llm(filename, patch, spec_context=None):
    OLLAMA_URL = "http://localhost:11434/api/generate"
    prompt = f"""
You are an expert software reviewer. Given the following file diff, write a professional summary for inclusion in a pull request review. Your summary must enable reviewers to quickly understand:

Section: File Name
State the file name (plain text).

Section: Summary of Changes
Concisely describe what this patch introduces, modifies, or removes in this file.

Section: Reason for Change
Summarize why these changes are necessary or valuable.

Section: Standards/Specification Reference
If the change relates to OpenMP or other standards, explain how and where. Reference relevant sections if possible. If not applicable, state "Not applicable".

Section: Reviewer Notes
List any important caveats, edge cases, or points reviewers should pay attention to.

Do NOT use lists, markdown, or formatting characters like *, #, or -; use plain clear text. Avoid repetition.

File: {filename}

Diff:
{patch}

OpenMP Specification Context:
{spec_context if spec_context and spec_context.strip() else "N/A"}
"""
    response = requests.post(
        OLLAMA_URL,
        json={"model": "llama3", "prompt": prompt, "stream": False}
    )
    return response.json()["response"].strip()

def get_spec_context(patch, topk=2):
    QUERY_SCRIPT = "query_openmp_faiss.py"
    result = subprocess.run(
        ["python", QUERY_SCRIPT, patch[:1000], str(topk)],
        capture_output=True, text=True
    )
    return result.stdout

def strip_markdown(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'__(.*?)__', r'\1', text)
    text = re.sub(r'`(.*?)`', r'\1', text)
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^>\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^-{3,}$', '', text, flags=re.MULTILINE)
    return text

def format_markdown(summaries):
    md_lines = []
    for s in summaries:
        md_lines.append(f"### File: {s['filename']}\n")
        md_lines.append(s['summary'])
        md_lines.append("\n---\n")
    return "\n".join(md_lines)

def format_text(summaries):
    txt_lines = []
    for s in summaries:
        txt_lines.append(f"File: {s['filename']}\n")
        txt_lines.append(strip_markdown(s['summary']))
        txt_lines.append("\n" + "="*40 + "\n")
    return "\n".join(txt_lines)

def format_json(summaries):
    summaries_clean = []
    for s in summaries:
        summaries_clean.append({
            "filename": s['filename'],
            "summary": strip_markdown(s['summary'])
        })
    return json.dumps(summaries_clean, indent=2, ensure_ascii=False)

def ensure_summaries_folder():
    summaries_dir = os.path.join(os.getcwd(), "summaries")
    if not os.path.exists(summaries_dir):
        os.makedirs(summaries_dir)
    return summaries_dir

def summarize_pr_for_cli(repo, pr):
    print(f"\nFetching files for PR #{pr} in {repo}...\n")
    pr_files = fetch_pr_files(repo, int(pr))
    if pr_files is None:
        return

    summaries = []
    for patch_file in pr_files:
        filename = patch_file["filename"]
        patch = patch_file.get("patch", "")
        if not patch:
            continue
        print(f"Finding relevant OpenMP spec for {filename}...")
        spec_context = get_spec_context(patch)
        print(f"Summarizing {filename}...")
        summary = summarize_patch_with_llm(filename, patch, spec_context)
        summaries.append({
            "filename": filename,
            "summary": summary
        })

    print("\nSummaries:\n")
    print(format_text(summaries))

    while True:
        print("Export summary as:")
        print("1. Markdown (.md)")
        print("2. Plain text (.txt)")
        print("3. JSON (.json)")
        print("4. Skip export")
        choice = input("Enter your choice (1/2/3/4): ").strip()
        if choice == "4":
            print("Export skipped.")
            break
        elif choice in ("1", "2", "3"):
            filename = input("Enter filename (without extension): ").strip()
            if not filename:
                filename = "summary"
            summaries_dir = ensure_summaries_folder()
            filepath = os.path.join(summaries_dir, filename)
            if choice == "1":
                out = format_markdown(summaries)
                ext = ".md"
            elif choice == "2":
                out = format_text(summaries)
                ext = ".txt"
            else:
                out = format_json(summaries)
                ext = ".json"
            fullpath = filepath + ext
            with open(fullpath, "w", encoding="utf-8") as f:
                f.write(out)
            print(f"Summaries exported to {fullpath}\n")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")