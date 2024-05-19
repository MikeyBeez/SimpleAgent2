import rdflib

# 1. Create an empty RDF graph
graph = rdflib.Graph()

# 2. Parse the N-Triples file into the graph 
graph.parse("kb/short-abstracts_lang=en.nt", format="nt") 

print("N-Triples data loaded into RDF graph!")
