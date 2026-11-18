# Assistant RAG : version 1

Configuration :
- Recherche : multilingual-e5-small, 3 fiches récupérées par question
- Modèle de génération : llama3.1:8b (Ollama), température 0
- Consigne : répondre uniquement à partir des fiches, citer la fiche entre crochets, refuser si l'information est absente
- Les fiches entières sont insérées dans le message envoyé au modèle

Résultats sur 4 questions :

1. "Conjugue aller au futur simple"
   Réponse : "J'irai [futur-simple-irreguliers.md]."
   Fiches consultées : futur-simple-irreguliers, futur-simple-er, passe-simple
   Verdict : partiel. La forme est correcte et la source aussi, mais seule la 1re personne est donnée alors que la question demande de conjuguer.

2. "Comment accorder leparticipe passé avec avoir ?" (question tapée avec une faute d'espace)
   Réponse : la règle de l'accord avec le COD placé avant le verbe [accord-participe-passe-avoir.md]
   Fiches consultées : accord-participe-passe-avoir, accord-participe-passe-etre, participe-passe-pronominaux
   Verdict : réussi.

3. "Faut-il écrire parler ou parlé ?"
   Réponse : "Il faut écrire parler. [infinitif-ou-participe-passe.md]"
   Fiches consultées : infinitif-ou-participe-passe, imperatif, present-er
   Verdict : échec de fidélité. La question n'a pas de contexte et la fiche donne une astuce de remplacement, pas une règle qui impose parler. La réponse affirme plus que la source et cite pourtant la bonne fiche.

4. "Quelle est la capitale du Canada ?" (hors sujet)
   Réponse : "Je ne trouve pas cette information dans mes fiches."
   Fiches consultées : conditionnel-present, futur-anterieur, accord-participe-passe-avoir
   Verdict : réussi (refus correct).

Bilan : 2 réussis, 1 partiel, 1 échec sur 4.

Observations :
- Un score "bonne fiche citée" ne détecterait pas l'échec de la question 3, ce qui justifie un juge qui vérifie si la réponse est soutenue par la source.
- La recherche renvoie toujours 3 fiches, même pour une question sans rapport. Le refus dépend donc entièrement du modèle.
- Limite : 4 questions seulement, à confirmer avec le jeu d'évaluation complet (étape 13).