# Évaluation de l'assistant : série test, version 1

## Configuration

- Recherche : multilingual-e5-small, 3 fiches récupérées par question
- Modèle : llama3.1:8b (Ollama, 100 % CPU)
- Options : température 0, num_predict 400, sans pénalité de répétition
- Prompt système : version 2 de assistant.py
- Script : app/evaluer.py (vérification par mots clés)
- Résultats bruts : evals/resultats_assistant_test.jsonl
- Durée totale : environ 76 minutes (65 s par cas en moyenne)

## Résultats globaux

| Mesure | Résultat |
| --- | --- |
| Exactitude | 71 % (37/52) |
| Bonne fiche récupérée | 88 % (46/52) |
| Bonne fiche citée | 75 % (39/52) |
| Refus correct (hors corpus et sans rapport) | 89 % (16/18) |
| Faux refus | 17 % (9/52) |

## Résultats par catégorie

| Catégorie | Cas | Exactitude | Fiche récupérée | Fiche citée | Faux refus | Refus correct |
| --- | --- | --- | --- | --- | --- | --- |
| Conjugaison | 21 | 57 % | 71 % | 57 % | 33 % | sans objet |
| Règle | 19 | 95 % | 100 % | 95 % | 0 % | sans objet |
| Piège | 12 | 58 % | 100 % | 75 % | 17 % | sans objet |
| Hors corpus | 12 | sans objet | sans objet | sans objet | sans objet | 83 % |
| Sans rapport | 6 | sans objet | sans objet | sans objet | sans objet | 100 % |

## Analyse des 17 échecs

Lecture manuelle de chaque cas non exact ou mal refusé, classé selon la cause probable.

### 1. Recherche ratée (4 cas)

La fiche attendue n'a pas été fournie au modèle, qui a refusé. Avec le contexte reçu, le refus est le bon comportement : l'échec vient de la recherche.

- c02 (avoir au présent) : fiches reçues present-ir, imparfait, imperatif. La fiche attendue present-irreguliers manque.
- c10 (j'ai fini) : la fiche attendue passe-compose-avoir manque.
- c13 (passé simple d'avoir) : la fiche attendue passe-simple manque.
- c16 (pouvoir au futur) : la fiche attendue futur-simple-irreguliers manque.

Les 4 cas portent sur des conjugaisons. La recherche est nettement plus faible pour ce type de question (71 % de fiches récupérées, contre 100 % pour les règles et les pièges).

### 2. Faux refus alors que la fiche était fournie (5 cas)

- c21 (voir au futur) : la fiche ne donne que "je verrai".
- c22 (jouer à l'imparfait) : la fiche donne la règle, mais pas le verbe jouer.
- p03 (les pommes que j'ai mangées) : l'exemple exact figure dans la fiche.
- c35 (nous mangeons) : l'exemple exact figure dans la fiche.
- c19 (partir au présent) : la réponse commence par "Je ne trouve pas cette information dans mes fiches", puis donne les six formes correctes en citant present-ir.md.

Hypothèse de l'essai dev (refus quand le verbe n'apparaît pas dans les exemples) : confirmée par c21 et c22, contredite par p03 et c35. Elle n'explique qu'une partie des faux refus.

### 3. Conjugaisons ou règles incomplètes (3 cas)

- c12 (être à l'imparfait) : "J'étais" seulement.
- c14 (futur antérieur de chanter) : "J'aurai chanté" seulement.
- c29 (passé composé avec être) : formation correcte, mais l'accord avec le sujet n'est pas mentionné.

Pour c12 et c14, le prompt demande pourtant les six personnes. Même défaut que la version 1 de l'assistant (docs/assistant-v1.md).

### 4. Erreurs de fond (3 cas)

- p06 : affirme que "je chanterais" est l'imparfait (c'est le conditionnel présent). La fiche conditionnel-present n'avait pas été récupérée.
- c38 : affirme que "nous finissions" est au présent (c'est l'imparfait de l'indicatif ou le subjonctif présent).
- c40 : affirme que le COD "les fleurs" est féminin et singulier (il est au pluriel).

### 5. Réponses hors corpus avec une citation inventée (2 cas)

- c17 (vouloir au présent, cas hors corpus) : conjugaison correcte, mais attribuée à present-ir.md, qui ne contient pas vouloir.
- c31 (passé composé ou imparfait, cas hors corpus) : réponse tirée des connaissances du modèle, attribuée à plus-que-parfait.md, qui n'aborde pas ce sujet.

p06 cite aussi imparfait.md pour une affirmation fausse.

Constat principal : la présence d'une citation ne garantit pas que la réponse vient de la source citée.

## Fiabilité de la vérification par mots clés

Sur les 17 échecs, le verdict automatique correspond à mon jugement dans 16 cas. Seul désaccord : c19, compté comme faux refus alors que la réponse est correcte (mais contradictoire).

Limites de cette méthode :
- Elle ne distingue pas les causes (recherche, refus, réponse incomplète, erreur, citation inventée).
- Elle ne vérifie pas la fidélité à la source : une réponse fausse qui contient les mots clés serait comptée exacte.
- Elle détecte le refus par une phrase exacte. Une réponse qui commence par cette phrase puis répond quand même (c19) est mal classée.

## Synthèse

| Famille d'échec | Cas |
| --- | --- |
| Recherche ratée | 4 |
| Faux refus avec la fiche fournie | 5 |
| Réponse incomplète | 3 |
| Erreur de fond | 3 |
| Citation inventée sur un cas hors corpus | 2 |

Pistes pour une version 3, à mesurer avant et après :
- Améliorer la recherche pour les conjugaisons (par exemple ajouter le nom des verbes aux morceaux indexés, ou combiner recherche par sens et recherche par mots).
- Vérifier automatiquement que la fiche citée contient bien les formes ou la règle données.
- Revoir la consigne de refus, qui l'emporte parfois alors que la fiche contient la réponse.

## Limites

- Une seule exécution par cas, à température 0.
- 52 cas avec réponse attendue et 18 cas de refus : les pourcentages par catégorie reposent sur 6 à 21 cas.
- Les cas c17, c18, c20 et c31 ont été reclassés en "hors corpus" avant la mesure, après une vérification du contenu des fiches.
- La vérification par mots clés ne mesure pas la fidélité. Le juge LLM (étape 15) et l'annotation humaine (étape 16) doivent compléter cette mesure.