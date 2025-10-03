param(
    [string]$Message,
    [string]$RemoteName = "origin",
    [switch]$Push
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "git command not found. Install Git and rerun."
}

if (-not $Message) {
    $Message = "Auto commit " + (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
}

$changes = git status --short
if (-not $changes) {
    Write-Host "Nothing to commit. Working tree clean."
    return
}

Write-Host "Staging changes..."
git add -A | Out-Null

try {
    Write-Host "Committing with message: $Message"
    git commit -m $Message | Out-Null
} catch {
    Write-Warning $_
    Write-Warning "Commit failed."
    return
}

if ($Push) {
    $branch = git rev-parse --abbrev-ref HEAD
    if ($branch -eq "HEAD") {
        Write-Warning "Detached HEAD state. Skipping push."
        return
    }

    $remotes = git remote
    if (-not ($remotes -contains $RemoteName)) {
        Write-Warning "Remote $RemoteName not configured. Use scripts/git_setup.ps1 first."
        return
    }

    Write-Host "Pushing $branch to $RemoteName..."
    try {
        git push $RemoteName $branch
    } catch {
        Write-Warning $_
        Write-Warning "Push failed. Check credentials or remote permissions."
    }
} else {
    Write-Host "Commit created locally. Run with -Push to publish."
}
