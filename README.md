# assistant-ia-eval

Projet d'évaluation et de sécurité d'un petit assistant IA : un assistant de grammaire française (recherche dans des fiches, puis génération de la réponse) qui peut aussi appeler des outils. Le sujet est volontairement simple. Ce qui compte ici, c'est la manière de l'évaluer, de l'attaquer, de le corriger et de le surveiller.

## Résultats clés

| Mesure | Résultat |
| --- | --- |
| Exactitude sur le jeu de test (mots clés, 52 cas) | 71 %, probablement surestimée : 3 des 9 réponses tirées au hasard et jugées bonnes automatiquement avaient un défaut |
| Accord entre le juge LLM et l'annotation humaine (30 cas) | 53 % (kappa 0,16), contre 77 % (kappa 0,51) pour la vérification par mots clés |
| Attaques réussies avant et après les contre-mesures | à mesurer (semaine 3) |

Détail : docs/rapport-evaluation-v1.md

## État d'avancement

Étapes 1 à 18 sur 31 : assistant, recherche, serveur MCP, agent et évaluation complète (métriques, juge LLM, annotation humaine, promptfoo). Tests adversariaux et surveillance à venir.

## Architecture

1. Les fiches de corpus/ sont découpées en morceaux et indexées dans ChromaDB (modèle d'embeddings multilingual-e5-small).
2. Pour chaque question, les 3 fiches les plus proches sont ajoutées au message envoyé à llama3.1:8b (Ollama, sur processeur).
3. L'agent peut appeler 3 outils exposés par un serveur MCP : chercher un verbe, lire un fichier, envoyer un courriel (simulé, rien n'est envoyé).
4. Les résultats des outils retournent au modèle, jusqu'à 5 tours.

Voir docs/surface-attaque.md pour les points d'entrée de données non fiables.

## Installation (Windows, PowerShell)

1. Installer Python 3.12, Git et Ollama.
2. Télécharger le modèle : `ollama pull llama3.1:8b`
3. Créer l'environnement :

    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt

## Utilisation

    python app\indexer.py
    python app\recherche.py "Conjugue aller au futur simple"
    python app\assistant.py "Conjugue aller au futur simple"
    python app\agent.py "Conjugue aller au futur simple"

Sur un processeur sans carte graphique, compte de quelques dizaines de secondes à plus de 7 minutes par question avec l'agent.

## Contenu du dépôt

- app/ : indexation, recherche, assistant, agent, serveur MCP et scripts de test
- corpus/ : 20 fiches de grammaire
- docs/ : journal des essais, échecs compris (recherche, assistant, MCP, agent), surface d'attaque

## Limites connues

- Corpus de 20 fiches seulement.
- Modèle local de 8 milliards de paramètres, qui se trompe parfois sur la conjugaison et sur l'usage des outils.
- Les premiers essais ont été faits sur très peu de questions et ne prouvent pas la qualité générale.