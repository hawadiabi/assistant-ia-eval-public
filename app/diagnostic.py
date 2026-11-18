import chromadb
from sentence_transformers import SentenceTransformer

modele = SentenceTransformer("intfloat/multilingual-e5-small")
client = chromadb.PersistentClient(path="chroma_db")
col = client.get_collection("grammaire")

question = "subjonctif présent"
embedding = modele.encode(["query: " + question]).tolist()
res = col.query(query_embeddings=embedding, n_results=col.count())

for rang, (meta, dist, doc) in enumerate(
    zip(res["metadatas"][0], res["distances"][0], res["documents"][0]), 1
):
    if rang <= 5 or meta["source"] == "subjonctif-present.md":
        apercu = doc[:70].replace("\n", " / ")
        print(rang, meta["source"], round(dist, 2), "|", apercu)