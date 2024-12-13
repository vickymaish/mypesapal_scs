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



