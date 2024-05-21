from rdflib import Graph

# Load the TTL file into an RDF graph
graph = Graph()
graph.parse("short-abstracts_lang=en.ttl", format="turtle")

# Serialize the graph to N-Triples format
graph.serialize(destination="short-abstracts_lang=en.nt", format="nt", encoding='utf-8')

print("Conversion complete! File saved as short-abstracts_lang=en.nt") 
