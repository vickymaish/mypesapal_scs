import unittest
import os
from staging import stage_file  # Import the stage_file function from repoinit.py

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

        # Create an image file (use an existing one for simplicity)
        # Assuming `gitimagetest.png` is a sample image you have in your working directory
        # You can use `os.system()` or a separate script to copy a sample image for this test.

        # Create a binary file with raw binary data
        self.binary_file_path = "binary.bin"
        with open(self.binary_file_path, "wb") as f:
            f.write(b"This is binary content for testing.")

    def tearDown(self):
        """Clean up after tests by removing test files and the index file."""
        for file_path in [self.text_file_path, self.json_file_path, self.binary_file_path, "gitimagetest.png"]:
            if os.path.exists(file_path):
                os.remove(file_path)
        if os.path.exists(".myscs/index"):
            os.remove(".myscs/index")

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

    def test_stage_image_file(self):
        """Test staging an image file."""
        # Ensure that the image file exists before testing
        if os.path.exists("gitimagetest.png"):
            stage_file("gitimagetest.png")
            index_path = ".myscs/index"
            with open(index_path, "r") as index_file:
                content = index_file.read()
                self.assertIn("gitimagetest.png", content, "Image file path not found in the index.")
        else:
            self.skipTest("Image file 'gitimagetest.png' not found, skipping test.")

    def test_stage_binary_file(self):
        """Test staging a binary file."""
        stage_file(self.binary_file_path)
        index_path = ".myscs/index"
        with open(index_path, "r") as index_file:
            content = index_file.read()
            self.assertIn(self.binary_file_path, content, "Binary file path not found in the index.")

if __name__ == "__main__":
    unittest.main()
