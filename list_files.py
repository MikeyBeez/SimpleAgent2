import os

# Set the root directory
root_dir = "."

# Set the excluded directories and files
excluded_dirs = ["my_kb", "oldfiles", "__pycache__", ".git"]
excluded_files = ["LICENSE", "README.md", "chatlogic.txt", "output.txt", "promptsold33.py"]

# Initialize a list to store the files to be included
files_to_include = []

# Traverse the directory tree
for root, dirs, files in os.walk(root_dir):
    # Remove excluded directories from the list
    dirs[:] = [d for d in dirs if d not in excluded_dirs]

    for filename in files:
        # Skip excluded files
        if filename in excluded_files:
            continue

        file_path = os.path.join(root, filename)
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                # The file is readable, so include it
                files_to_include.append(file_path)
        except UnicodeDecodeError:
            # Skip files that cannot be decoded as UTF-8
            continue

# Print the list of files to be included
print("Files to be included:")
for file_path in files_to_include:
    print(file_path)
