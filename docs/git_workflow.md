# Git workflow automatise

Ce dossier contient deux scripts PowerShell pour simplifier la mise en place et la synchronisation du depot Git.

## Prerequis
- Git installe et disponible dans le PATH.
- Compte GitHub avec un depot distant vide ou existant.
- Identifiants configures (PAT HTTPS ou cle SSH). Pour stocker un PAT de maniere securisee :
  - `git config --global credential.helper manager-core` sur Windows pour utiliser le gestionnaire d'identifiants.
  - Alternativement generer une cle SSH (`ssh-keygen`) et l'ajouter a GitHub.
- Renseigner votre nom et email git :
  - `git config --global user.name "Votre Nom"`
  - `git config --global user.email "vous@example.com"`

## 1. Initialiser et connecter le depot
Utilisez le script `scripts/git_setup.ps1` pour creer le depot local (si necessaire), configurer la branche principale et ajouter le remote.

```powershell
pwsh -File scripts/git_setup.ps1 -RepoUrl "https://github.com/votre-compte/votre-repo.git" -BranchName main -ForceBranchRename
```

Le script :
- Verifie la disponibilite de git.
- Initie le depot si `.git` est absent.
- Renomme la branche courante en `main` lorsque `-ForceBranchRename` est fourni.
- Ajoute ou met a jour le remote `origin` vers l'URL fournie.
- Tente un `git push -u origin main` et avertit si les identifiants ne sont pas configures.

Pour une URL SSH :
```powershell
pwsh -File scripts/git_setup.ps1 -RepoUrl "git@github.com:votre-compte/votre-repo.git" -BranchName main -ForceBranchRename
```

## 2. Synchroniser les modifications
Le script `scripts/git_sync.ps1` automatise l'ajout, le commit et le push optionnel.

```powershell
# Commit local uniquement
pwsh -File scripts/git_sync.ps1 -Message "Ajout module analyse normative"

# Commit + push
pwsh -File scripts/git_sync.ps1 -Message "Mise a jour scenario" -Push
```

Fonctionnement :
- Arrete si aucun changement n'est detecte.
- `git add -A`, `git commit -m "..."`.
- Si `-Push` est present, poussee vers le remote `origin` (parametrable via `-RemoteName`).

## Conseils pratiques
- Utiliser des messages de commit explicites pour faciliter l'historique.
- Lancer `git status` regulierement pour verifier l'etat avant de pousser.
- Ajouter des verifications supplementaires si vous souhaitez exclure certains fichiers (adapter `.gitignore`).
- Pour automatiser davantage, creer un alias PowerShell :
  - `Set-Alias gs "pwsh -File $PWD\scripts\git_sync.ps1"`

## Resolution des problemes
- **Authentification** : si le push echoue, verifier que le PAT a l'autorisation `repo` et que le gestionnaire d'identifiants Git stocke correctement le mot de passe.
- **Conflits** : si GitHub contient deja des commits, effectuer un `git pull --rebase origin main` pour recuperer les modifications avant de pousser.
- **BranchName** : le script ne renomme pas automatiquement la branche si `-ForceBranchRename` est omis. L'utiliser la premiere fois pour harmoniser avec GitHub.

Avec ces scripts, la boucle standard devient :
1. Modifier les fichiers.
2. `pwsh -File scripts/git_sync.ps1 -Message "Votre message" -Push`
3. Les changements sont publies sur GitHub sans avoir a taper les commandes git manuellement.
