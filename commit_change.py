"""FUNCTION commit(commit_message):
    # Step 1: Check if there are files in the index (staged)
    IF .myscs/index is empty:
        PRINT "No files staged for commit."
        RETURN

    # Step 2: Collect staged files from the index
    READ .myscs/index to get file paths and their hashes

    # Step 3: Create commit data (metadata + staged file references)
    CREATE commit object with:
        - Parent commit (if any)
        - Timestamp
        - Commit message
        - References to staged files

    # Step 4: Generate a unique hash for the commit object
    CALCULATE commit hash using hashlib

    # Step 5: Save the commit object to .myscs/objects
    CREATE a file in .myscs/objects using the hash as the filename
    WRITE commit data to the file

    # Step 6: Update HEAD to point to the new commit
    WRITE "ref: refs/heads/main" to .myscs/HEAD

    PRINT "Commit successful."

    """

import os
import json
import hashlib
import time
import logging

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
            file_path, file_hash = line.strip().split()
            staged_files.append((file_path, file_hash))

    # Step 3: Create the commit object data
    commit_data = {
        "commit_message": commit_message,
        "timestamp": time.time(),
        "parent_commit": get_current_commit_hash(),  # Reference to the parent commit
        "files": staged_files
    }
    commit_data_str = json.dumps(commit_data, indent=4)

    # Step 4: Calculate the hash for the commit object
    commit_hash = hashlib.sha1(commit_data_str.encode('utf-8')).hexdigest()

    # Step 5: Save the commit object to the object directory
    commit_path = f".myscs/objects/{commit_hash}"
    with open(commit_path, "w") as commit_file:
        commit_file.write(commit_data_str)
    logging.info(f"Commit object created with hash {commit_hash}")

    # Step 6: Update HEAD to point to the new commit
    with open(".myscs/HEAD", "w") as head_file:
        head_file.write(f"ref: refs/heads/main\n{commit_hash}")
    logging.info("HEAD updated to new commit.")

    # Step 7: Provide feedback
    print(f"Commit successful. Commit hash: {commit_hash}")
    logging.info("Commit completed successfully.")

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

if __name__ == "__main__":
    commit("Initial commit")
