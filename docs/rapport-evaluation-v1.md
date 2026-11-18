\# Rapport d'évaluation, version 1 (semaine 2)



\## Résumé



\- Sur 70 cas de test, l'assistant obtient 71 % d'exactitude selon la vérification par mots clés et 89 % de refus corrects sur les questions hors corpus.

\- Ce chiffre est probablement surestimé : parmi 9 réponses tirées au hasard et jugées bonnes par les deux méthodes automatiques, l'annotation humaine en trouve 3 défectueuses, dont 2 avec une citation fausse.

\- Le juge LLM (qwen2.5:7b) n'est pas fiable dans cette configuration : accord de 53 % avec l'annotation humaine sur le verdict acceptable ou non (kappa 0,16), contre 77 % pour la simple vérification par mots clés (kappa 0,51).

\- Les échecs principaux sont les faux refus (9 cas sur 52, dont 4 causés par la recherche) et les citations de fiches qui ne contiennent pas l'information.

\- promptfoo, utilisé comme vérification croisée sur les 6 cas dev, donne exactement les mêmes verdicts que le script maison.



\## 1. Objectif



Mesurer la qualité d'un assistant de grammaire française fondé sur un RAG (20 fiches), avant les tests de sécurité de la semaine 3, et évaluer la fiabilité des méthodes d'évaluation elles-mêmes.



\## 2. Méthode



\### Système évalué



\- Recherche : multilingual-e5-small, 3 fiches récupérées par question (docs/recherche-apres-e5.md)

\- Génération : llama3.1:8b via Ollama, sur processeur, température 0, num\_predict 400 (docs/eval-dev.md)

\- Prompt système : version 2 de assistant.py (docs/assistant-v2.md)



\### Jeu d'évaluation (evals/dataset.jsonl)



\- 76 cas : 6 dev (utilisés pour les ajustements) et 70 test (gelés avant la mesure)

\- 70 cas test : 21 conjugaisons, 19 règles, 12 pièges, 12 hors corpus, 6 sans rapport

\- 40 cas rédigés avec l'aide de Claude, 30 par moi



\### Quatre méthodes d'évaluation



1\. Vérification par mots clés (app/evaluer.py) : tous les mots clés présents, refus détecté par une phrase exacte, source récupérée et source citée.

2\. Juge LLM (app/juge.py) : qwen2.5:7b, choisi dans une autre famille que le modèle évalué pour limiter le biais d'auto-évaluation. Grille evals/rubric.md : 6 verdicts et 3 notes (exactitude, fidélité, complétude). Le juge reçoit les mêmes fiches que l'assistant.

3\. Annotation humaine (app/annoter.py) : 30 réponses jugées par moi avec la même grille, sans voir le verdict du juge. 9 cas tirés au hasard (graine fixe), annotés à l'aveugle, et 21 cas difficiles déjà analysés.

4\. promptfoo : vérification croisée sur les 6 cas dev, avec les mêmes critères que la méthode 1.



\### Règles d'annotation



\- Une réponse est correcte si elle est juste, soutenue par les fiches fournies et complète.

\- Une citation de fiche qui ne contient pas l'information rend la réponse incorrecte, même si le contenu est juste.

\- Un refus alors qu'une réponse existait dans le corpus est un faux refus, même si la fiche n'a pas été récupérée (la cause est notée en commentaire).

\- En cas d'hésitation entre correct et partiel : la réponse suffit-elle seule pour répondre correctement à la question ?



\## 3. Résultats de l'assistant (mots clés, 70 cas)



| Mesure | Résultat |

| --- | --- |

| Exactitude | 71 % (37/52) |

| Bonne fiche récupérée | 88 % (46/52) |

| Bonne fiche citée | 75 % (39/52) |

| Refus correct | 89 % (16/18) |

| Faux refus | 17 % (9/52) |



| Catégorie | Exactitude | Fiche récupérée | Faux refus |

| --- | --- | --- | --- |

| Conjugaison (21) | 57 % | 71 % | 33 % |

| Règle (19) | 95 % | 100 % | 0 % |

| Piège (12) | 58 % | 100 % | 17 % |



Durée moyenne : 65 s par cas sur processeur.



\## 4. Analyse des échecs



Détail dans docs/eval-test-v1.md. Cinq familles :



| Famille | Cas | Exemples |

| --- | --- | --- |

| Recherche ratée, puis refus | 4 | c02 (avoir au présent : present-irreguliers.md non récupérée) |

| Faux refus avec la bonne fiche fournie | 4 | p03, c35 (l'exemple exact était dans la fiche), c21, c22 |

| Réponse incomplète | 3 | c12, c14 (une personne sur six) |

| Erreur de fond | 3 | p06 (« je chanterais » présenté comme l'imparfait) |

| Réponse hors corpus avec citation inventée | 2 | c17, c31 |



L'annotation a fait apparaître des défauts supplémentaires dans des réponses comptées exactes :

\- c07 : cite present-er.md, fiche non fournie, et invente son contenu (« je ouvre »).

\- c09, c15 : formes justes, mais citation d'une fiche qui ne les contient pas.

\- c33 : ajoute des emplois du subjonctif absents de la fiche.



Constat principal : une citation ne garantit pas que la réponse vient de la source citée.



\## 5. Fiabilité des méthodes d'évaluation



| Comparaison avec l'annotation humaine | Accord | Kappa |

| --- | --- | --- |

| Juge LLM, 6 verdicts (30 cas) | 37 % | 0,18 |

| Juge LLM, acceptable ou non (30 cas) | 53 % | 0,16 |

| Mots clés, acceptable ou non (30 cas) | 77 % | 0,51 |

| Juge et mots clés, cas aléatoires (9 cas) | 67 % | 0,00 |



Sur les 9 cas aléatoires, le juge et les mots clés ont jugé les 9 réponses bonnes. L'annotation en trouve 3 défectueuses (c26 partielle, c09 et c15 avec une citation fausse). Le kappa vaut 0 parce que ces méthodes n'ont rien signalé.



Erreurs du juge (19 désaccords sur 30) :

\- 12 fois plus indulgent : 6 faux refus classés refus corrects, 3 réponses incomplètes classées correctes, 2 citations fausses et 1 erreur de fond (p06) non vues.

\- 5 fois dans la bonne direction mais avec la mauvaise étiquette (par exemple faux refus classé incorrect).

\- 2 fois plus sévère, à tort (c36, c37). Ses justifications décrivent alors mal la réponse.

\- Il n'a jamais utilisé le verdict reponse\_hors\_corpus.



Ses notes moyennes (4,5 sur 5) sont donc trompeuses.



Vérification croisée : promptfoo et evaluer.py donnent les mêmes verdicts sur les 6 cas dev (4 réussis, 2 échecs).



\## 6. Incidents de configuration (docs/eval-dev.md)



\- Sans limite de longueur, une réponse a produit plus de 1 250 jetons et bloqué l'évaluation environ 15 minutes. Correction : num\_predict = 400.

\- Une pénalité de répétition (1,2) supprimait la boucle de d03 mais cassait les conjugaisons (« J'allrai »). Elle a été retirée, et les boucles sont comptées comme des échecs.



\## 7. Limites



\- Une seule exécution par cas, à température 0, sur un seul modèle évalué.

\- Échantillons petits : 52 cas avec réponse attendue, 30 annotations dont 9 aléatoires. Les pourcentages par catégorie reposent sur 12 à 21 cas.

\- Une seule annotatrice, qui avait déjà vu les verdicts du juge pour 21 des 30 cas.

\- Les 21 cas annotés non aléatoires ont été choisis parce qu'ils étaient difficiles.

\- Les fiches et 40 cas de test ont été rédigés avec l'aide de Claude, ce qui peut avantager l'assistant.

\- Un seul modèle juge et une seule version de la grille.



\## 8. Recommandations



1\. Ne pas utiliser le juge LLM seul. Passer à une évaluation hybride :

&#x20;  - règle déterministe pour les refus (refus détecté comparé au refus attendu) ;

&#x20;  - vérification automatique des citations (la fiche citée contient-elle les formes ou la règle données ?) ;

&#x20;  - juge LLM réservé à la fidélité du texte libre, puis revalidé par une nouvelle annotation.

2\. Améliorer la recherche pour les questions de conjugaison (par exemple ajouter les noms des verbes aux morceaux indexés, ou combiner recherche par sens et par mots), puis mesurer avant et après.

3\. Revoir la consigne de refus, qui l'emporte parfois alors que la fiche contient la réponse.

4\. Semaine 3 : tests adversariaux sur l'agent (docs/surface-attaque.md). Les citations inventées observées ici montrent déjà qu'un contenu présenté comme issu d'une source peut ne pas l'être, ce qui rend l'injection indirecte particulièrement préoccupante.



\## Fichiers



\- Jeu et grille : evals/dataset.jsonl, evals/rubric.md

\- Résultats : evals/resultats\_assistant\_test.jsonl, evals/juge\_assistant\_test.jsonl, evals/annotations.jsonl, evals/promptfoo\_dev.json

\- Analyses : docs/eval-dev.md, docs/eval-test-v1.md

