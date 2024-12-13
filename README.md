# Documentation of Source Control System (SCS)

## Purpose of the Documentation
This documentation outlines the design, implementation, and the key features of the distributed source control system (SCS). It aims to provide users with a clear understanding of how to set up and use the system, as well as the underlying architecture that makes it functional. The purpose of this project was to replicate core features of version control systems, such as Git, and implement them using a custom-built system.

## Table of Contents
1. [User Guide](#user-guide)
2. [Features of the Source Control System](#features-of-the-source-control-system)
3. [Data Structures and Algorithms Used](#data-structures-and-algorithms-used)
4. [Use of SHA-1 Hashing](#use-of-sha-1-hashing)
5. [Traversing through Commit Hashes](#traversing-through-commit-hashes)
6. [User Interface with Rich](#user-interface-with-rich)
7. [Setup and Installation Guide](#setup-and-installation-guide)
8. [Purpose and Functionality of the .bat File](#purpose-and-functionality-of-the-bat-file)
   

---

## User Guide
This section explains how to use the custom-built source control system.

1. **Initialize a Repository**
    - Use the `myscs init` command to initialize a new repository.
    - The repository is stored in a hidden `.myscs` directory.

2. **Stage Files (`git add`)**
    - Stage files using `myscs add <file_path>`.

3. **Commit Changes (`git commit`)**
    - Commit staged files using `myscs commit "<commit_message>"`.

4. **View Commit History (`git log`)**
    - Use `myscs log` to view the commit history.

5. **Create and Switch Branches**
    - Create new branches with `myscs branch <branch_name>`.
    - Switch between branches with `myscs switch <branch_name>`.

6. **Merge Branches**
    - Merge branches with `myscs merge <branch_name>`.

7. **Clone a Repository**
    - Use `myscs clone` to clone a repository to a different directory.

---

## Features of the Source Control System
The source control system replicates key functionalities of Git:
1. **Initializing a Repository**: Creates a hidden directory `.myscs` and stores essential files.
2. **Staging Files**: Tracks files with their hashes before committing.
3. **Committing Changes**: Records staged files and their changes, associating them with a unique commit hash.
4. **Viewing Commit History**: The user can see a chronological list of commits.
5. **Branching and Merging**: Supports multiple branches and merging functionality.
6. **Conflict Detection**: Alerts users if branches have diverged or contain conflicting changes.
7. **Cloning**: Gives users the ability to clone a repo on the local machine and create a destination folder with copied items.
8. **Ignoring files**: Allows users to select the files the do not want to get staged when the myscs add/ add . is entered.

---

## Data Structures and Algorithms Used

### Data Structures:
- **Hash Tables**: Used to store file hashes and staged files.
- **Linked List**: The commit history is modeled using a linked list structure.
- **Trees**: The repository’s branch system is modeled using trees.

### Algorithms:
- **SHA-1 Hashing**: Used to generate unique identifiers (hashes) for files and commits.
- **BFS**: Used for traversing the commit history.
- **Merge Algorithm**: A simple merge algorithm checks for conflicting changes but does not resolve them automatically.

---

## Use of SHA-1 Hashing

SHA-1 hashing is integral to the source control system. It is used to generate unique hashes for files and commits. SHA-1 ensures that any change in the content of a file or commit will generate a new hash, making it easy to track the evolution of the repository.

---

## Traversing through Commit Hashes

The commit history is represented as a chain of commit objects, where each commit object stores:
- **Commit Hash**: A unique identifier for the commit.
- **Parent Commit Hash**: Links to the previous commit, forming a chain.

---

## User Interface with Rich

The `rich` Python library is used to create visually appealing command-line output. Key features include:
- **Styled Text**: Commit history and error messages are displayed in colored text.
- **Tables**: Commit logs are displayed in organized tables with styled columns.
- **Interactive**: The UI allows users to interact with the system and receive real-time feedback.

---

## Setup and Installation Guide

To get started:
1. Clone the repository:
   ```bash
   git clone <repository_url>

2. Install dependencies:
Make sure to use a virtual environment:
```bash
python -m venv venv

Activate the environment:
```bash
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate  # Windows (I used windows)

3. Install required dependencies:
```bash
pip install -r requirements.txt

. To run the system, use the following command:
```bash
python myscs.py

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


##  Feature 2: Staging Files (`git add`)

### Overview:
This feature allows users to stage files before committing them, just like the `git add` command in Git. The staged files are tracked in the `.myscs/index` file, which keeps a record of the file paths and their corresponding hashes. This step is essential for preparing files for a commit.

### Key Operations:
- **Stage Files**: Users can add files to the staging area using the `myscs add <file_path>` command. The file path and its hash are recorded in the `.myscs/index` file.
- **Check for Duplicates**: If a file is already staged, it won’t be staged again, preventing redundancy.
- **Ignore Files**: Files matching patterns in the `.myscsignore` file are ignored during staging. This prevents temporary files, logs, or build artifacts from being added to the repository.

### How It Works:
1. **Calculate Hash**: The system computes the SHA-1 hash of each file to ensure its integrity and uniqueness.
2. **Staging**: Once the file is staged, its path and hash are written into the `.myscs/index` file. This file acts as a record of staged changes.
3. **Skipping Already Staged Files**: If a file has already been staged (based on its path and hash), the system skips staging it again and provides a message to inform the user.

## Feature 3: Committing Changes (`git commit`)

### Overview:
This feature allows users to commit staged changes to the repository. The commit operation records the current state of the staged files, including the commit message, author, and timestamp, into the repository’s history. Each commit creates a unique commit object and is linked to the previous commit, forming a chain of commits that represent the history of changes.

### Key Operations:
- **Commit Changes**: Users can commit changes by providing a commit message using the `myscs commit "<commit_message>"` command.
- **Commit Object**: Each commit is stored as a commit object, which contains details such as the commit message, timestamp, parent commit hash, author, and the files that were staged.
- **Update HEAD**: After each commit, the HEAD file is updated to reference the new commit hash, pointing to the latest commit in the current branch.

### How It Works:
1. **Create Commit Object**: The system creates a new commit object that contains the commit message, timestamp, author, and list of staged files.
2. **Save Commit**: The commit object is saved in the `.myscs/objects` directory with a unique commit hash (calculated using SHA-1).
3. **Update HEAD**: The HEAD file is updated to reference the new commit, linking it to the current branch.
4. **Link to Parent Commit**: Each commit references its parent commit (the previous commit), creating a chain of commits that represents the repository history.

---

## Feature 4: Viewing Commit History

### Overview:
This feature allows users to view the commit history of the repository, similar to the `git log` command in Git. The commit history shows a list of all commits made, along with their commit hashes, messages, timestamps, and authors.

### Key Operations:
- **View History**: Users can view the commit history using the `myscs log` command. This command fetches the commit objects starting from the latest commit (referenced by HEAD) and traverses back through the commit chain.
- **Display Commit Details**: For each commit, the following details are shown: commit hash, commit message, timestamp, and author.
- **Traverse Parent Commits**: The system continues to display commits until it reaches the first commit (where the parent commit is `None`).

### How It Works:
1. **Read HEAD**: The system reads the HEAD file to get the latest commit hash.
2. **Traverse Commit History**: Starting from the latest commit, the system fetches and displays the commit object. It then moves to the parent commit and continues until there are no more parent commits.
3. **Display Information**: For each commit, the system displays the commit hash, commit message, timestamp (formatted), and author in a table-like format.

---

## Feature 5: Creating Branches

### Overview:
This feature allows users to create branches in the repository. A branch represents an independent line of development that allows users to work on changes without affecting the main branch. Each branch points to a commit hash and has its own commit history.

### Key Operations:
- **Create Branch**: Users can create a new branch using the `myscs branch <branch_name>` command.
- **Switch Branches**: After creating a branch, users can switch to it using the `myscs switch <branch_name>` command, which updates the HEAD file to reference the new branch.
- **Track Commits**: Each branch has its own set of commits, and changes made in one branch will not affect other branches until they are merged.

### How It Works:
1. **Create New Branch**: The system creates a new file in `.myscs/refs/heads/` to represent the branch, which stores the commit hash that the branch currently points to.
2. **Switch to Branch**: When switching to a branch, the HEAD file is updated to reference the branch’s commit hash, making it the current branch.
3. **Branch-Specific History**: Each branch tracks its own commits and changes independently from other branches.

---

## Feature 6: Merging Branches

### Overview:
This feature allows users to merge changes from one branch into another. Merging combines the commits from two branches into a single branch. If the branches have diverged, a three-way merge is performed, and conflicting changes are detected.

### Key Operations:
- **Merge Branches**: Users can merge one branch into another using the `myscs merge <target_branch>` command.
- **Conflict Detection**: The system checks if there are conflicting changes between the two branches. If conflicts are found, it alerts the user but does not resolve the conflicts.
- **Commit Merge**: After merging, the system creates a new commit that records the merged changes.

### How It Works:
1. **Identify Divergence**: The system checks if the two branches have diverged by comparing their commit histories.
2. **Perform Merge**: The system merges the changes, creating a new commit that combines the changes from both branches.
3. **Handle Conflicts**: If conflicting changes are detected, the system alerts the user but does not resolve them automatically.

---

## Feature 7: Diffs Between Commits

### Overview:
This feature allows users to view the differences (diffs) between two commits. It helps users understand what changes have been made between versions of the repository.

### Key Operations:
- **View Diffs**: Users can view the differences between two commits using the `myscs diff <commit_hash1> <commit_hash2>` command.
- **Compare Files**: The system compares the file contents between the two commits and shows the differences.
- **Display Changes**: The changes are displayed in a human-readable format, highlighting added, modified, or deleted lines.

### How It Works:
1. **Fetch Commit Data**: The system fetches the commit objects for the two specified commits.
2. **Compare File Changes**: It compares the contents of the files in both commits and generates a diff.
3. **Display Diffs**: The system displays the differences between the files, showing added or removed lines.

---

## Feature 8: Cloning the Repository

### Overview:
This feature allows users to clone the repository onto their local machine. Cloning creates a copy of the repository, including its history and files, allowing users to work with it independently.

### Key Operations:
- **Clone Repository**: Users can clone the repository using the `myscs clone` command, which copies the repository’s `.myscs` directory and files to a new location.
- **Complete Copy**: The clone includes all the commit history, branches, and staged files.

### How It Works:
1. **Copy Repository Data**: The system copies the `.myscs` directory and all its contents to the new location.
2. **Maintain Commit History**: The cloned repository retains all commit history, branches, and the current state of the working directory.
3. **Ready for Use**: The cloned repository is now ready for use, with all the functionality available to the user as in the original repository.

---

## Feature 9: Ignoring Files (`.myscsignore`)

### Overview:
This feature allows users to specify files that should be ignored by the version control system. The `.myscsignore` file holds patterns for files that should not be staged, committed, or tracked.

### Key Operations:
- **Ignore Files**: Users can define patterns in the `.myscsignore` file to specify which files should be ignored.
- **Prevent Staging**: Files matching the patterns are skipped during staging, preventing them from being added to the repository.

### How It Works:
1. **Read `.myscsignore`**: The system reads the `.myscsignore` file to get the patterns for files to ignore.
2. **Skip Ignored Files**: When staging or committing, the system checks if a file matches any of the ignore patterns. If it does, it is skipped.


