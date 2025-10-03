# Agent Analyse normative : scenario trottoir accessibilite

## Objectif
Identifier les non-conformites d'accessibilite (largeur, pente) a partir des donnees issues de l'intake et des mesures DWG/terrain, puis proposer des actions correctives a transmettre aux autres agents.

## Entrees
- `intake_payload` (JSON conforme au schema intake).
- `measurements` : tableau des sections mesurees (voir format ci-dessous).
- `norm_catalog` : references de normes (extraits numerises) pour citations.

### Format `measurements`
```json
[
  {
    "chainage_m": 0,
    "segment_length_m": 5,
    "width_m": 1.05,
    "longitudinal_slope_percent": 6.5,
    "transversal_slope_percent": 2.0,
    "notes": "Presence chambre telecom"
  },
  {
    "chainage_m": 5,
    "segment_length_m": 10,
    "width_m": 1.45,
    "longitudinal_slope_percent": 4.2,
    "transversal_slope_percent": 1.8
  }
]
```

## Sortie attendue
```json
{
  "summary": "2 non-conformites identifiees : largeur < 1.40 m sur 20 m, pente > 5% sur 8 m.",
  "non_compliance": [
    {
      "type": "width",
      "chainage_start_m": 0,
      "chainage_end_m": 20,
      "measured_value": 1.05,
      "required_min": 1.40,
      "severity": "high",
      "norm_reference": "Guide accessibilite 2023, section 2.1"
    },
    {
      "type": "longitudinal_slope",
      "chainage_start_m": 12,
      "chainage_end_m": 20,
      "measured_value": 6.2,
      "required_max": 5.0,
      "severity": "medium",
      "norm_reference": "Guide accessibilite 2023, section 2.3"
    }
  ],
  "recommendations": [
    "Elargir le trottoir sur les chainages 0-20 m (objectif 1.50 m pour marge).",
    "Reprofiler la pente 12-20 m pour atteindre 4.5% maximum (coordination reseaux)."
  ],
  "quality_checks": {
    "intake_crosscheck": true,
    "data_gaps": []
  }
}
```

## Prompt de base (pseudo)
```
SYSTEM: Tu es l'agent Analyse normative. Tu verifie la conformite PMR des trottoirs.
        Tu produis un JSON valide respectant la structure definie.
INPUT:
- Resume intake : ${intake_payload}
- Mesures : ${measurements}
- Normes : ${norm_catalog}
TASK:
1. Comparer chaque segment aux seuils largeur/pentes.
2. Lister les non-conformites avec chainages et references normatives.
3. Proposer des recommandations concises.
4. Signaler les donnees manquantes.
OUTPUT: JSON structure ci-dessus. Pas de texte hors JSON.
```

## Regles de decision
- `severity` :
  - `high` si ecart > 10 % ou bloque la conformite totale.
  - `medium` si ecart 5-10 %.
  - `low` si ecart marginal < 5 % mais a surveiller.
- Si `measurements` est vide : signaler erreur dans `data_gaps`.
- Si valeurs `width_m` / `longitudinal_slope_percent` manquantes : mentionner dans `data_gaps` et ne pas generer de recommandation approximative.

## Monitoring specifique
- Stats : nombre de segments analyses, nombre de non-conformites, severite moyenne.
- Vérifier tokens, latence, ratio non-conformites detectees vs segments.
- Alerte si `non_compliance` vide alors que des ecarts sont attendus (c.f. tests synthétiques).

## Jeu de test minimal
- `tests/normative_agent/test_case_001.json` : scenario ok (aucune non-conformite) => `non_compliance` vide.
- `tests/normative_agent/test_case_002.json` : largeur insuffisante sur 10 m.
- `tests/normative_agent/test_case_003.json` : pente excessive + donnees manquantes.

## Questions ouvertes
- Faut-il verifier d'autres criteres PMR (bandes podotactiles, abord de traverses) ?
- Integration avec mesures reeles issues d'un script (extraction auto du DWG) : format a preciser.
- Processus de validation humaine : revue systematique ou par echantillonnage ?
## Execution & tests
- Lancer un test unitaire : `python src/run_normative_agent.py tests/normative_agent/test_case_001.json --pretty`.
- Executer toute la suite : `pwsh -File scripts/run_tests.ps1` (option `-Pretty` pour affichege lisible).
