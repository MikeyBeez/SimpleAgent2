import rdflib
import json

# 1. Load the N-Triples file into the graph
graph = rdflib.Graph()
graph.parse("kb/short-abstracts_lang=en.nt", format="nt")

# 2. Extract relevant text (e.g., labels)
kb_entries = []
for subject, predicate, object in graph:
    if predicate == rdflib.URIRef("http://www.w3.org/2000/01/rdf-schema#label"): 
        kb_entries.append({
            "text": str(object), 
            "uri": str(subject)
        })

# 3. Save the extracted entries to a JSON file
with open("kb/extracted_kb.json", "w") as f:
    json.dump(kb_entries, f, indent=4)  # Save with pretty-printing

print("Extracted KB entries saved to kb/extracted_kb.json") 
