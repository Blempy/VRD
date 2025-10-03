# Fiche scenario : Mise aux normes accessibilite trottoir

## Vue d'ensemble
- Contexte : la mairie mandate une mise aux normes PMR d'un trottoir de 100 m avec reprise des reseaux secs (eclairage public, telecom).
- Objectif : livrer un plan projete, un rapport de conformite accessibilite et une estimation budgetaire rapide.
- Hypothese : donnees topographiques simplifiees suffisantes pour le calage ; eventuels complements releves a planifier s'ils manquent.

## Donnees d'entree
- Plan DWG de l'etat existant (leve topo simplifie).
- Cahier des charges simplifie : pente longitudinale maximale 5 %, largeur utile minimale 1.40 m.
- Catalogue des normes accessibilite (references PMR nationales + prescriptions locales le cas echeant).
- Parametres chantier additionnels a collecter : localisation, contraintes de circulation, materiaux existants.

## Agents et roles
- Intake & contexte : lit la demande, extrait les contraintes, prepare un resume structure pour les agents aval.
- Analyse normative : verifie les pentes et largeurs existantes/projet contre le referentiel accessibilite ; signale les ecarts.
- Gestion terrain & calage : propose les ajustements en plan et profil pour respecter les normes tout en gerant les reseaux secs.
- Charte graphique : genere les calques, styles et annotations du plan projete (DWG + export PDF normalise).
- Cout & budget : produit une estimation rapide (unitaire ou par metre lineaire) avec ventilation par poste.
- QA & livrables : assemble le dossier, controle coherence, prepare le rapport de conformite et les exports finaux.

## Flux cible
1. Intake recupere les entrees (DWG, cahier des charges, normes) et cree un paquet de contexte.
2. Orchestrateur declenche l'analyse normative sur l'etat existant, identifie les non-conformites.
3. Gestion terrain produit une proposition de calage respectant largeur/pente et gere les interferences reseaux.
4. Charte graphique applique la charte (calques, legende) et genere DWG projete + PDF.
5. Cout & budget estime les travaux (demolition, fourniture/pose, reseaux, finitions).
6. QA & livrables compile un rapport de conformite et verifie les seuils de validation.

## Monitoring requis
- Traces : ID unique par requete, suivi des appels agents, latence, tokens, version de prompt.
- Logs reasoning : stockage chiffre des etapes de reflexion cles pour revue ponctuelle.
- Metriques qualite : nombre d'ecarts normatifs detectes/corriges, % sections conformes, derive cout estime vs reference.
- Alertes : depassement latence (>60 s), cout tokens inhabituel, incoherences detectees par QA.
- Feedback : capture retour utilisateur sur livrable et facilite d'usage.

## Livrables
- Plan DWG projete conforme a la charte + PDF pret a l'impression.
- Rapport de conformite accessibilite (sections : exigences, controles, ecarts, actions correctives).
- Estimation budgetaire simplifiee, format tableau (poste, quantite, prix unitaire, montant).

## Criteres de validation
- Largeurs et pentes projet respectent le cahier des charges et normes PMR.
- Estimation budgetaire : ecart < 10 % vs estimation manuelle de reference.
- Livrables generes sans erreurs bloquantes de calque/notation.
- Temps de traitement cible < 5 min avec 95 % de confiance.

## Ouvertures / questions
- Quelle granularite du catalogue normes (national + communal) et mode de mise a jour ?
- Besoin d'integration directe avec logiciel DAO existant (Civil 3D, Covadis) ou generation DWG suffit-elle ?
- Peut-on disposer de chiffrages unitaires de reference (base interne, BPU, bordereaux publics) ?
- Processus de revue humaine : a quel moment la validation terrain doit intervenir ?

## Prochaines etapes suggerees
1. Rassembler les documents exemples (DWG, cahier des charges, referentiel normes).
2. Definir les attributs de contexte a extraire automatiquement lors de l'intake.
3. Prototyper l'agent Analyse normative avec un petit jeu de donnees test.
4. Mettre en place le squelette d'orchestrateur instrumente (traces + metriques de base).
