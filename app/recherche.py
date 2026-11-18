import sys

import chromadb
from sentence_transformers import SentenceTransformer

DB_PATH = "chroma_db"

modele = SentenceTransformer("intfloat/multilingual-e5-small")
client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_collection("grammaire")


def chercher(question, n=3):
    embedding = modele.encode(["query: " + question]).tolist()
    resultats = collection.query(query_embeddings=embedding, n_results=15)
    vues = {}
    for meta, distance in zip(resultats["metadatas"][0], resultats["distances"][0]):
        if meta["source"] not in vues:  # meilleur morceau par fiche
            vues[meta["source"]] = distance
    return list(vues.items())[:n]


if __name__ == "__main__":
    question = " ".join(sys.argv[1:])
    for source, distance in chercher(question):
        print(f"{source}  (distance : {distance:.2f})")