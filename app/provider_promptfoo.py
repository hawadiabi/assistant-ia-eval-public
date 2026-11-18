import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from assistant import repondre  # noqa: E402


def call_api(prompt, options, context):
    texte, sources = repondre(prompt)
    # Même normalisation de l'apostrophe que evaluer.py
    texte = texte.replace("\u2019", "'")
    return {"output": texte, "metadata": {"sources": sources}}