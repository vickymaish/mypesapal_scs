import os
import json
import hashlib
import time
import logging
from rich.console import Console
from rich.table import Table
from diff import get_commit_history

# Initialize Rich console for output
console = Console()


# Configure logging
logging.basicConfig(
    filename="myscs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def commit(commit_message):
    """
    Commit the staged files to the repository with a given commit message.
    """
    # Step 1: Check if the index is empty (no staged files)
    index_path = ".myscs/index"
    if not os.path.exists(index_path) or os.path.getsize(index_path) == 0:
        print("No files staged for commit.")
        logging.warning("Commit attempt with no staged files.")
        return

    # Step 2: Read staged files from the index
    staged_files = []
    with open(index_path, "r") as index_file:
        for line in index_file:
            line = line.strip()
            if not line:  # Skip empty lines
                continue

            # Split line into file path and file hash
            parts = line.split()
            if len(parts) != 2:  # Skip malformed lines that don't contain exactly two parts
                console.print(f"[bold yellow]Skipping malformed line: {line}[/bold yellow]")
                logging.warning(f"Skipping malformed line: {line}")
                continue

            file_path, file_hash = parts
            staged_files.append((file_path, file_hash))

    # Step 3: Create the commit object data
    commit_data = {
        "commit_message": commit_message,
        "timestamp": time.time(),
        "parent_commit": get_current_commit_hash(),  # Reference to the parent commit
        "files": staged_files,
        "author": "Victor Maina"
    }
    commit_data_str = json.dumps(commit_data, indent=4)

    # Step 4: Calculate the hash for the commit object
    commit_hash = hashlib.sha1(commit_data_str.encode('utf-8')).hexdigest()

    # Log the commit path and the commit data
    commit_path = f".myscs/objects/{commit_hash}"
    logging.info(f"Saving commit object to: {commit_path}")
    logging.info(f"Commit data: {commit_data_str}")

    # Step 5: Save the commit object to the object directory
    with open(commit_path, "w") as commit_file:
        commit_file.write(commit_data_str)
    logging.info(f"Commit object created with hash {commit_hash}")

    # Step 6: Update HEAD to point to the new commit
    with open(".myscs/HEAD", "w") as head_file:
        head_file.write(f"ref: refs/heads/main\n{commit_hash}")
    
    # Step 7: Update refs/heads/main to point to the new commit (to sync HEAD with branch)
    with open(".myscs/refs/heads/main", "w") as branch_file:
        branch_file.write(commit_hash)

    print(f"Commit successful. Commit hash: {commit_hash}")
    logging.info(f"Commit completed successfully. Commit hash: {commit_hash}")

def get_current_commit_hash():
    """
    Get the current commit hash from the HEAD file.
    Returns None if HEAD is not present or points to the initial commit.
    """
    head_path = ".myscs/HEAD"
    if os.path.exists(head_path):
        with open(head_path, "r") as head_file:
            content = head_file.read().strip()
            if content.startswith("ref: refs/heads/main"):
                return content.split()[-1]  # Extract the commit hash
    return None

def merge(target_branch):
    """
    Merge the current branch with the target branch.
    If the branches have diverged, a three-way merge is performed.
    """
    current_branch = get_current_branch_and_commit()  # Get the current active branch
    if current_branch == target_branch:
        print("You are already on the target branch.")
        return

    target_commit_hash = get_commit_hash_for_branch(target_branch)
    if not target_commit_hash:
        print(f"Error: Branch '{target_branch}' does not exist.")
        return

    # Perform a simple merge or three-way merge
    merge_result = perform_merge(current_branch, target_branch)
    if merge_result:
        print(f"Merge successful. Merged {target_branch} into {current_branch}.")
    else:
        print(f"Merge conflict detected. Unable to merge {target_branch} into {current_branch}.")

def get_commit_hash_for_branch(branch_name):
    """
    Get the commit hash for the specified branch from the .myscs/refs/heads directory.
    """
    branch_path = f".myscs/refs/heads/{branch_name}"
    if os.path.exists(branch_path):
        with open(branch_path, "r") as branch_file:
            return branch_file.read().strip()
    return None

def perform_merge(current_branch, target_branch):
    """
    Perform the merge operation.
    This will check for diverged commits and attempt to merge them.
    For now, we assume the merge always succeeds.
    """
    # Here, you would check if the branches have diverged and implement the merge logic.
    # For now, we're assuming a simple merge without checking for conflicts.
    
    return True  # Simplified for demonstration purposes

def get_current_branch_and_commit():
    """
    Retrieve the current branch and latest commit hash from HEAD.
    """
    head_path = ".myscs/HEAD"
    if os.path.exists(head_path):
        with open(head_path, "r") as head_file:
            lines = head_file.readlines()  # Read all lines
            branch = lines[0].strip().split("/")[-1] if len(lines) > 0 else None
            if len(lines) > 1:  # Ensure the commit hash exists in the second line
                commit_hash = lines[1].strip()
                return branch, commit_hash
            else:
                logging.error("HEAD file does not contain a commit hash.")
                console.print("[bold red]Error: No commit hash found in HEAD file.[/bold red]")
                return branch, None
    logging.error("HEAD file is missing.")
    console.print("[bold red]Error: HEAD file is missing.[/bold red]")
    return None, None

def get_commit_history(commit_hash):
    """
    Recursively fetch the commit history for a given commit hash.
    Returns a list of commit details in reverse order (latest commit first).
    """
    commit_history = []
    while commit_hash:
        commit_path = f".myscs/objects/{commit_hash}"
        if not os.path.exists(commit_path):
            #console.print(f"[bold red]Error: Commit object {commit_hash} not found.[/bold red]")
            break
        with open(commit_path, "r") as commit_file:
            commit_data = json.load(commit_file)
            commit_history.append({
                "commit_hash": commit_hash,
                "commit_message": commit_data.get("commit_message", ""),
                "timestamp": commit_data.get("timestamp", ""),
                "author": commit_data.get("author", "Unknown"),
                "parent_commit": commit_data.get("parent_commit", None),
            })
            # Move to the parent commit
            commit_hash = commit_data.get("parent_commit")

    # Reverse the order to have the latest commit first
    return commit_history[::-1]

def view_commit_history():
    """
    Display the commit history for the current branch, starting from the latest commit (HEAD).
    """
    try:
        # Step 1: Get current branch and commit hash
        current_branch, latest_commit_hash = get_current_branch_and_commit()
        if not current_branch:
            console.print("[bold red]Error: No valid branch found in HEAD.[/bold red]")
            return
        if not latest_commit_hash:
            console.print(f"[bold red]Error: No valid commit hash found for branch '{current_branch}'.[/bold red]")
            return

        console.print(f"[bold green]Current branch: {current_branch}[/bold green]")
        console.print(f"[bold blue]Latest commit hash: {latest_commit_hash}[/bold blue]")

        # Step 2: Get commit history
        commit_history = get_commit_history(latest_commit_hash)
        if not commit_history:
            console.print(f"[bold yellow]No commits found for branch '{current_branch}'.[/bold yellow]")
            return

        # Step 3: Initialize table for output
        table = Table(title=f"Commit History for {current_branch}", style="bold green")
        table.add_column("Commit Hash", justify="right", style="cyan", no_wrap=True)
        table.add_column("Message", style="magenta")
        table.add_column("Date", style="dim")
        table.add_column("Author", style="yellow")

        # Step 4: Populate and display the table
        for commit in commit_history:
            commit_timestamp = time.ctime(commit['timestamp'])
            table.add_row(commit['commit_hash'][:7], commit['commit_message'], commit_timestamp, commit['author'])

        console.print(table)

    except Exception as e:
        console.print(f"[bold red]Error displaying commit history: {e}[/bold red]")
        logging.error(f"Error displaying commit history: {e}")

if __name__ == "__main__":
    commit("Initial commit")
