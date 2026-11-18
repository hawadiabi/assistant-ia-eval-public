import json
from collections import Counter
from pathlib import Path

CHEMIN = Path("evals/dataset.jsonl")
CATEGORIES = {"conjugaison", "regle", "piege", "ambigu", "hors_corpus", "sans_rapport"}
CHAMPS = {
    "id", "usage", "categorie", "question",
    "reponse_attendue", "mots_cles", "source_attendue",
}

ids = set()
par_categorie = Counter()
par_usage = Counter()
erreurs = []

lignes = CHEMIN.read_text(encoding="utf-8").splitlines()
for numero, ligne in enumerate(lignes, 1):
    if not ligne.strip():
        continue
    try:
        cas = json.loads(ligne)
    except json.JSONDecodeError as e:
        erreurs.append(f"ligne {numero} : JSON invalide ({e})")
        continue
    manquants = CHAMPS - set(cas)
    if manquants:
        erreurs.append(f"ligne {numero} : champs manquants {sorted(manquants)}")
        continue
    if cas["id"] in ids:
        erreurs.append(f"ligne {numero} : id en double {cas['id']}")
    ids.add(cas["id"])
    if cas["categorie"] not in CATEGORIES:
        erreurs.append(f"ligne {numero} : catégorie inconnue {cas['categorie']}")
    if cas["usage"] not in {"dev", "test"}:
        erreurs.append(f"ligne {numero} : usage inconnu {cas['usage']}")
    for source in cas["source_attendue"]:
        if not (Path("corpus") / source).exists():
            erreurs.append(f"ligne {numero} : fiche introuvable {source}")
    refus = cas["reponse_attendue"] == "REFUS"
    if cas["categorie"] in {"hors_corpus", "sans_rapport"} and not refus:
        erreurs.append(f"ligne {numero} : cette catégorie doit avoir REFUS")
    if refus and (cas["mots_cles"] or cas["source_attendue"]):
        erreurs.append(f"ligne {numero} : un REFUS n'a ni mots clés ni source")
    if not refus and not cas["mots_cles"]:
        erreurs.append(f"ligne {numero} : mots clés manquants")
    par_categorie[cas["categorie"]] += 1
    par_usage[cas["usage"]] += 1

print(f"{len(ids)} cas lus")
print("Par catégorie :", dict(par_categorie))
print("Par usage :", dict(par_usage))
if erreurs:
    print(f"\n{len(erreurs)} problème(s) :")
    for e in erreurs:
        print(" -", e)
else:
    print("\nAucun problème détecté.")