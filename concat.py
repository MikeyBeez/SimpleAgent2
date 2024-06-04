import os

# Set the root directory
root_dir = "."

# Set the excluded directories and files
excluded_dirs = ["my_kb", "oldfiles", "__pycache__", ".git"]
excluded_files = ["LICENSE", "README.md", "chatlogic.txt", "output.txt", "promptsold33.py"]

# Initialize a list to store the file contents
file_contents = []

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
                # Add the filename as a header
                file_contents.append(f"# {filename}\n")
                # Append the file contents
                file_contents.append(file.read())
                file_contents.append("\n\n")  # Add two newlines for separation
        except UnicodeDecodeError:
            # Skip files that cannot be decoded as UTF-8
            continue

# Write the concatenated contents to the output.txt file
with open("output.txt", "w", encoding="utf-8") as output_file:
    output_file.write("\n\n".join(file_contents))

print("File concatenation completed successfully!")
