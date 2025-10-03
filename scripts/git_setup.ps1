param(
    [string]$RepoUrl,
    [string]$RemoteName = "origin",
    [string]$BranchName = "main",
    [switch]$ForceBranchRename
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Assert-GitAvailable {
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        throw "git command not found. Install Git and rerun this script."
    }
}

function Ensure-Repository {
    if (-not (Test-Path -Path (Join-Path -Path (Get-Location) -ChildPath ".git"))) {
        Write-Host "Initializing new git repository..."
        git init | Out-Null
    }
}

function Ensure-UserConfig {
    $name = git config user.name
    $email = git config user.email
    if (-not $name) {
        Write-Warning "git user.name is not set. Configure it with: git config --global user.name \"Your Name\""
    }
    if (-not $email) {
        Write-Warning "git user.email is not set. Configure it with: git config --global user.email \"you@example.com\""
    }
}

function Ensure-Branch {
    param(
        [string]$DesiredBranch,
        [switch]$ForceRename
    )

    $currentBranch = git rev-parse --abbrev-ref HEAD
    if ($currentBranch -eq "HEAD") {
        return
    }

    if ($currentBranch -ne $DesiredBranch) {
        if ($ForceRename) {
            Write-Host "Renaming branch $currentBranch to $DesiredBranch..."
            git branch -M $DesiredBranch | Out-Null
        } else {
            Write-Host "Current branch is $currentBranch. Use -ForceBranchRename to rename to $DesiredBranch."
        }
    }
}

function Ensure-Remote {
    param(
        [string]$RemoteName,
        [string]$RemoteUrl
    )

    $existingRemote = git remote
    if ($existingRemote -contains $RemoteName) {
        $existingUrl = git remote get-url $RemoteName
        Write-Host "Remote $RemoteName already exists with URL $existingUrl"
        if ($RemoteUrl -and $existingUrl -ne $RemoteUrl) {
            Write-Host "Updating remote $RemoteName to $RemoteUrl"
            git remote set-url $RemoteName $RemoteUrl | Out-Null
        }
    } elseif ($RemoteUrl) {
        Write-Host "Adding remote $RemoteName -> $RemoteUrl"
        git remote add $RemoteName $RemoteUrl | Out-Null
    } else {
        Write-Warning "Remote $RemoteName is missing. Provide -RepoUrl to create it."
    }
}

function Push-InitialCommit {
    param(
        [string]$RemoteName,
        [string]$BranchName
    )

    $branch = git rev-parse --abbrev-ref HEAD
    if ($branch -eq "HEAD") {
        Write-Warning "No branch found to push. Create a commit first."
        return
    }

    Write-Host "Pushing branch $branch to $RemoteName..."
    git push -u $RemoteName $branch
}

Assert-GitAvailable
Ensure-Repository
Ensure-UserConfig
Ensure-Branch -DesiredBranch $BranchName -ForceRename:$ForceBranchRename

if (-not $RepoUrl) {
    $RepoUrl = Read-Host -Prompt "Enter remote repository URL (leave blank to skip)"
}

Ensure-Remote -RemoteName $RemoteName -RemoteUrl $RepoUrl

if ($RepoUrl) {
    try {
        Push-InitialCommit -RemoteName $RemoteName -BranchName $BranchName
    } catch {
        Write-Warning $_
        Write-Warning "Push failed. Ensure credentials are configured (Personal Access Token or SSH key)."
    }
} else {
    Write-Host "Setup complete. Remote not configured because no URL was provided."
}
