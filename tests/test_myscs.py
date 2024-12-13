import unittest
import os
import shutil
import sys
print(sys.path)
from repoinit import initialize_repo




class TestInitializeRepo(unittest.TestCase):
    def setUp(self):
        """Prepare the test environment."""
        # Clean up any pre-existing .myscs directory
        if os.path.exists(".myscs"):
            shutil.rmtree(".myscs")

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(".myscs"):
            shutil.rmtree(".myscs")

    def test_initialize_new_repo(self):
        """Test initializing a new repository."""
        initialize_repo()
        # Check if the main directory and subdirectories are created
        self.assertTrue(os.path.exists(".myscs"))
        self.assertTrue(os.path.exists(".myscs/objects"))
        self.assertTrue(os.path.exists(".myscs/refs/heads"))
        # Check if essential files are created
        self.assertTrue(os.path.isfile(".myscs/HEAD"))
        self.assertTrue(os.path.isfile(".myscs/config"))

    def test_existing_repo(self):
        """Test behavior when repository already exists."""
        os.makedirs(".myscs")
        with self.assertLogs(level="WARNING") as log:
            initialize_repo()
            # Check that the log output matches the actual warning format
            self.assertIn("WARNING:root:Repository already exists in the current directory.", log.output)

    def test_logging(self):
        """Ensure logging works correctly."""
        log_file = "myscs.log"
        if os.path.exists(log_file):
            os.remove(log_file)  # Reset log file before test
        initialize_repo()
        # Check that log file was created and contains relevant info
        self.assertTrue(os.path.exists(log_file))
        with open(log_file, "r") as log:
            content = log.read()
            self.assertIn("Starting repository initialization.", content)
            self.assertIn("Repository initialization completed successfully.", content)

if __name__ == "__main__":
    unittest.main()
