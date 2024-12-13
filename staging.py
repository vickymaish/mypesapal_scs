import os
import logging
import hashlib
from fnmatch import fnmatch
from rich.console import Console
from rich.text import Text

# Initialize Rich console for output
console = Console()

# Configure logging
logging.basicConfig(
    filename="myscs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_myscsignore():
    """
    Load patterns from the .myscsignore file.
    Returns a list of patterns.
    """
    ignore_file = ".myscsignore"
    patterns = []
    if os.path.exists(ignore_file):
        with open(ignore_file, "r") as f:
            for line in f:
                # Ignore empty lines and comments
                line = line.strip()
                if line and not line.startswith("#"):
                    patterns.append(line)
    return patterns

def is_ignored(file_path, ignore_patterns):
    """
    Check if a file matches any pattern in the .myscsignore file.
    """
    for pattern in ignore_patterns:
        if fnmatch(file_path, pattern):
            return True
    return False

def stage_file(file_path):
    """
    Stage a file by adding it to the .myscs/index file.
    """
    # If the file path is '.', stage all non-ignored files
    if file_path == ".":
        files = [f for f in os.listdir() if os.path.isfile(f) and not is_ignored(f, load_myscsignore())]
        for file in files:
            stage_single_file(file)
        return

    # Stage the file normally
    stage_single_file(file_path)

def stage_single_file(file_path):
    """
    Stage a single file and add it to the .myscs/index file.
    """
    # Load ignore patterns
    ignore_patterns = load_myscsignore()

    # Check if the file is ignored
    if is_ignored(file_path, ignore_patterns):
        console.print(Text(f"Skipped: File '{file_path}' is ignored (matches .myscsignore).", style="yellow"))
        logging.info(f"Skipped staging file '{file_path}' due to .myscsignore rules.")
        return

    # Check if the file exists
    if not os.path.exists(file_path):
        console.print(Text(f"Error: File '{file_path}' not found in the working directory.", style="bold red"))
        logging.warning(f"File '{file_path}' not found.")
        return

    try:
        # Calculate the file hash
        hasher = hashlib.sha1()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        file_hash = hasher.hexdigest()

        # Ensure the index file exists
        index_path = ".myscs/index"
        if not os.path.exists(index_path):
            with open(index_path, 'w') as _:
                pass  # Create an empty index file

        # Load current index entries
        staged_files = set()
        with open(index_path, 'r') as index_file:
            for line in index_file:
                staged_files.add(line.strip())

        # Check for duplicates
        entry = f"{file_path} {file_hash}"
        if entry in staged_files:
            console.print(Text(f"File '{file_path}' is already staged.", style="yellow"))
            logging.info(f"File '{file_path}' already staged. Skipping.")
            return

        # Add the new entry to the index
        with open(index_path, 'a') as index_file:
            index_file.write(entry + "\n")

        console.print(Text(f"Success: File '{file_path}' staged successfully.", style="bold green"))
        logging.info(f"File '{file_path}' added to the index with hash {file_hash}.")

    except Exception as e:
        console.print(Text(f"Error staging the file. Details: {str(e)}", style="bold red"))
        logging.error(f"Error staging the file '{file_path}': {str(e)}")
