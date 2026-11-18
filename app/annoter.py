import argparse
import json
import random
from collections import Counter
from pathlib import Path

DATASET = Path("evals/dataset.jsonl")
RESULTATS = Path("evals/resultats_assistant_test.jsonl")
JUGE = Path("evals/juge_assistant_test.jsonl")
SORTIE = Path("evals/annotations.jsonl")

VERDICTS = [
    "correct", "partiel", "incorrect",
    "faux_refus", "refus_correct", "reponse_hors_corpus",
]
ACCEPTABLES = {"correct", "refus_correct"}

DEJA_ANALYSES = [
    "c02", "c10", "c12", "c13", "c14", "p03", "p06", "c16", "c17", "c19",
    "c21", "c22", "c29", "c31", "c35", "c38", "c40", "c07", "c33", "c36", "c37",
]
NB_ALEATOIRES = 9
GRAINE = 42


def charger(chemin):
    lignes = chemin.read_text(encoding="utf-8").splitlines()
    return [json.loads(ligne) for ligne in lignes if ligne.strip()]


def selection(ids_test):
    restants = sorted(i for i in ids_test if i not in DEJA_ANALYSES)
    aleatoires = random.Random(GRAINE).sample(restants, NB_ALEATOIRES)
    # Les cas aléatoires d'abord : ils sont annotés à l'aveugle
    return [(i, "aleatoire") for i in aleatoires] + [
        (i, "deja_analyse") for i in DEJA_ANALYSES
    ]


def annoter():
    cas = {c["id"]: c for c in charger(DATASET)}
    res = {r["id"]: r for r in charger(RESULTATS)}
    deja = {a["id"] for a in charger(SORTIE)} if SORTIE.exists() else set()
    a_faire = [(i, g) for i, g in selection(res.keys()) if i not in deja]
    print(f"{len(a_faire)} cas à annoter ({len(deja)} déjà faits). Tape q pour arrêter.")

    for n, (i, groupe) in enumerate(a_faire, 1):
        c, r = cas[i], res[i]
        print("\n" + "=" * 60)
        print(f"[{n}/{len(a_faire)}] {i} ({c['categorie']})")
        print("Question :", c["question"])
        if c["reponse_attendue"] == "REFUS":
            print("Réponse attendue : REFUS (information absente des fiches)")
        else:
            print("Réponse attendue :", c["reponse_attendue"])
        print("Fiches fournies :", ", ".join(r["sources_recuperees"]))
        print("\nRéponse de l'assistant :\n" + r["reponse"])
        print("\n" + "  ".join(f"{k}={v}" for k, v in enumerate(VERDICTS, 1)))
        while True:
            choix = input("Ton verdict (1 à 6, ou q pour arrêter) : ").strip().lower()
            if choix == "q":
                return
            if choix in {"1", "2", "3", "4", "5", "6"}:
                break
            print("Choix invalide.")
        commentaire = input("Commentaire (facultatif) : ").strip()
        ligne = {
            "id": i,
            "groupe": groupe,
            "verdict_humain": VERDICTS[int(choix) - 1],
            "commentaire": commentaire,
        }
        with open(SORTIE, "a", encoding="utf-8") as f:
            f.write(json.dumps(ligne, ensure_ascii=False) + "\n")
    print("\nAnnotation terminée.")


def kappa(a, b):
    """Kappa de Cohen : accord corrigé de l'accord dû au hasard."""
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(a) | set(b)) / (n * n)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def acceptable_mots_cles(r):
    if r["exact"] is not None:
        return r["exact"]
    return bool(r["refus_correct"])


def comparer(nom, humain, autre):
    n = len(humain)
    accords = sum(h == a for h, a in zip(humain, autre))
    print(f"  {nom} : accord {accords}/{n} ({100 * accords / n:.0f} %), "
          f"kappa {kappa(humain, autre):.2f}")


def calculer():
    annotations = charger(SORTIE)
    res = {r["id"]: r for r in charger(RESULTATS)}
    juge = {j["id"]: j for j in charger(JUGE)}

    groupes = [
        ("Tous les cas annotés", None),
        ("Cas aléatoires (à l'aveugle)", "aleatoire"),
        ("Cas déjà analysés", "deja_analyse"),
    ]
    for titre, groupe in groupes:
        sel = [a for a in annotations if groupe is None or a["groupe"] == groupe]
        if not sel:
            continue
        print(f"\n== {titre} ({len(sel)} cas) ==")
        h = [a["verdict_humain"] for a in sel]
        j = [juge[a["id"]]["verdict"] for a in sel]
        comparer("Juge, 6 verdicts", h, j)
        comparer("Juge, acceptable ou non",
                 [v in ACCEPTABLES for v in h], [v in ACCEPTABLES for v in j])
        comparer("Mots clés, acceptable ou non",
                 [v in ACCEPTABLES for v in h],
                 [acceptable_mots_cles(res[a["id"]]) for a in sel])

    print("\nDésaccords entre toi et le juge :")
    for a in annotations:
        v = juge[a["id"]]["verdict"]
        if v != a["verdict_humain"]:
            print(f"  {a['id']} : toi = {a['verdict_humain']}, juge = {v}")
    print("\nTes verdicts :", dict(Counter(a["verdict_humain"] for a in annotations)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--calcul", action="store_true")
    args = parser.parse_args()
    calculer() if args.calcul else annoter()