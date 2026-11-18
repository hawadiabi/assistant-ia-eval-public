# Assistant RAG : version 2

Changement par rapport à la version 1 : le prompt système a été modifié (ne rien affirmer que les fiches ne disent pas, donner les six personnes pour une conjugaison, expliquer la règle ou l'astuce de la fiche quand la bonne réponse dépend d'un contexte absent). Même recherche, même modèle, température 0.

Résultats sur les mêmes 4 questions :

1. "Conjugue aller au futur simple"
   Réponse : j'irai, tu iras, il ira, nous irons, vous irez, ils iront [futur-simple-irreguliers.md]
   Verdict : réussi (v1 : partiel).

2. "Comment accorder leparticipe passé avec avoir ?" (même faute d'espace qu'en v1, question identique)
   Réponse : la règle de l'accord avec le COD placé avant le verbe [accord-participe-passe-avoir.md]
   Verdict : réussi (inchangé).

3. "Faut-il écrire parler ou parlé ?"
   Réponse : "Je ne trouve pas cette information dans mes fiches."
   Fiche la mieux classée : infinitif-ou-participe-passe, qui contient l'astuce de remplacement
   Verdict : échec (faux refus). La v1 affirmait "parler" sans soutien de la fiche, la v2 refuse alors que l'information était disponible.

4. "Quelle est la capitale du Canada ?" (hors sujet)
   Réponse : "Je ne trouve pas cette information dans mes fiches."
   Verdict : réussi (inchangé).

Bilan : 3 réussis, 1 échec sur 4 (v1 : 2 réussis, 1 partiel, 1 échec).

Observations :
- Le changement de prompt a corrigé la conjugaison incomplète, mais a transformé une réponse non fidèle en faux refus. Le compromis fidélité contre utilité est à mesurer sur le jeu d'évaluation complet.
- Les quatre questions sont les mêmes que celles utilisées pour ajuster le prompt : le score de 3 sur 4 ne prouve rien sur la qualité générale.
- Limite : une seule exécution par question (température 0), sans jeu de questions indépendant.