import os
import json
import subprocess
import openai

SECRETS_FILE = "secrets.json"
CONFIG_FILE = "config.json"
MAX_DIFF_CHARS = 3000
SKIP_EXTENSIONS = (".zip", ".pdf", ".svg", ".png", ".jpg", ".brd", ".sch")

def load_api_key():
    if os.environ.get("OPENAI_API_KEY"):
        return os.environ["OPENAI_API_KEY"]

    with open(SECRETS_FILE) as f:
        secrets = json.load(f)
    return secrets["openai_api_key"]

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {"favorites": []}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

def load_model():
    config = load_config()
    return config.get("openai_model", "gpt-4o")

def get_modified_files(repo_path):
    result = subprocess.run(
        ["git", "-C", repo_path, "status", "--porcelain"],
        stdout=subprocess.PIPE,
        text=True
    )
    modified = []
    for line in result.stdout.strip().splitlines():
        if len(line) < 4:
            continue
        status = line[:2]
        filename = line[3:] if line[2] == ' ' else line[2:].strip()
        modified.append(filename)
    return modified

def has_unmerged_files(repo_path):
    result = subprocess.run(
        ["git", "-C", repo_path, "status", "--porcelain"],
        stdout=subprocess.PIPE,
        text=True
    )
    return any(line.startswith("U") for line in result.stdout.strip().splitlines())

def is_branch_behind(repo_path):
    subprocess.run(["git", "-C", repo_path, "fetch"])
    result = subprocess.run(
        ["git", "-C", repo_path, "status"],
        stdout=subprocess.PIPE,
        text=True
    )
    return "behind" in result.stdout

def offer_pull(repo_path):
    if is_branch_behind(repo_path):
        choice = input("🔄 Your branch is behind the remote. Pull now? (y/n): ").strip().lower()
        if choice == "y":
            subprocess.run(["git", "-C", repo_path, "pull"])

def ask_gpt_commit_message(filename, repo_path, repo_type):
    if filename.lower().endswith(SKIP_EXTENSIONS):
        return f"Update {filename}: binary or non-text file (GPT skipped)."

    result = subprocess.run(
        ["git", "-C", repo_path, "diff", filename],
        stdout=subprocess.PIPE,
        text=True,
        encoding='utf-8',
        errors='replace'
    )
    diff = result.stdout.strip()[:MAX_DIFF_CHARS] or "(No diff available. File may be staged or new.)"

    context = {
        "eagle": "This is an EAGLE PCB design repository. Generate a concise commit message based on schematic updates, board layout changes, or regenerated Gerber files.",
        "generic": "This is a general-purpose code or documentation repository. Generate a commit message based on the diff, focusing on what was added, removed, or updated.",
        "firmware": "This is a firmware repository for embedded systems. Generate a commit message based on source code updates, configuration changes, or device-specific logic modifications.",
        "docs": "This is a documentation repository. Generate a clear commit message that describes edits to markdown files, content structure, or instructional material.",
        "website": "This is a web development project. Generate a commit message for HTML, CSS, JavaScript, or framework-based updates (e.g., React, Vue, Django).",
        "cli": "This is a command-line application project. Generate a commit message reflecting improvements to CLI functionality, flags, I/O handling, or user feedback.",
        "data": "This is a data-focused repository. Generate a commit message for changes to datasets, data processing scripts, or analysis results.",
        "api": "This is an API or backend project. Generate a commit message describing changes to routes, controllers, models, or service logic.",
        "desktop": "This is a desktop application project. Generate a commit message for UI changes, feature additions, or performance improvements in desktop software.",
        "testing": "This is a test suite or QA automation project. Generate a commit message describing new tests, assertions, coverage improvements, or bug reproductions."
    }

    prompt = f"""Write a Git commit message for `{filename}` based on this diff:\n\n--- BEGIN DIFF ---\n{diff}\n--- END DIFF ---\n\n{context.get(repo_type, context['generic'])}"""

    try:
        model = load_model()
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful Git assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ GPT error for {filename}: {e}"

def commit_and_push(files, repo_path, repo_type):
    for file in files:
        print(f"🔍 Generating commit message for {file}...")
        msg = ask_gpt_commit_message(file, repo_path, repo_type)
        print(f"💬 Commit message: {msg}")
        subprocess.run(["git", "-C", repo_path, "add", file])
        subprocess.run(["git", "-C", repo_path, "commit", "-m", msg])
    offer_pull(repo_path)
    print("📤 Pushing to remote...")
    subprocess.run(["git", "-C", repo_path, "push"])
