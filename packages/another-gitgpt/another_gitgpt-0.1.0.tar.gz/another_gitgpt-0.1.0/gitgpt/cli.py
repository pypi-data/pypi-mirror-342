import os
import sys
import openai
import subprocess
from gitgpt import core, __version__

openai.api_key = core.load_api_key()

def list_subfolders(path):
    try:
        return [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    except PermissionError:
        return []

def select_git_repo():
    current_path = "C:\\"
    while True:
        subfolders = list_subfolders(current_path)
        print(f"\n📂 Current folder: {current_path}")
        print("0. [Select this folder]")
        for i, folder in enumerate(subfolders, 1):
            print(f"{i}. {folder}")
        print("B. [Back]")

        choice = input("Select folder: ").strip().upper()

        if choice == "0":
            if os.path.isdir(os.path.join(current_path, ".git")):
                return current_path
            else:
                print("❌ Not a Git repository. Try another folder.")
        elif choice == "B":
            parent = os.path.dirname(current_path.rstrip("\\"))
            if parent and parent != current_path:
                current_path = parent
        elif choice.isdigit() and 1 <= int(choice) <= len(subfolders):
            current_path = os.path.join(current_path, subfolders[int(choice) - 1])
        else:
            print("❓ Invalid choice.")

def select_git_repo_with_favorites():
    config = core.load_config()
    favorites = config.get("favorites", [])

    while True:
        print("\n⭐ Favorite Git Repos:")
        for i, entry in enumerate(favorites, 1):
            print(f"{i}. {entry['path']} ({entry['type']})")
        print("B. [Browse for new folder]")

        choice = input("Select repo or browse: ").strip().upper()

        if choice == "B":
            path = select_git_repo()
            repo_type = input("📂 Is this an EAGLE repo or generic? (eagle/generic): ").strip().lower()
            if repo_type not in ["eagle", "generic"]:
                repo_type = "generic"
            if not any(f["path"] == path for f in favorites):
                add = input("💾 Add to favorites? (y/n): ").strip().lower()
                if add == "y":
                    favorites.append({"path": path, "type": repo_type})
                    config["favorites"] = favorites
                    core.save_config(config)
            return path, repo_type
        elif choice.isdigit() and 1 <= int(choice) <= len(favorites):
            entry = favorites[int(choice) - 1]
            return entry["path"], entry["type"]
        else:
            print("❓ Invalid choice.")

def list_and_select_model():
    try:
        models_data = openai.models.list()
        all_models = sorted(
            m.id for m in models_data.data 
            if m.id.startswith("gpt-") and not m.id.endswith("-vision")
        )
    except Exception as e:
        print(f"❌ Failed to retrieve models: {e}")
        return

    if not all_models:
        print("⚠️ No GPT models found in your account.")
        return

    print("\n🧠 Available OpenAI Models:")
    for i, model_id in enumerate(all_models, 1):
        print(f"{i}. {model_id}")
    print("Q. Quit")

    choice = input("\nSelect a model [1-{}]: ".format(len(all_models))).strip().lower()
    if choice == "q":
        return

    if choice.isdigit() and 1 <= int(choice) <= len(all_models):
        selected_model = all_models[int(choice) - 1]
        config = core.load_config()
        config["openai_model"] = selected_model
        core.save_config(config)
        print(f"✅ Model set to: {selected_model}")
    else:
        print("❌ Invalid choice.")

def view_or_remove_favorites():
    config = core.load_config()
    favorites = config.get("favorites", [])

    if not favorites:
        print("📁 No favorite repositories saved.")
        return

    print("\n⭐ Current Favorites:")
    for i, entry in enumerate(favorites, 1):
        print(f"{i}. {entry['path']} ({entry['type']})")
    print("D. Delete a favorite")
    print("Q. Quit")

    choice = input("\nChoose an option: ").strip().upper()

    if choice == "D":
        index = input("Enter the number of the favorite to remove: ").strip()
        if index.isdigit() and 1 <= int(index) <= len(favorites):
            removed = favorites.pop(int(index) - 1)
            print(f"❌ Removed: {removed['path']}")
            config["favorites"] = favorites
            core.save_config(config)
        else:
            print("❌ Invalid index.")

def show_config():
    config = core.load_config()
    print("\n🛠 Current Configuration:\n")
    print(json.dumps(config, indent=2))

def clear_cache():
    confirm = input("⚠️ Are you sure you want to clear all favorites and model? (y/n): ").strip().lower()
    if confirm == "y":
        core.save_config({"favorites": []})
        print("🧹 Cleared all cached favorites and model.")
    else:
        print("❎ Cancelled.")

def show_help_banner():
    print("\n🧠 GitGPT - AI-Powered Git Commit Assistant")
    print("🚀 Smarter commits using OpenAI and git diff\n")

    print("📦 Core Commands:")
    print("  🧠 push          → Scan, generate GPT commit messages, commit, and push")
    print("  🔧 model         → Select and change OpenAI model")
    print("  ⭐ favorites     → View/remove favorite Git repositories")
    print("  🛠 config        → Show current configuration")
    print("  🧹 clear-cache   → Remove all favorites and reset model")
    print("  ⬆️  upgrade       → Pull latest Git changes or upgrade via PyPI")
    print("  🔍 status        → Show git status (short)")
    print("  📥 pull          → Git pull from the current repo")
    print("  📜 log           → Show recent commit history")
    print("  📤 stage         → Stage all modified files")
    print("  🧾 version       → Show current installed version")
    print("  ❓ help          → Show this help message\n")

    print("🧭 Aliases:")
    print("  fav   → favorites")
    print("  cfg   → config")
    print("  reset → clear-cache")
    print("  ver   → version")
    print("  up    → upgrade\n")

    print("✨ Run `gitgpt` with no arguments to launch the interactive commit assistant.\n")

def show_version():
    print(f"🧠 GitGPT version {__version__}")

from gitgpt import __version__

def show_version():
    print(f"🧠 GitGPT version {__version__}")

def upgrade_gitgpt():
    import subprocess
    from datetime import datetime

    log_file = os.path.join(os.path.expanduser("~"), "gitgpt_upgrade_log.txt")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log = [f"\n🔧 GitGPT Upgrade Log — {timestamp}"]

    print("\n⬆️  Upgrading GitGPT...")

    repo_path = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(repo_path, ".."))
    git_dir = os.path.join(project_root, ".git")

    try:
        if os.path.exists(git_dir):
            # Git upgrade
            print("📥 Pulling latest changes from Git...")
            result1 = subprocess.run(["git", "-C", project_root, "pull"], check=True, capture_output=True, text=True)
            log.append(result1.stdout)

            print("📦 Reinstalling updated package...")
            result2 = subprocess.run(["pip", "install", "."], cwd=project_root, check=True, capture_output=True, text=True)
            log.append(result2.stdout)

            print("✅ GitGPT upgraded from GitHub.")
            log.append("✅ Upgrade successful from GitHub.")
        else:
            # PyPI upgrade
            print("📦 Upgrading via PyPI...")
            result = subprocess.run(["pip", "install", "--upgrade", "gitgpt"], check=True, capture_output=True, text=True)
            log.append(result.stdout)
            print("✅ GitGPT upgraded via PyPI.")
            log.append("✅ Upgrade successful via PyPI.")
    except subprocess.CalledProcessError as e:
        error_message = f"❌ Upgrade failed: {e}"
        print(error_message)
        log.append(error_message)

    # Write upgrade log
    with open(log_file, "a", encoding="utf-8") as f:
        f.write("\n".join(log) + "\n")

    # Show final version
    from gitgpt import __version__
    print(f"🔢 Current GitGPT version: {__version__}")
    print(f"📄 Upgrade log saved to: {log_file}")

def run_push_workflow():
    repo_path, repo_type = select_git_repo_with_favorites()
    print(f"📍 Using Git repo: {repo_path} ({repo_type})")

    if core.has_unmerged_files(repo_path):
        print("❌ Merge conflicts detected. Resolve before continuing.")
        return

    modified_files = core.get_modified_files(repo_path)
    if not modified_files:
        print("✅ No changes to push.")
        return

    print(f"📝 Found {len(modified_files)} files to commit.")
    core.commit_and_push(modified_files, repo_path, repo_type)

def interactive_commit_flow():
    openai_key = core.load_api_key()
    if not openai_key:
        print("❌ No OpenAI API key found. Please check secrets.json.")
        return

    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        command_map = {
            "model": list_and_select_model,
            "favorites": view_or_remove_favorites,
            "fav": view_or_remove_favorites,
            "config": show_config,
            "cfg": show_config,
            "clear-cache": clear_cache,
            "reset": clear_cache,
            "help": show_help_banner,
            "--help": show_help_banner,
            "-h": show_help_banner,
            "version": show_version,
            "ver": show_version,
            "--version": show_version,
            "--ver": show_version,
            "upgrade": upgrade_gitgpt,
            "up": upgrade_gitgpt,

            # 🧠 Git-like commands
            "push": run_push_workflow,
            "pull": lambda: subprocess.run(["git", "pull"]),
            "status": lambda: subprocess.run(["git", "status", "-sb"]),
            "log": lambda: subprocess.run(["git", "log", "--oneline", "-n", "10"]),
            "stage": lambda: subprocess.run(["git", "add", "."]),
        }


        if cmd in command_map:
            command_map[cmd]()  # ✅ Call the associated function
            return
        else:
            print(f"❓ Unknown command: {cmd}")
            show_help_banner()
            return

    # 🧭 Default interactive flow
    repo_path, repo_type = select_git_repo_with_favorites()
    print(f"✅ Selected Git repo: {repo_path} ({repo_type})")

    if core.has_unmerged_files(repo_path):
        print("❌ Merge conflicts detected. Please resolve them before committing.")
        return

    modified_files = core.get_modified_files(repo_path)
    if not modified_files:
        print("✅ No changes to commit.")
        return

    print(f"📝 Found {len(modified_files)} files to commit.")
    core.commit_and_push(modified_files, repo_path, repo_type)

if __name__ == "__main__":
    interactive_commit_flow()

