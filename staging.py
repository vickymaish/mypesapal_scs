# staging.py

import os
import logging
import hashlib

# Configure logging
logging.basicConfig(
    filename="myscs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def stage_file(file_path):
    """
    Stage a file by adding it to the .myscs/index file.
    """
    if not os.path.exists(file_path):
        print("File not found in the working directory.")
        logging.warning(f"File {file_path} not found.")
        return

    try:
        # Calculate the file hash
        hasher = hashlib.sha1()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        file_hash = hasher.hexdigest()

        # Add the file path and hash to the index
        index_path = ".myscs/index"
        with open(index_path, 'a') as index_file:
            index_file.write(f"{file_path} {file_hash}\n")

        print("File staged successfully.")
        logging.info(f"File {file_path} added to the index with hash {file_hash}.")

    except Exception as e:
        print(f"Error staging the file. Details: {str(e)}")
        logging.error(f"Error staging the file {file_path}: {str(e)}")
