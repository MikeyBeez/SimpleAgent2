import json
from langchain_community.embeddings import OllamaEmbeddings
from tqdm import tqdm  # Make sure you have tqdm installed!

# 1. Load the extracted KB data from the JSON file
with open("extracted_kb.json", "r") as f:
    kb_entries = json.load(f)

# 2. Initialize the Ollama embedding model
embeddings = OllamaEmbeddings(model="mxbai-embed-large")  # Replace with your model

# 3. Generate embeddings for each text entry
print("Generating embeddings...")
for entry in tqdm(kb_entries):  # Wrap kb_entries with tqdm for the progress bar
    entry["embedding"] = embeddings.embed_query(entry["text"])

# 4. Save the updated data with embeddings to a new JSON file
with open("kb_with_embeddings.json", "w") as f:
    json.dump(kb_entries, f, indent=4)

print("Embeddings generated and saved to kb/kb_with_embeddings.json") 
