#myscs pseudocode
Function intialize_repo(git init):
if subdirectory .myscs exists
    print("There is a repository named myscs"):
else:
    try : Create a subdirectory called .myscs 
    print('you have initialized a new repository')
    except Exception as e: print(f"Error creating repository: {str(e)}")
