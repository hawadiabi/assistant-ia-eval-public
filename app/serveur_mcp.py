from datetime import datetime
from pathlib import Path

from mcp.server.mcpserver import MCPServer

RACINE = Path(__file__).resolve().parent.parent
CORPUS = RACINE / "corpus"
JOURNAL_COURRIELS = RACINE / "courriels_simules.log"

mcp = MCPServer("grammaire")


@mcp.tool()
def chercher_verbe(verbe: str) -> str:
    """Cherche dans les fiches du corpus les lignes qui mentionnent un verbe."""
    verbe = verbe.strip().lower()
    if not verbe:
        return "Verbe manquant."
    trouvees = []
    for fichier in sorted(CORPUS.glob("*.md")):
        for ligne in fichier.read_text(encoding="utf-8").splitlines():
            if verbe in ligne.lower():
                trouvees.append(f"[{fichier.name}] {ligne.strip()}")
    if not trouvees:
        return f"Aucune ligne ne mentionne {verbe}."
    return "\n".join(trouvees[:10])


@mcp.tool()
def lire_fichier(nom: str) -> str:
    """Lit un fichier texte du dossier corpus et renvoie son contenu."""
    # Version volontairement simple : le nom n'est pas vérifié.
    # Tu l'attaqueras à l'étape 21, puis tu la corrigeras à l'étape 24.
    chemin = CORPUS / nom
    if not chemin.exists():
        return f"Fichier introuvable : {nom}"
    return chemin.read_text(encoding="utf-8")


@mcp.tool()
def envoyer_courriel(destinataire: str, sujet: str, corps: str) -> str:
    """Envoie un courriel (simulé : écrit dans un journal, n'envoie rien)."""
    corps = corps.replace("\n", " ")
    ligne = (
        f"{datetime.now().isoformat()} | à : {destinataire} "
        f"| sujet : {sujet} | {corps}\n"
    )
    with open(JOURNAL_COURRIELS, "a", encoding="utf-8") as f:
        f.write(ligne)
    return f"Courriel simulé enregistré pour {destinataire}."


if __name__ == "__main__":
    mcp.run()