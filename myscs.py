#!/usr/bin/env python3

import sys
from main import main  # Import the main function from main.py

if __name__ == "__main__":
    # Pass command-line arguments to the main function
    sys.argv[0] = "myscs"  # Ensure the script name is set to "myscs"
    main()
