import sys
from qdrant_client import QdrantClient
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer

def get_qdrant_client():
    return QdrantClient(host="localhost", port=6333)

def get_neo4j_driver():
    return GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "demodemo"))

def main():
    if len(sys.argv) != 2:
        print("Usage: python query_krag.py \"<your_query>\"")
        sys.exit(1)

    query = sys.argv[1]
    print(f"Querying for: '{query}'\n")

    # Initialize clients and model
    qdrant_client = get_qdrant_client()
    neo4j_driver = get_neo4j_driver()
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

    # 1. Semantic Search in Qdrant
    print("--- Qdrant (Semantic Search) Results ---")
    query_vector = embedding_model.encode(query).tolist()
    search_results = qdrant_client.search(
        collection_name="krag_papers",
        query_vector=query_vector,
        limit=2
    )
    if search_results:
        for result in search_results:
            print(f"  - Found in document: {result.payload.get('filename')}")
            print(f"    Score: {result.score:.4f}")
            print(f"    Text preview: {result.payload.get('text_preview')}...")
    else:
        print("No semantic results found in Qdrant.")

    # 2. Graph Search in Neo4j
    print("\n--- Neo4j (Graph Search) Results ---")
    with neo4j_driver.session() as session:
        # Find concepts related to the query
        cypher_query = """
        MATCH (c:Concept)
        WHERE toLower(c.name) CONTAINS toLower($query)
        RETURN c.name as concept
        """
        results = session.run(cypher_query, parameters={'query': query})
        concepts = [record["concept"] for record in results]
        
        if concepts:
            print(f"Found related concepts: {concepts}")
            # Find papers discussing these concepts
            for concept in concepts:
                cypher_query_papers = """
                MATCH (p:Paper)-[:DISCUSSES]->(c:Concept {name: $concept})
                RETURN p.name as paper_name
                """
                paper_results = session.run(cypher_query_papers, concept=concept)
                papers = [record["paper_name"] for record in paper_results]
                if papers:
                    print(f"  - Concept '{concept}' is discussed in: {papers}")
        else:
            print("No related concepts found in Neo4j.")

    neo4j_driver.close()

if __name__ == "__main__":
    main()
