# Diagnostic de la recherche (modèle MiniLM)

Objectif : savoir si les échecs viennent de l'indexation ou du modèle d'embeddings.

Test 1 : requêtes avec les mots exacts des titres de fiches
- "subjonctif présent" : futur-anterieur (0.36), plus-que-parfait (0.39), passe-compose-etre (0.39)
  La fiche subjonctif-present n'est pas dans le top 3.
- "infinitif ou participe passé" : verbes-dre (0.25), plus-que-parfait (0.29), passe-compose-avoir (0.30)
  La fiche infinitif-ou-participe-passe n'est pas dans le top 3.

Test 2 : rang de tous les morceaux de subjonctif-present pour la requête "subjonctif présent" (script diagnostic.py)
- Les 5 morceaux de la fiche sont bien dans la base, aux rangs 5, 7, 11, 34 et 40 (distances de 0.42 à 0.57)
- Les rangs 1 à 4 sont occupés par des morceaux de futur-anterieur, plus-que-parfait et passe-compose-etre
- La fiche subjonctif-present arrive donc en 4e position parmi les fiches distinctes

Constats :
- L'indexation est correcte : 20 fiches, 79 morceaux, aucun morceau manquant
- Même avec le titre exact comme requête, le modèle classe d'autres fiches devant la bonne

Hypothèse (non vérifiée) : le modèle paraphrase-multilingual-MiniLM est peu adapté à la recherche de passages à partir d'une question, surtout sur un corpus composé de nombreuses formes conjuguées qui se ressemblent.

Piste suivante : tester multilingual-e5-small (conçu pour la recherche, avec les préfixes "query: " et "passage: ") et comparer les 5 mêmes questions.

Limite à signaler dans le rapport final : corpus petit (20 fiches), jeu de test de seulement 5 questions à ce stade, résultats à confirmer avec le jeu d'évaluation complet de la semaine 2.