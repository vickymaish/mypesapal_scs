import unittest
import os
from staging import stage_file  # Import the stage_file function from staging.py

class TestStageFile(unittest.TestCase):
    def setUp(self):
        """Set up test environment by creating test files of different types."""
        # Create a text file
        self.text_file_path = "text.txt"
        with open(self.text_file_path, "w") as f:
            f.write("Hello, this is a text file for testing.")

        # Create a JSON file
        self.json_file_path = "data.json"
        with open(self.json_file_path, "w") as f:
            f.write('{"key": "value"}')

        # Create a binary file with raw binary data
        self.binary_file_path = "binary.bin"
        with open(self.binary_file_path, "wb") as f:
            f.write(b"This is binary content for testing.")

        # Create a file that should be ignored based on the .myscsignore pattern
        self.ignored_file_path = "ignored_file.txt"
        with open(self.ignored_file_path, "w") as f:
            f.write("This file should be ignored by staging.")

        # Create a .myscsignore file
        with open(".myscsignore", "w") as f:
            f.write("*.txt\n")  # Ignore all .txt files

    def tearDown(self):
        """Clean up after tests by removing test files and the index file."""
        for file_path in [self.text_file_path, self.json_file_path, self.binary_file_path, self.ignored_file_path]:
            if os.path.exists(file_path):
                os.remove(file_path)
        if os.path.exists(".myscs/index"):
            os.remove(".myscs/index")
        if os.path.exists(".myscsignore"):
            os.remove(".myscsignore")

    def test_stage_text_file(self):
        """Test staging a text file."""
        stage_file(self.text_file_path)
        index_path = ".myscs/index"
        self.assertTrue(os.path.exists(index_path), "Index file was not created.")
        with open(index_path, "r") as index_file:
            content = index_file.read()
            self.assertIn(self.text_file_path, content, "Text file path not found in the index.")

    def test_stage_json_file(self):
        """Test staging a JSON file."""
        stage_file(self.json_file_path)
        index_path = ".myscs/index"
        with open(index_path, "r") as index_file:
            content = index_file.read()
            self.assertIn(self.json_file_path, content, "JSON file path not found in the index.")

    def test_stage_binary_file(self):
        """Test staging a binary file."""
        stage_file(self.binary_file_path)
        index_path = ".myscs/index"
        with open(index_path, "r") as index_file:
            content = index_file.read()
            self.assertIn(self.binary_file_path, content, "Binary file path not found in the index.")

    def test_stage_ignored_file(self):
        """Test if ignored file is skipped."""
        stage_file(self.ignored_file_path)
        index_path = ".myscs/index"
        with open(index_path, "r") as index_file:
            content = index_file.read()
            self.assertNotIn(self.ignored_file_path, content, "Ignored file should not be staged.")

    def test_stage_all_files(self):
        """Test staging all files using 'myscs add .'."""
        # Stage all files
        os.system("python myscs.py add .")  # Use the script to stage all non-ignored files

        index_path = ".myscs/index"
        self.assertTrue(os.path.exists(index_path), "Index file was not created.")

        with open(index_path, "r") as index_file:
            content = index_file.read()
            # Ensure that non-ignored files are staged
            self.assertIn(self.text_file_path, content, "Text file path not found in the index.")
            self.assertIn(self.json_file_path, content, "JSON file path not found in the index.")
            self.assertIn(self.binary_file_path, content, "Binary file path not found in the index.")
            # Ensure that ignored files are not staged
            self.assertNotIn(self.ignored_file_path, content, "Ignored file should not be staged.")

if __name__ == "__main__":
    unittest.main()
