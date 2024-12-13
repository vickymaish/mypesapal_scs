# MyPesapal SCS Documentation

## Feature 1: Initializing a Repository and Storing it in a Dot-Subdirectory

### Objective:
The first feature of the MyPesapal SCS (Source Control System) is to initialize a repository in a directory and store all the repository data in a hidden `.myscs` folder, which behaves similarly to Git’s `.git` folder.

### Approach:
1. **Command to initialize the repository**:
   To initialize the repository, use the `myscs init` command. This will create the `.myscs` directory in the current working directory. Inside this directory, the following structure is created:

   .myscs/ ├── index ├── objects ├── refs/ │ └── heads/ └── HEAD

   2. **What Happens on Initialization**:
- The `.myscs` directory will be hidden from regular file listings.
- Essential files like `index`, `HEAD`, and `refs/heads` are created for tracking staged files, the latest commit, and branch information.

### Code Implementation:
```python
import os

def init_repo():
 """
 Initializes the repository by creating the necessary directory structure
 within a hidden `.myscs` directory.
 """
 repo_dir = ".myscs"
 
 # Check if repository already exists
 if os.path.exists(repo_dir):
     print("Repository already initialized.")
     return

 # Create necessary subdirectories
 os.makedirs(os.path.join(repo_dir, "objects"))
 os.makedirs(os.path.join(repo_dir, "refs", "heads"))
 
 # Create the HEAD file to track the current branch and commit
 with open(os.path.join(repo_dir, "HEAD"), "w") as head_file:
     head_file.write("ref: refs/heads/main\n")
 
 # Create an empty index file for staged files
 with open(os.path.join(repo_dir, "index"), "w") as index_file:
     pass

 print(f"Initialized an empty repository in {os.getcwd()}")



## Feature 2: Staging Files (`git add`)

### Objective:
Allow users to stage files for commit, similar to `git add`. This enables users to prepare their changes for the next commit.

### Approach:
- **Command**: `myscs add <file_path>` stages a specific file.
- **Index**: The `.myscs/index` file tracks staged files with their respective SHA-1 hashes.
- **File Ignoring**: Files matching patterns in the `.myscsignore` file are skipped.
- **Handling Duplicates**: Files already staged will not be added again to prevent redundant entries.

### Code Explanation:
```python
import os
import hashlib
from fnmatch import fnmatch
from rich.console import Console

# Initialize Rich console for output
console = Console()

def load_myscsignore():
    """
    Load ignore patterns from the .myscsignore file.
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
    # Load ignore patterns
    ignore_patterns = load_myscsignore()

    # Check if the file is ignored
    if is_ignored(file_path, ignore_patterns):
        console.print(f"Skipped: File '{file_path}' is ignored (matches .myscsignore).", style="yellow")
        return

    # Check if the file exists
    if not os.path.exists(file_path):
        console.print(f"Error: File '{file_path}' not found.", style="bold red")
        return

    try:
        # Calculate the file hash (SHA-1)
        hasher = hashlib.sha1()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        file_hash = hasher.hexdigest()

        # Ensure the index file exists
        index_path = ".myscs/index"
        if not os.path.exists(index_path):
            with open(index_path, 'w') as _:
                pass  # Create an empty index file if it doesn't exist

        # Load current index entries
        staged_files = set()
        with open(index_path, 'r') as index_file:
            for line in index_file:
                staged_files.add(line.strip())

        # Check for duplicates
        entry = f"{file_path} {file_hash}"
        if entry in staged_files:
            console.print(f"File '{file_path}' is already staged.", style="yellow")
            return

        # Add the new entry to the index
        with open(index_path, 'a') as index_file:
            index_file.write(entry + "\n")

        console.print(f"Success: File '{file_path}' staged successfully.", style="bold green")

    except Exception as e:
        console.print(f"Error staging the file. Details: {str(e)}", style="bold red")


