# Recherche : version 2 (découpage en morceaux et distance cosinus)

Changements par rapport à la version 1 :
- Chaque fiche est découpée par paragraphe, avec le titre répété dans chaque morceau (20 fiches, 79 morceaux)
- Distance cosinus (0 = même sens, 1 = aucun rapport)
- On garde le meilleur morceau par fiche
- Même modèle d'embeddings que la version 1

Résultats sur les mêmes 5 questions :

1. "Conjugue aller au futur simple"
   Obtenu : futur-simple-irreguliers (0.29), conditionnel-present (0.32), futur-anterieur (0.32)
   Résultat : réussi

2. "Comment accorder le participe passé avec avoir ?" (sans faute de frappe cette fois)
   Obtenu : accord-participe-passe-etre (0.27), plus-que-parfait (0.38), passe-compose-avoir (0.41)
   Résultat : échec (attendue absente du top 3)

3. "Quand utilise-t-on le subjonctif ?"
   Obtenu : futur-anterieur (0.56), imparfait (0.56), conditionnel-present (0.59)
   Résultat : échec (attendue absente du top 3)

4. "Écris le verbe manger à l'imparfait"
   Obtenu : imparfait (0.18), imperatif (0.22), verbes-ger-cer (0.23)
   Résultat : réussi

5. "Faut-il écrire parler ou parlé ?"
   Obtenu : futur-simple-er (0.46), present-er (0.47), verbes-dre (0.50)
   Résultat : échec (attendue absente du top 3)

Score : 2 sur 5, sans amélioration.

Conclusion : le découpage seul ne règle pas le problème. L'hypothèse initiale (début de fiche seul lu par le modèle) n'explique pas à elle seule les échecs.