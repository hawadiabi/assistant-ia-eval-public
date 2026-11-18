import argparse
import hashlib
import json
import time
from collections import Counter, defaultdict
from pathlib import Path

import ollama

CORPUS = Path("corpus")
DATASET = Path("evals/dataset.jsonl")
RUBRIQUE = Path("evals/rubric.md")
MODELE_JUGE = "qwen2.5:7b"
OPTIONS_JUGE = {"temperature": 0, "num_predict": 300}
VERDICTS = {
    "correct", "partiel", "incorrect",
    "faux_refus", "refus_correct", "reponse_hors_corpus",
}

PROMPT_SYSTEME = (
    "Tu es un évaluateur rigoureux de réponses en grammaire française. "
    "Tu appliques la grille fournie sans indulgence. "
    "Tu réponds uniquement par un objet JSON."
)


def charger(chemin):
    lignes = chemin.read_text(encoding="utf-8").splitlines()
    return [json.loads(ligne) for ligne in lignes if ligne.strip()]


def construire_message(cas, res, rubrique):
    fiches = []
    for source in res["sources_recuperees"]:
        chemin = CORPUS / source
        if chemin.exists():
            fiches.append(f"[{source}]\n{chemin.read_text(encoding='utf-8')}")
    contexte = "\n\n---\n\n".join(fiches) or "(aucune fiche)"
    if cas["reponse_attendue"] == "REFUS":
        attendu = "Un refus : l'information n'est pas dans les fiches."
    else:
        attendu = cas["reponse_attendue"]
    return (
        f"Grille d'évaluation :\n{rubrique}\n\n"
        f"Fiches fournies à l'assistant :\n{contexte}\n\n"
        f"Question : {cas['question']}\n"
        f"Réponse attendue : {attendu}\n"
        f"Réponse de l'assistant :\n{res['reponse']}\n\n"
        "Évalue la réponse de l'assistant selon la grille. Réponds uniquement "
        "en JSON avec les clés : verdict, exactitude, fidelite, completude, "
        "justification."
    )


def juger(cas, res, rubrique, version_grille):
    debut = time.time()
    message = construire_message(cas, res, rubrique)
    brut = ""
    try:
        reponse = ollama.chat(
            model=MODELE_JUGE,
            messages=[
                {"role": "system", "content": PROMPT_SYSTEME},
                {"role": "user", "content": message},
            ],
            format="json",
            options=OPTIONS_JUGE,
        )
        brut = reponse["message"]["content"]
        donnees = json.loads(brut)
        verdict = str(donnees.get("verdict", "")).strip().lower()
        if verdict not in VERDICTS:
            raise ValueError(f"verdict inconnu : {verdict}")
        notes = {k: int(donnees[k]) for k in ("exactitude", "fidelite", "completude")}
        justification = str(donnees.get("justification", ""))
        erreur = None
    except Exception as e:
        verdict, notes, justification, erreur = "erreur_juge", {}, "", str(e)

    return {
        "id": res["id"],
        "categorie": res["categorie"],
        "verdict": verdict,
        "exactitude": notes.get("exactitude"),
        "fidelite": notes.get("fidelite"),
        "completude": notes.get("completude"),
        "justification": justification,
        "exact_mots_cles": res["exact"],
        "refus_correct_mots_cles": res["refus_correct"],
        "modele_juge": MODELE_JUGE,
        "version_grille": version_grille,
        "duree_s": round(time.time() - debut, 1),
        "erreur": erreur,
        "brut": brut if erreur else None,
    }


def accord_mots_cles(j):
    """Le juge et les mots clés donnent-ils le même verdict ?"""
    if j["exact_mots_cles"] is not None:
        return j["exact_mots_cles"] == (j["verdict"] == "correct")
    if j["refus_correct_mots_cles"] is not None:
        return j["refus_correct_mots_cles"] == (j["verdict"] == "refus_correct")
    return None


def resumer(jugements):
    print(f"\n== {len(jugements)} cas jugés ==")
    print("Verdicts :", dict(Counter(j["verdict"] for j in jugements)))

    avec_notes = [j for j in jugements if j["exactitude"] is not None]
    if avec_notes:
        for cle in ("exactitude", "fidelite", "completude"):
            moyenne = sum(j[cle] for j in avec_notes) / len(avec_notes)
            print(f"Moyenne {cle} : {moyenne:.1f} / 5")

    par_cat = defaultdict(Counter)
    for j in jugements:
        par_cat[j["categorie"]][j["verdict"]] += 1
    print("\nPar catégorie :")
    for cat in sorted(par_cat):
        print(f"  {cat} : {dict(par_cat[cat])}")

    comparables = [j for j in jugements if accord_mots_cles(j) is not None]
    desaccords = [j["id"] for j in comparables if not accord_mots_cles(j)]
    if comparables:
        accords = len(comparables) - len(desaccords)
        print(f"\nAccord juge et mots clés : {accords}/{len(comparables)}")
        print("Désaccords :", desaccords)
    erreurs = [j["id"] for j in jugements if j["verdict"] == "erreur_juge"]
    if erreurs:
        print("Erreurs du juge :", erreurs)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--resultats", required=True)
    parser.add_argument("--sortie")
    parser.add_argument("--resume-seulement", action="store_true")
    args = parser.parse_args()

    chemin_resultats = Path(args.resultats)
    sortie = Path(args.sortie or str(chemin_resultats).replace("resultats_", "juge_"))
    rubrique = RUBRIQUE.read_text(encoding="utf-8")
    version_grille = hashlib.sha1(rubrique.encode("utf-8")).hexdigest()[:8]

    cas_par_id = {c["id"]: c for c in charger(DATASET)}
    deja = {j["id"]: j for j in charger(sortie)} if sortie.exists() else {}

    if not args.resume_seulement:
        a_faire = [r for r in charger(chemin_resultats) if r["id"] not in deja]
        print(f"{len(a_faire)} cas à juger ({len(deja)} déjà faits)")
        for i, res in enumerate(a_faire, 1):
            print(f"[{i}/{len(a_faire)}] {res['id']}", flush=True)
            j = juger(cas_par_id[res["id"]], res, rubrique, version_grille)
            with open(sortie, "a", encoding="utf-8") as f:
                f.write(json.dumps(j, ensure_ascii=False) + "\n")
            deja[j["id"]] = j
            print(f"    {j['duree_s']:.0f} s | {j['verdict']} | {j['justification'][:100]}", flush=True)

    if deja:
        resumer(list(deja.values()))


if __name__ == "__main__":
    main()