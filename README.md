# Feature 1: Initializing a Repository

## Overview:
The system allows users to initialize a repository in a directory. This is the foundational step in creating a distributed source control system, similar to `git init` in Git. The repository is stored in a dot-prefixed subdirectory (i.e., `.myscs`), where all the essential information related to version control is stored.

## Key Operations:
- **Initialize Repository**: Users can initialize a repository in any directory using the `myscs init` command. This command sets up a `.myscs` directory within the current directory.
- **Repository Structure**:
  - `.myscs`: The main directory that holds the version control data.
  - `.myscs/objects`: Stores the commit objects (which hold the changes made to files).
  - `.myscs/refs/heads`: Contains references to different branches.
  - `.myscs/index`: This file keeps track of staged files ready for commit.

## How It Works:
When a user runs `myscs init`, the system checks if the `.myscs` directory exists. If it doesn't, the system creates it along with the necessary subdirectories. The initialization also creates an empty index file and a `HEAD` file that references the default branch (`main`), marking the start of the repository.

### Code Example:

```python
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
