# Schema intake : scenario accessibilite trottoir

## Objectif
Standardiser les informations collectées lors de l'intake pour alimenter l'orchestrateur et les agents spécialisés.

## Attributs obligatoires
- `project_id` : identifiant interne unique (string).
- `client_type` : ex. `mairie`, `collectivite`, `aménageur` (string).
- `site_location` : adresse, commune, coordonnées GPS si disponibles (string).
- `project_length_m` : longueur de trottoir concernée (float, mètres).
- `existing_width_m` : largeur utile moyenne existante (float).
- `existing_slope_percent` : pente longitudinale moyenne existante (float).
- `required_min_width_m` : exigence largeur utile (float, min 1.40 m dans ce cas).
- `required_max_slope_percent` : pente maximale autorisée (float, 5 ici).
- `dwg_path` : chemin vers le fichier DWG d’état existant (string, absolu ou relatif).
- `spec_doc_refs` : liste d’URL ou chemins vers cahier des charges, normes (array string).
- `utility_networks` : réseaux secs à reprendre (array string, ex. `["eclairage", "telecom"]`).

## Attributs optionnels
- `sidewalk_material` : nature revêtement existant (string).
- `constraints_notes` : points particuliers (stationnement, arbres, acces rive) (string).
- `traffic_management_required` : boolean, besoins de circulation pendant travaux.
- `survey_accuracy_cm` : précision relevé (float).
- `reference_cost_source` : base de prix pour validation (string, ex. `BPU2024`).
- `deadline` : date butoir remise livrables (ISO 8601 string).
- `contact_person` : personne de contact mairie (string + coordonnées).

## Format de sortie proposé
```json
{
  "project_id": "ACCES-2025-001",
  "client_type": "mairie",
  "site_location": "Rue des Lilas, 75000 Paris",
  "project_length_m": 100.0,
  "existing_width_m": 1.1,
  "existing_slope_percent": 6.2,
  "required_min_width_m": 1.4,
  "required_max_slope_percent": 5.0,
  "dwg_path": "data/intake/etat_existant.dwg",
  "spec_doc_refs": [
    "data/cdc/cdc_accessibilite.pdf",
    "data/normes/catalogue_pmr.pdf"
  ],
  "utility_networks": ["eclairage", "telecom"],
  "sidewalk_material": "enrobe",
  "constraints_notes": "Acces commerces sur 30 m, arbres a proteger",
  "traffic_management_required": true,
  "survey_accuracy_cm": 2.5,
  "reference_cost_source": "BPU2024",
  "deadline": "2025-08-30",
  "contact_person": "Julie Martin, julie.martin@mairie.fr"
}
```

## Validation automatique
- Vérifier la présence de tous les attributs obligatoires.
- Contrôle de type simple (float > 0, listes non vides).
- Correspondance `project_length_m` avec le DWG (futur check géométrique).
- Alertes si `existing_width_m < required_min_width_m` ou `existing_slope_percent > required_max_slope_percent`.

## Utilisation
1. L’agent Intake parse la demande (email, formulaire, dossier) et remplit ce schema.
2. L’orchestrateur stocke l’objet dans le bus de contexte (base JSON).
3. Les agents aval consomment l’objet :
   - Analyse normative pour comparer mesures vs seuils.
   - Gestion terrain pour dimensionner le calage.
   - Charte graphique pour retrouver les ressources DWG.
   - Cout & budget pour rattacher les prix de référence.

## Question ouvertes
- Faut-il dériver automatiquement `project_id` ou le laisser renseigné manuellement ?
- Quelle granularité pour `utility_networks` (codes internes ?).
- Besoin de versionner le DWG et cahier des charges (stockage objet ?).
