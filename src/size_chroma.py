import os

chroma_directory = "my_context"
total_size = sum(os.path.getsize(os.path.join(chroma_directory, f)) for f in os.listdir(chroma_directory) if os.path.isfile(os.path.join(chroma_directory, f)))

print(f"Size of the Chroma database: {total_size} bytes")
