# Essai dev de l'évaluation (6 cas)

Objectif : vérifier que le script evaluer.py fonctionne de bout en bout et fixer la configuration de génération avant la série test.

## Configuration retenue

- Recherche : multilingual-e5-small, 3 fiches récupérées par question
- Modèle : llama3.1:8b (Ollama, 100 % CPU)
- Options : température 0, num_predict 400, sans pénalité de répétition
- Prompt système : version 2 de assistant.py (voir docs/assistant-v2.md)

## Résultats

| Cas | Question | Durée | Verdict automatique |
| --- | --- | --- | --- |
| d01 | Conjugue aller au futur simple | 136 s | exact |
| d02 | Comment accorder le participe passé avec avoir ? | 83 s | exact |
| d03 | Quand utilise-t-on le subjonctif ? | 234 s | non exact |
| d04 | Écris le verbe manger à l'imparfait | 98 s | exact |
| d05 | Faut-il écrire parler ou parlé ? | 61 s | faux refus |
| d06 | Quelle est la capitale du Canada ? | 60 s | refus correct |

Résumé :
- Exactitude : 3 sur 5
- Source récupérée : 5 sur 5
- Source citée : 3 sur 5
- Refus correct : 1 sur 1
- Faux refus : 1 sur 5
- Durée moyenne : 112 s par cas

La recherche fournit la bonne fiche dans tous les cas. Les échecs viennent donc de la génération, pas de la recherche.

## Incident 1 : génération sans limite

Un premier essai, sans limite de longueur, a été interrompu sur d03. Le journal d'Ollama montrait plus de 1 250 jetons générés pour une seule réponse, à environ 1,4 jeton par seconde, soit environ 15 minutes de calcul. Le script ne répondait plus à Ctrl+C et a dû être arrêté avec ollama stop.

Correction : num_predict = 400. Les deux cas terminés avant l'interruption (d01 et d02) ont été relancés avec la nouvelle configuration, pour que les 6 cas soient mesurés de la même façon.

## Incident 2 : boucle de répétition sur d03

Avec la limite, d03 se termine mais tourne en boucle. Extrait de la réponse : "Le subjonctif est utilisé après les verbes qui expriment un doute, un incertitude, un souhait, une volonté, une obligation, une concession, une condition, une cause, un but, un résultat, un moyen, un temps, un lieu, un moyen, un instrument, un objet..." La même suite est répétée jusqu'à la coupure à 400 jetons.

La réponse n'utilise pas la fiche subjonctif-present.md, pourtant récupérée en premier, qui contient la réponse attendue ("après il faut que, vouloir que, bien que, pour que, avant que").

## Essai de correction : pénalité de répétition

Configuration testée : repeat_penalty = 1.2.

- d03 : la boucle disparaît. La réponse cite la fiche et donne ses exemples ("Il faut que tu partes", "Je veux qu'elle vienne"), mais elle affirme aussi que le subjonctif s'emploie "après les verbes qui introduisent des conditions ou des hypothèses". La fiche ne le dit pas, et c'est trompeur (après si exprimant une condition, on n'emploie pas le subjonctif). Les mots clés auraient compté cette réponse comme exacte.
- Témoin "Conjugue aller au futur simple" : réponse "J'allrai", une seule forme, mot inexistant.
- Après retrait de la pénalité, le même témoin redonne les six formes correctes avec la bonne fiche citée.

Décision : pénalité retirée. La conjugaison est la tâche principale de l'assistant, et la limite de 400 jetons suffit à empêcher le blocage. Les boucles sont comptées comme des échecs dans l'évaluation.

Les résultats du tableau ci-dessus ont été obtenus avec la configuration retenue (sans pénalité). La version 1 du fichier de résultats est conservée dans evals/resultats_assistant_dev_v1.jsonl.

## Hypothèse pour d05 (faux refus)

La fiche infinitif-ou-participe-passe.md, récupérée en premier, contient la règle (remplacer par vendre ou vendu), mais aucun exemple avec "parler". Le modèle refuse peut-être parce qu'il ne retrouve pas le mot exact de la question, au lieu d'appliquer la règle générale. À vérifier sur la série test avec d'autres verbes absents des exemples des fiches.

## Vérification manuelle des verdicts

| Cas | Verdict automatique | Mon verdict | Commentaire |
| --- | --- | --- | --- |
| d01 | exact |exact|D'accord|
| d02 | exact |exact|D'accord|
| d03 | non exact |non exact|D’accord. Réponse en boucle, n’utilise pas la fiche.|
| d04 | exact |exact|D'accord|
| d05 | faux refus |faux refus|D'accord. Des indications sont présentes pour le participe passé dans le corpus mais pas pour le verbe parler|
| d06 | refus correct |refus correct|D'accord. Pas de lien avec le corpus|

Accord avec le verdict automatique : 6 sur 6. Sur ces 6 cas, la vérification par mots clés juge comme moi. Elle reste à vérifier sur la série test, notamment pour les réponses qui contiennent les bons mots mais affirment autre chose que la fiche.

## Limites

- 6 cas seulement, déjà utilisés pour ajuster la recherche et le prompt : ces résultats ne mesurent pas la qualité générale.
- Un seul essai par configuration pour la pénalité de répétition, sur deux questions.
- La vérification par mots clés ne détecte pas les réponses infidèles qui contiennent les bons mots (voir l'essai avec pénalité sur d03).
- Durées très variables (60 à 234 s), probablement liées à la mémoire disponible (non mesuré pendant l'essai).