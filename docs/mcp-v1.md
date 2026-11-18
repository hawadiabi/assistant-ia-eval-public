# Serveur MCP : version 1

Configuration :
- SDK : mcp 2.3.0 (Python), transport stdio
- Trois outils : chercher_verbe (lecture seule), lire_fichier (lit un fichier du dossier corpus), envoyer_courriel (simulé : écrit dans courriels_simules.log, n'envoie rien)
- Test : script test_mcp.py, qui appelle les outils directement, sans modèle

Incident au premier test :
- Symptôme : "Connection closed" au moment de initialize(), et aucun journal créé.
- Cause : le serveur utilisait from mcp.server.fastmcp import FastMCP. Dans la version 2 du SDK, FastMCP a été renommé MCPServer (mcp.server.mcpserver), donc le serveur plantait à l'import et le client ne recevait aucun message.
- Diagnostic : lancement du serveur seul (python app\serveur_mcp.py), qui a affiché l'erreur d'import, puis pip show mcp pour confirmer la version.
- Correction : deux lignes modifiées (l'import et la création du serveur). Les décorateurs @mcp.tool() sont restés identiques.

Résultats du test :
- list_tools : chercher_verbe, lire_fichier, envoyer_courriel. Réussi.
- chercher_verbe("aller") : 10 lignes issues de 8 fiches. Réussi.
- lire_fichier("imparfait.md") : contenu complet de la fiche. Réussi.
- envoyer_courriel : "Courriel simulé enregistré", ligne écrite dans le journal. Réussi.

Limites connues (à traiter en semaine 3) :
- lire_fichier ne vérifie pas le nom reçu. Un nom contenant ../ pourrait sortir du dossier corpus.
- envoyer_courriel accepte n'importe quel destinataire et n'importe quel contenu, sans confirmation.
- chercher_verbe renvoie du texte du corpus tel quel, sans filtre.
- Les outils ont été testés directement, pas encore appelés par un modèle.