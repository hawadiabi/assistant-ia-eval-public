\# Grille d'évaluation des réponses de l'assistant



L'assistant doit répondre uniquement à partir des fiches fournies. Si l'information n'y est pas, il doit répondre "Je ne trouve pas cette information dans mes fiches."



\## Verdict (un seul choix)



\- correct : la réponse est juste, complète et soutenue par les fiches.

\- partiel : la réponse est juste mais incomplète (par exemple une seule personne au lieu de six pour une conjugaison).

\- incorrect : la réponse contient une erreur de fond, ou affirme quelque chose que les fiches ne disent pas.

\- faux\_refus : l'assistant refuse alors que la réponse attendue n'est pas un refus.

\- refus\_correct : un refus était attendu et l'assistant a refusé.

\- reponse\_hors\_corpus : un refus était attendu, mais l'assistant a répondu quand même.



Si la réponse commence par un refus puis répond quand même, juge le contenu de la réponse, et signale la contradiction dans la justification.



\## Notes de 1 à 5



\- exactitude : la réponse est-elle juste en français, par rapport à la réponse attendue ? (1 = fausse, 5 = entièrement juste)

\- fidelite : chaque affirmation est-elle soutenue par les fiches fournies, et la fiche citée contient-elle vraiment l'information ? (1 = inventée ou citation fausse, 5 = entièrement soutenue)

\- completude : la réponse couvre-t-elle tout ce que la question demande ? (1 = presque rien, 5 = complète)



Pour un refus correct, mets 5 aux trois notes. Pour un faux refus, mets 1 aux trois notes.



\## Justification



Une ou deux phrases qui expliquent le verdict, en citant l'erreur précise s'il y en a une.

