# Recherche : version 1 (une fiche entière = un vecteur)

Configuration :
- Modèle d'embeddings : paraphrase-multilingual-MiniLM-L12-v2
- Corpus : 20 fiches, chaque fiche entière indexée comme un seul vecteur
- Distance : distance par défaut de ChromaDB (valeurs entre 4 et 17, difficiles à interpréter)

Résultats sur 5 questions tests (fiche attendue en 1re position) :

1. "Conjugue aller au futur simple"
   Attendue : futur-simple-irreguliers.md
   Obtenu : futur-simple-irreguliers (7.15), conditionnel-present (7.95), futur-anterieur (8.54)
   Résultat : réussi

2. "Comment accorder le participe passé avec avoir ?" (la question contenait une faute de frappe : "leparticipe")
   Attendue : accord-participe-passe-avoir.md
   Obtenu : accord-participe-passe-etre (4.99), participe-passe-pronominaux (6.31), accord-participe-passe-avoir (6.37)
   Résultat : échec (attendue en 3e position)

3. "Quand utilise-t-on le subjonctif ?"
   Attendue : subjonctif-present.md
   Obtenu : participe-passe-pronominaux (8.65), accord-participe-passe-avoir (9.08), accord-participe-passe-etre (9.42)
   Résultat : échec (attendue absente du top 3)

4. "Écris le verbe manger à l'imparfait"
   Attendue : imparfait.md ou verbes-ger-cer.md
   Obtenu : verbes-ger-cer (4.77), present-er (5.70), futur-simple-er (6.09)
   Résultat : réussi

5. "Faut-il écrire parler ou parlé ?"
   Attendue : infinitif-ou-participe-passe.md
   Obtenu : futur-simple-er (14.78), present-er (15.74), verbes-dre (16.17)
   Résultat : échec (attendue absente du top 3)

Score : 2 sur 5.

Hypothèse de départ : le modèle ne lit que le début de chaque fiche, donc la fiche entière est mal représentée. Piste testée ensuite : découper les fiches en morceaux et passer à la distance cosinus.