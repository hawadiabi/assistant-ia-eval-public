# Recherche : version 3 (multilingual-e5-small)

Changements par rapport à la version 2 :
- Modèle d'embeddings : intfloat/multilingual-e5-small
- Préfixe "passage: " pour les morceaux indexés et "query: " pour les questions
- Même découpage (20 fiches, 79 morceaux) et même distance cosinus

Premier essai invalide :
- Les distances étaient toutes entre 0.90 et 0.97 et les mêmes fiches revenaient pour des questions différentes.
- Cause probable : recherche.py utilisait encore l'ancien modèle ou n'avait pas le préfixe "query: " pendant que l'indexeur utilisait e5.
- Correction : recherche.py remplacé en entier, puis réindexation. Cet essai n'est pas compté dans les résultats.

Résultats sur les mêmes 5 questions :

1. "Conjugue aller au futur simple"
   Obtenu : futur-simple-irreguliers (0.10), futur-simple-er (0.12), passe-simple (0.13)
   Résultat : réussi

2. "Comment accorder le participe passé avec avoir ?"
   Obtenu : accord-participe-passe-avoir (0.09), accord-participe-passe-etre (0.11), participe-passe-pronominaux (0.11)
   Résultat : réussi

3. "Quand utilise-t-on le subjonctif ?"
   Obtenu : subjonctif-present (0.14), verbes-ger-cer (0.18), conditionnel-present (0.19)
   Résultat : réussi

4. "Écris le verbe manger à l'imparfait"
   Obtenu : infinitif-ou-participe-passe (0.12), imparfait (0.13), verbes-ger-cer (0.13)
   Résultat : échec en 1re position (les deux fiches attendues sont en 2e et 3e positions)

5. "Faut-il écrire parler ou parlé ?"
   Obtenu : infinitif-ou-participe-passe (0.16), imperatif (0.17), present-er (0.17)
   Résultat : réussi

Score : 4 sur 5, contre 2 sur 5 pour les versions 1 et 2.

Limites :
- Seulement 5 questions, les mêmes qui ont servi à comparer les modèles. Le résultat peut être trop optimiste.
- Écarts de distance très faibles entre les rangs (souvent 0.01 à 0.02), donc classement fragile.
- Hypothèse non vérifiée pour la question 4 : le mot "manger" apparaît dans les exemples de infinitif-ou-participe-passe.

Suite : mesurer la recherche sur le jeu d'évaluation complet (étape 13), avec des questions non utilisées pour choisir le modèle.