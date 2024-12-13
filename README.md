## Feature 1: Initializing a Repository
Overview:
The system allows users to initialize a repository in a directory. This is the foundational step in creating a distributed source control system, similar to git init in Git. The repository is stored in a dot-prefixed subdirectory (i.e., .myscs), where all the essential information related to version control is stored.

## Key Operations:
Initialize Repository: Users can initialize a repository in any directory using the myscs init command. This command sets up a .myscs directory within the current directory.
Repository Structure:
.myscs: The main directory that holds the version control data.
.myscs/objects: Stores the commit objects (which hold the changes made to files).
.myscs/refs/heads: Contains references to different branches.
.myscs/index: This file keeps track of staged files ready for commit.
How It Works:
When a user runs myscs init, the system checks if the .myscs directory exists. If it doesn't, the system creates it along with the necessary subdirectories. The initialization also creates an empty index file and a HEAD file that references the default branch (main), marking the start of the repository.

# Initializing a repository 

def initialize_repository():
    """
    Initializes the repository by creating the .myscs directory structure.
    """
    if not os.path.exists(".myscs"):
        os.makedirs(".myscs/objects")
        os.makedirs(".myscs/refs/heads")
        with open(".myscs/index", "w") as f:
            pass  # Create an empty index file
        with open(".myscs/HEAD", "w") as head_file:
            head_file.write("ref: refs/heads/main\n")  # Default branch 'main'
        print("Repository initialized successfully.")



        
## Feature 2: Staging Files (git add)
Overview:
This feature allows users to stage files before committing them, just like the git add command in Git. The staged files are tracked in the .myscs/index file, which keeps a record of the file paths and their corresponding hashes. This step is essential for preparing files for a commit.

Key Operations:
Stage Files: Users can add files to the staging area using the myscs add <file_path> command. The file path and its hash are recorded in the .myscs/index file.
Check for Duplicates: If a file is already staged, it won’t be staged again, preventing redundancy.
Ignore Files: Files matching patterns in the .myscsignore file are ignored during staging. This prevents temporary files, logs, or build artifacts from being added to the repository.
How It Works:
Calculate Hash: The system computes the SHA-1 hash of each file to ensure its integrity and uniqueness.
Staging: Once the file is staged, its path and hash are written into the .myscs/index file. This file acts as a record of staged changes.
Skipping Already Staged Files: If a file has already been staged (based on its path and hash), the system skips staging it again and provides a message to inform the user.


# Staging a File
import hashlib
import os

def stage_file(file_path):
    """
    Stage a file by adding it to the .myscs/index file.
    """
    # Load ignore patterns
    ignore_patterns = load_myscsignore()

    # Check if the file is ignored
    if is_ignored(file_path, ignore_patterns):
        print(f"Skipped: File '{file_path}' is ignored (matches .myscsignore).")
        return

    # Calculate the file hash
    if os.path.exists(file_path):
        hasher = hashlib.sha1()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        file_hash = hasher.hexdigest()

        # Ensure the index file exists and is not empty
        index_path = ".myscs/index"
        staged_files = set()
        if os.path.exists(index_path):
            with open(index_path, 'r') as index_file:
                for line in index_file:
                    staged_files.add(line.strip())

        entry = f"{file_path} {file_hash}"
        if entry in staged_files:
            print(f"File '{file_path}' is already staged.")
        else:
            # Add the new entry to the index
            with open(index_path, 'a') as index_file:
                index_file.write(entry + "\n")
            print(f"Success: File '{file_path}' staged successfully.")
