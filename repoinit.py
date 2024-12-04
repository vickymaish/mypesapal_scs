"""PSEUDO-CODE 

FUNCTION initialize_repo():
    # Step 1: Check if repository already exists
    if directory .myscs EXISTS:
    print("There is already a repository in this directory.")
    return
    # Step 2: Create main repository directory
    try:
    CREATE_DIR "myscs"
    #step 3 create subdirectories associated with myscs directory
    CREATE DIRECTORIES "myscs/Objects"
    CREATE DIRECTORIES "myscs/refs/heads"

    # Step 4: Create essential files
    # Create the HEAD file
    CREATE file ".myscs/HEAD" with content "ref: refs/head/main"
    CREATE file ".myscs/Config" with content 
    {
    "repository": "myscs",
    "version": "1.0"
    }
    #step 5 : Create feedback/ print message to user on state of repo
    print("Initialized empty repository in the current directory.")

    CATCH except as e:
    #handle errors
    Print ("error: unable to initialize repository. details : {str(e)})"
    END FUNCTION


"""

import os
import json
import logging
import hashlib 

# Configure logging
logging.basicConfig(
    filename="myscs.log",
    level=logging.INFO,  # Log level (INFO, DEBUG, ERROR)
    format="%(asctime)s - %(levelname)s - %(message)s"
)

"""  #Pseudo code for initialize index fn
FUNCTION initialize_index():
    # Step 1: Check if the .myscs/index file already exists
    IF .myscs/index does not exist:
        # Step 2: Create the .myscs/index file
        CREATE an empty .myscs/index file
        LOG "Index file created successfully."
        PRINT "Index file created for staging."
    ELSE:
        PRINT "Index file already exists."
"""

def initialize_index():
    """
    The .myscs/index file serves as the staging area
    in your custom version control system. 
    It will store the paths and content hashes 
    of files that have been staged, allowing you to track
    what changes are ready for the next commit.
    Initialize the .myscs/index file if it does not exist.
    """
    index_path = ".myscs/index"
    
    if not os.path.exists(index_path):
        try:
            # Create the index file
            with open(index_path, 'w') as index_file:
                pass  # Create an empty file
            logging.info("Index file created successfully.")
            print("Index file created for staging.")
        except Exception as e:
            logging.error(f"Error creating index file: {str(e)}")
            print(f"Error creating index file. Details: {str(e)}")
    else:
        print("Index file already exists.")



def initialize_repo():
    """
    Initialize a new repository in the current directory.
    """
    logging.info("Starting repository initialization.")
    # Step 1: Check if repository already exists
    if os.path.exists(".myscs"):
        logging.warning("Repository already exists in the current directory.")
        print("There is already a repository in this directory.")
        logging.shutdown()  # Ensure the log file is closed properly
        return

    try:
        # Step 2: Create the main repository directory
        os.makedirs(".myscs")
        logging.info("Created main repository directory: .myscs")

        # Step 3: Create subdirectories
        os.makedirs(".myscs/objects")
        os.makedirs(".myscs/refs/heads")
        logging.info("Created subdirectories: objects, refs/heads")

        # Step 4: Create essential files
        with open(".myscs/HEAD", "w") as head_file:
            head_file.write("ref: refs/heads/main\n")
        logging.info("HEAD file created and initialized.")

        config_data = {
            "repository": "myscs",
            "version": "1.0"
        }

        with open(".myscs/config", "w") as config_file:
            json.dump(config_data, config_file, indent=4)
        logging.info("Config file created with default settings.")

        # Initialize the index file
        initialize_index()

        # Step 5: Provide user feedback
        print("Initialized empty repository in the current directory.")
        logging.info("Repository initialization completed successfully.")
        logging.shutdown()  # Ensure the log file is closed properly

    except Exception as e:
        logging.error(f"Error during repository initialization: {str(e)}")
        print(f"Error: Unable to initialize repository. Details: {str(e)}")
        logging.shutdown()  # Ensure the log file is closed properly
if __name__ == "__main__":
    initialize_repo()


# # GIT ADD PSEUDO CODE for staging files 
# """
# FUNCTION stage_file(file_path):
#     # Step 1: Check if the file exists in the working directory
#     IF file_path does not exist:
#         PRINT "File not found in the working directory."
#         RETURN

#     # Step 2: Check if the file is ignored (optional, depending on implementation)
#     IF file_path is in .gitignore:
#         PRINT "File is ignored and will not be staged."
#         RETURN

#     # Step 3: Calculate the hash of the file content
#     TRY:
#         OPEN file at file_path in read mode
#         CALCULATE hash of the file content using hashlib
#         CLOSE the file
#         LOG "File hash calculated successfully."

#         # Step 4: Add the file path and its hash to the staging area (index)
#         OPEN .myscs/index in write mode or append mode
#         WRITE the file path and hash to the index
#         CLOSE the file
#         PRINT "File staged successfully."
#         LOG "File added to the index."

#     EXCEPT Exception as e:
#         PRINT "Error staging the file. Details: {str(e)}"
#         LOG "Error staging the file: {str(e)}"
# END FUNCTION



# """
