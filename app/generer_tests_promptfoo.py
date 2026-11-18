import json
from pathlib import Path

lignes = Path("evals/dataset.jsonl").read_text(encoding="utf-8").splitlines()
cas_liste = [json.loads(l) for l in lignes if l.strip()]
REFUS = "je ne trouve pas cette information"

tests = []
for cas in cas_liste:
    if cas["usage"] != "dev":
        continue
    if cas["reponse_attendue"] == "REFUS":
        assertions = [{"type": "icontains", "value": REFUS}]
    else:
        assertions = [{"type": "icontains", "value": m} for m in cas["mots_cles"]]
        assertions.append({"type": "not-icontains", "value": REFUS})
    tests.append({
        "description": f"{cas['id']} ({cas['categorie']})",
        "vars": {"question": cas["question"]},
        "assert": assertions,
    })

sortie = Path("evals/promptfoo_tests_dev.json")
sortie.write_text(json.dumps(tests, ensure_ascii=False, indent=2), encoding="utf-8")
print(len(tests), "tests écrits dans", sortie)