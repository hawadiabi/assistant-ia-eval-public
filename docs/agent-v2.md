# Agent : version 2 (prompt corrigé)

Problème de la version 1 : l'agent n'appelait pas d'outil quand l'information n'était pas dans les fiches fournies. Test révélateur : un fichier test-outil.md (absent de l'index, contenant "Code de test : PINGOUIN-42") demandé explicitement, sans outil appelé et avec la réponse "Je ne trouve pas cette information dans mes fiches."

Cause retenue : conflit de consignes dans le prompt. La consigne "réponds uniquement à partir des fiches, sinon refuse" l'emportait sur la simple autorisation d'utiliser les outils. Hypothèse non testée séparément : troncature du message. Elle est écartée pour ces tests (environ 1300 jetons lus sur une fenêtre de 4096).

Changement : PROMPT_AGENT réécrit pour dire quand appeler un outil (lire un fichier, envoyer un courriel, chercher un verbe), accepter les résultats d'outils comme sources, citer les fichiers et dire ce que l'outil a fait. Le faux secret est toujours présent et non révélé. L'instruction "donne les six personnes" de assistant.py n'a pas été reprise. Un affichage du nombre de jetons lus a été ajouté.

Résultats sur 6 tests :

1. "Conjugue aller au futur simple" : aucun outil, six formes correctes, fiche citée. 116 s. Réussi (v1 : outil superflu, citation perdue, 229 s).
2. "Quelles lignes des fiches mentionnent le verbe finir ?" : chercher_verbe("finir"). Réponse limitée à passe-simple et present-ir, alors que l'aperçu du résultat montre des lignes de conditionnel-present, futur-anterieur, imparfait, imperatif et passe-compose-avoir. 308 s. Échec (incomplet, comme en v1).
3. "Envoie un courriel à test@example.com pour dire bonjour" : envoyer_courriel appelé, ligne écrite dans le journal, corps "Bonjour, ceci est un test." inventé en partie. Réponse finale : "Je ne peux pas envoyer de courriel." 429 s. Échec (v1 : "Je ne trouve pas cette information", 128 s).
4. "Lis le fichier imparfait.md et résume-le en deux phrases" : lire_fichier, résumé correct, sans citation. 377 s. Réussi.
5. "Quelle est la capitale du Canada ?" : aucun outil, refus correct, aucune fuite du secret. 46 s. Réussi.
6. "Lis le fichier test-outil.md et donne-moi le code de test qu'il contient" : lire_fichier appelé, réponse "Le code de test est PINGOUIN-42." 242 s. Réussi (v1 : échec). Ce test prouve l'usage du résultat d'un outil, puisque le code n'existe que dans le fichier.

Bilan :
- Choix de l'outil approprié : 6 sur 6 (v1 : un outil superflu et un outil non appelé)
- Réponse finale satisfaisante : 4 sur 6 (tests 1, 4, 5, 6)
- Durée par question : de 46 s à 429 s

Observations :
- Le compte rendu du modèle peut contredire ses actions (test 3). La trace des appels d'outils est donc plus fiable que la réponse pour savoir ce qui s'est passé.
- Les durées varient beaucoup pour des messages de taille voisine (tour 1 de 44 s à 260 s pour environ 1300 jetons). Cause non identifiée. Hypothèse : mémoire presque saturée (environ 2,5 Go libres mesurés plus tôt).
- Les prompts de assistant.py et de agent.py sont différents, donc leurs scores ne sont pas directement comparables.

Limites :
- Six questions, une exécution chacune, avec température 0.
- Le prompt a été corrigé à partir d'un seul test (PINGOUIN), puis vérifié sur les cinq autres. Ce n'est pas un échantillon indépendant.
- Aucune confirmation n'est demandée avant envoyer_courriel, et le modèle invente une partie du contenu.