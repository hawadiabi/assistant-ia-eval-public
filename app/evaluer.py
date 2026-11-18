import argparse
import hashlib
import json
import re
import time
import unicodedata
from collections import defaultdict
from pathlib import Path

from assistant import MODELE_LLM, PROMPT_SYSTEME, repondre

DATASET = Path("evals/dataset.jsonl")
PHRASE_REFUS = "je ne trouve pas cette information"
VERSION_PROMPT = hashlib.sha1(PROMPT_SYSTEME.encode("utf-8")).hexdigest()[:8]


def normaliser(texte):
    texte = unicodedata.normalize("NFC", texte).lower()
    texte = texte.replace("\u2019", "'").replace("`", "'")
    return re.sub(r"\s+", " ", texte)


def charger(chemin):
    lignes = chemin.read_text(encoding="utf-8").splitlines()
    return [json.loads(ligne) for ligne in lignes if ligne.strip()]


def evaluer_cas(cas):
    debut = time.time()
    try:
        reponse, sources = repondre(cas["question"])
        erreur = None
    except Exception as e:
        reponse, sources, erreur = "", [], str(e)
    duree = time.time() - debut

    texte = normaliser(reponse)
    refus = PHRASE_REFUS in texte
    citees = re.findall(r"\[([^\]]+\.md)\]", reponse)
    attendues = cas["source_attendue"]

    resultat = {
        "id": cas["id"],
        "usage": cas["usage"],
        "categorie": cas["categorie"],
        "question": cas["question"],
        "reponse": reponse,
        "sources_recuperees": sources,
        "sources_citees": citees,
        "refus_detecte": refus,
        "duree_s": round(duree, 1),
        "modele": MODELE_LLM,
        "version_prompt": VERSION_PROMPT,
        "erreur": erreur,
        "mots_manquants": None,
        "exact": None,
        "source_recuperee": None,
        "source_citee": None,
        "refus_correct": None,
        "faux_refus": None,
    }
    if cas["reponse_attendue"] == "REFUS":
        resultat["refus_correct"] = refus
    else:
        manquants = [m for m in cas["mots_cles"] if normaliser(m) not in texte]
        resultat["mots_manquants"] = manquants
        resultat["exact"] = (not refus) and (not manquants) and erreur is None
        resultat["faux_refus"] = refus
        resultat["source_recuperee"] = any(s in sources for s in attendues)
        resultat["source_citee"] = any(s in citees for s in attendues)
    return resultat


def pct(valeurs):
    valeurs = [v for v in valeurs if v is not None]
    if not valeurs:
        return "sans objet"
    return f"{100 * sum(valeurs) / len(valeurs):.0f} % ({sum(valeurs)}/{len(valeurs)})"


def afficher_resume(resultats, titre, cle):
    groupes = defaultdict(list)
    for r in resultats:
        groupes[cle(r)].append(r)
    print(f"\n== {titre} ==")
    for nom in sorted(groupes):
        g = groupes[nom]
        duree = sum(r["duree_s"] for r in g) / len(g)
        print(f"\n{nom} ({len(g)} cas, durée moyenne {duree:.0f} s)")
        print("  exactitude       :", pct([r["exact"] for r in g]))
        print("  source récupérée :", pct([r["source_recuperee"] for r in g]))
        print("  source citée     :", pct([r["source_citee"] for r in g]))
        print("  refus correct    :", pct([r["refus_correct"] for r in g]))
        print("  faux refus       :", pct([r["faux_refus"] for r in g]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--usage", choices=["dev", "test"])
    parser.add_argument("--limite", type=int)
    parser.add_argument("--sortie")
    parser.add_argument("--resume-seulement", action="store_true")
    args = parser.parse_args()

    sortie = (
        Path(args.sortie)
        if args.sortie
        else Path(f"evals/resultats_assistant_{args.usage or 'tous'}.jsonl")
    )
    deja = {}
    if sortie.exists():
        deja = {r["id"]: r for r in charger(sortie)}

    if not args.resume_seulement:
        cas_liste = charger(DATASET)
        if args.usage:
            cas_liste = [c for c in cas_liste if c["usage"] == args.usage]
        a_faire = [c for c in cas_liste if c["id"] not in deja]
        if args.limite:
            a_faire = a_faire[: args.limite]
        print(f"{len(a_faire)} cas à lancer ({len(deja)} déjà faits)")
        for i, cas in enumerate(a_faire, 1):
            print(f"[{i}/{len(a_faire)}] {cas['id']} {cas['question']}", flush=True)
            resultat = evaluer_cas(cas)
            with open(sortie, "a", encoding="utf-8") as f:
                f.write(json.dumps(resultat, ensure_ascii=False) + "\n")
            deja[resultat["id"]] = resultat
            print(
                f"    {resultat['duree_s']:.0f} s | refus : "
                f"{resultat['refus_detecte']} | exact : {resultat['exact']}",
                flush=True,
            )

    resultats = list(deja.values())
    if not resultats:
        print("Aucun résultat à résumer.")
        return
    versions = {r["version_prompt"] for r in resultats}
    if len(versions) > 1:
        print("Attention : plusieurs versions du prompt dans ce fichier :", versions)
    erreurs = [r["id"] for r in resultats if r["erreur"]]
    if erreurs:
        print("Attention : cas avec erreur :", erreurs)
    afficher_resume(resultats, "Tous les cas", lambda r: "tous")
    afficher_resume(resultats, "Par catégorie", lambda r: r["categorie"])

if __name__ == "__main__":
    main()