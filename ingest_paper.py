import fitz  # PyMuPDF
import sys
import os
import json
import uuid
from qdrant_client import QdrantClient, models
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page_num in range(min(5, doc.page_count)): # Limita l'analisi alle prime 5 pagine
            text += doc[page_num].get_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        sys.exit(1)

def get_qdrant_client():
    return QdrantClient(host="localhost", port=6333)

def get_neo4j_driver():
    return GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "demodemo"))

def extract_entities_with_openai(text):
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at extracting structured information from academic papers. Extract the authors and key concepts from the following text. Return the result as a JSON object with two keys: 'authors' (a list of strings) and 'concepts' (a list of strings)."
                },
                {
                    "role": "user",
                    "content": text[:4000] # Limita il testo inviato a OpenAI per efficienza
                }
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return {"authors": [], "concepts": []}

def main():
    if len(sys.argv) != 2:
        print("Usage: python ingest_paper.py <path_to_pdf>")
        sys.exit(1)

    pdf_file = sys.argv[1]
    episode_name = pdf_file.split('/')[-1]

    print(f"Processing {episode_name}...")

    text_content = extract_text_from_pdf(pdf_file)
    print("Text extracted.")

    qdrant_client = get_qdrant_client()
    neo4j_driver = get_neo4j_driver()
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    print("Clients and model initialized.")

    entities = extract_entities_with_openai(text_content)
    print(f"Extracted entities: {entities}")

    collection_name = "krag_papers"
    qdrant_client.recreate_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
    )
    qdrant_client.upsert(
        collection_name=collection_name,
        points=[
            models.PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding_model.encode(text_content).tolist(),
                payload={"filename": episode_name, "text_preview": text_content[:500]}
            )
        ],
    )
    print("Ingested into Qdrant.")

    with neo4j_driver.session() as session:
        # Create Paper node
        session.run("MERGE (p:Paper {name: $name})", name=episode_name)
        
        # Create Author nodes and relationships
        for author_name in entities.get('authors', []):
            session.run("MERGE (a:Author {name: $name})", name=author_name)
            session.run(
                "MATCH (p:Paper {name: $paper_name}), (a:Author {name: $author_name}) "
                "MERGE (a)-[:AUTHORED_BY]->(p)",
                paper_name=episode_name, author_name=author_name
            )

        # Create Concept nodes and relationships
        for concept_name in entities.get('concepts', []):
            session.run("MERGE (c:Concept {name: $name})", name=concept_name)
            session.run(
                "MATCH (p:Paper {name: $paper_name}), (c:Concept {name: $concept_name}) "
                "MERGE (p)-[:DISCUSSES]->(c)",
                paper_name=episode_name, concept_name=concept_name
            )
    print("Ingested into Neo4j with entities and relationships.")

    neo4j_driver.close()
    print("All done!")

if __name__ == "__main__":
    main()