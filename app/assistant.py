import sys
from pathlib import Path

import ollama

from recherche import chercher

CORPUS = Path("corpus")
MODELE_LLM = "llama3.1:8b"

# Paramètres de génération :
# - temperature 0 : réponses stables d'une exécution à l'autre
# - num_predict 400 : coupe les réponses trop longues (cas d03, boucle de plus de 1 250 jetons)
# - repeat_penalty 1.2 testé puis retiré : il cassait les conjugaisons ("J'allrai")
OPTIONS_LLM = {"temperature": 0, "num_predict": 400}

PROMPT_SYSTEME = (
    "Tu es un assistant de grammaire française. "
    "Réponds uniquement à partir des fiches fournies et n'affirme rien "
    "qu'elles ne disent pas. "
    "Si la réponse ne s'y trouve pas, réponds exactement : "
    "\"Je ne trouve pas cette information dans mes fiches.\" "
    "Si on te demande de conjuguer un verbe, donne les six personnes. "
    "Si la bonne réponse dépend d'un contexte absent de la question, "
    "explique la règle ou l'astuce de la fiche au lieu de choisir une réponse. "
    "Cite la fiche utilisée entre crochets, par exemple [imparfait.md]. "
    "Réponds en français, de façon brève."
)


def repondre(question, n_fiches=3):
    resultats = chercher(question, n=n_fiches)
    sources = [source for source, _ in resultats]

    fiches = []
    for source in sources:
        texte = (CORPUS / source).read_text(encoding="utf-8")
        fiches.append(f"[{source}]\n{texte}")
    contexte = "\n\n---\n\n".join(fiches)

    messages = [
        {"role": "system", "content": PROMPT_SYSTEME},
        {
            "role": "user",
            "content": f"Fiches :\n\n{contexte}\n\nQuestion : {question}",
        },
    ]
    reponse = ollama.chat(model=MODELE_LLM, messages=messages, options=OPTIONS_LLM)
    return reponse["message"]["content"], sources


if __name__ == "__main__":
    question = " ".join(sys.argv[1:])
    texte, sources = repondre(question)
    print(texte)
    print("\nFiches consultées :", ", ".join(sources))