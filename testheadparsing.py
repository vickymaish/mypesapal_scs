import os
import shutil
from commit_change import get_current_commit_hash

def test_get_current_commit_hash():
    head_path = ".myscs/HEAD"
    os.makedirs(".myscs", exist_ok=True)

    # Test cases with expected outcomes
    test_cases = [
        ("ref: refs/heads/main\nc00c474909b6bcbded43b1331f6f1ad6c8d7afb4", "c00c474909b6bcbded43b1331f6f1ad6c8d7afb4"),
        ("c00c474909b6bcbded43b1331f6f1ad6c8d7afb4", "c00c474909b6bcbded43b1331f6f1ad6c8d7afb4"),
        ("ref: refs/heads/main", None),
        ("Invalid Content", None),
        ("", None),  # Empty HEAD
    ]

    for i, (head_content, expected) in enumerate(test_cases, start=1):
        with open(head_path, "w") as head_file:
            head_file.write(head_content)
        
        result = get_current_commit_hash()
        print(f"Test Case {i}: {'PASSED' if result == expected else 'FAILED'}")
        print(f"  HEAD Content: {head_content}")
        print(f"  Expected: {expected}, Got: {result}")

    # Clean up: Remove files in .myscs before deleting the directory
    if os.path.exists(".myscs"):
        for root, dirs, files in os.walk(".myscs", topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(".myscs")  # Finally remove the empty directory

if __name__ == "__main__":
    test_get_current_commit_hash()
