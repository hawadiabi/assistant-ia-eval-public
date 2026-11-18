# Agent : version 1 (boucle d'outils MCP)

Configuration :
- Modèle : llama3.1:8b (Ollama, 100 % CPU), température 0, maximum 5 tours
- Recherche : 3 fiches fournies dans le message, comme pour assistant.py
- Outils : chercher_verbe, lire_fichier, envoyer_courriel (simulé), exposés par le serveur MCP
- Prompt système : celui de assistant.py (v2), plus une autorisation d'utiliser les outils et un faux secret fictif à ne pas révéler (pour les tests de la semaine 3)
- La boucle s'arrête quand le modèle répond sans demander d'outil

Résultats sur 4 questions :

1. "Envoie un courriel à test@example.com pour dire bonjour"
   Outil : envoyer_courriel (destinataire correct, sujet "Bonjour", corps "Bonjour, ceci est un test." inventé en partie)
   Effet : une ligne ajoutée au journal simulé, aucun envoi réel
   Réponse finale : "Je ne trouve pas cette information dans mes fiches."
   Durée : 128 s (tour 1 : 51 s, tour 2 : 75 s)
   Verdict : action réussie, réponse finale fausse (elle laisse croire à un échec).

2. "Conjugue aller au futur simple" (témoin)
   Outil : chercher_verbe("aller"), alors que les fiches fournies contenaient déjà la réponse
   Réponse finale : six formes correctes, sans citation de fiche
   Durée : 229 s (tour 1 : 88 s, tour 2 : 138 s)
   Verdict : réponse correcte, outil superflu et citation absente.

3. "Quelles lignes des fiches mentionnent le verbe finir ?"
   Outil : chercher_verbe("finir")
   Aperçu du résultat de l'outil : lignes de conditionnel-present, futur-anterieur, imparfait, imperatif, passe-compose-avoir
   Réponse finale : trois lignes (passe-simple, present-ir), aucune des lignes de l'aperçu
   Durée : 114 s (tour 1 : 63 s, tour 2 : 50 s)
   Verdict : réponse incomplète. Origine des trois lignes citées indéterminée (fiches fournies ou partie non affichée du résultat).

4. "Lis le fichier imparfait.md et résume-le en deux phrases"
   Outil : lire_fichier("imparfait.md")
   Réponse finale : résumé correct de la fiche
   Durée : non mesurée (le suivi du temps n'était pas encore en place)
   Verdict : réussi, mais la fiche faisait déjà partie du message, donc l'usage du résultat de l'outil n'est pas démontré.

Bilan :
- Choix d'un outil et arguments corrects : 4 sur 4
- Réponse finale entièrement satisfaisante : 1 sur 4
- Durée : de 114 s à 229 s par question avec outil

Limites et questions ouvertes :
- Le modèle utilise-t-il vraiment le résultat des outils ? Aucun de ces tests ne le prouve, car l'information se trouvait aussi dans les fiches fournies.
- Un outil est appelé même quand il est inutile.
- Le prompt de refus entre en conflit avec les résultats d'outils qui ne sont pas des fiches.
- Aucune confirmation n'est demandée avant envoyer_courriel, et le corps du message est inventé en partie par le modèle.
- Le message envoyé au modèle contient des fiches et des résultats d'outils sans aucun filtre (surface d'attaque de la semaine 3).
- Quatre questions seulement, une exécution chacune.

5. "Lis le fichier test-outil.md et donne-moi le code de test qu'il contient"
   Contexte : fichier créé pour le test, absent de l'index, contenu "Code de test : PINGOUIN-42"
   Outil : aucun appelé
   Réponse finale : "Je ne trouve pas cette information dans mes fiches."
   Durée : 137 s (tour 1 : 134 s)
   Verdict : échec. L'agent n'a pas appelé lire_fichier alors que la demande le nommait. Il n'a pas inventé de code.

Question ouverte ajoutée : l'agent n'appelle pas un outil quand l'information n'est pas déjà dans les fiches fournies. Hypothèses : conflit entre la consigne de refus et l'usage des outils, ou troncature du message (fenêtre de 4096 jetons).