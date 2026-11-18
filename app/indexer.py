from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

CORPUS = Path("corpus")
DB_PATH = "chroma_db"

modele = SentenceTransformer("intfloat/multilingual-e5-small")

client = chromadb.PersistentClient(path=DB_PATH)
try:
    client.delete_collection("grammaire")
except Exception:
    pass  # la collection n'existait pas encore
collection = client.create_collection(
    "grammaire", metadata={"hnsw:space": "cosine"}
)


def decouper(texte):
    """Un morceau par paragraphe, avec le titre de la fiche en tête."""
    blocs = [b.strip() for b in texte.split("\n\n") if b.strip()]
    titre = blocs[0]
    return [titre + "\n" + b for b in blocs[1:]] or [texte]


ids, textes, metadonnees = [], [], []
for fichier in sorted(CORPUS.glob("*.md")):
    contenu = fichier.read_text(encoding="utf-8")
    for i, morceau in enumerate(decouper(contenu)):
        ids.append(f"{fichier.stem}-{i}")
        textes.append(morceau)
        metadonnees.append({"source": fichier.name})

embeddings = modele.encode(["passage: " + t for t in textes]).tolist()
collection.add(
    ids=ids, documents=textes, embeddings=embeddings, metadatas=metadonnees
)
nb_fiches = len({m["source"] for m in metadonnees})
print(f"{nb_fiches} fiches, {len(ids)} morceaux indexés.")