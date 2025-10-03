param(
    [string]$PythonExe = "python",
    [switch]$Pretty
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if (-not (Get-Command $PythonExe -ErrorAction SilentlyContinue)) {
    throw "Python executable '$PythonExe' introuvable. Precisez le chemin avec -PythonExe."
}

$projectRoot = Split-Path -Path $PSScriptRoot -Parent
$runner = Join-Path $projectRoot "src/run_normative_agent.py"
if (-not (Test-Path $runner)) {
    throw "Script d'execution introuvable: $runner"
}

$testsRoot = Join-Path $projectRoot "tests/normative_agent"
if (-not (Test-Path $testsRoot)) {
    throw "Dossier de tests introuvable: $testsRoot"
}

$testFiles = Get-ChildItem -Path $testsRoot -Filter "*.json" | Sort-Object Name
if (-not $testFiles) {
    Write-Warning "Aucun fichier de test trouve dans $testsRoot"
    return
}

$failures = 0
foreach ($test in $testFiles) {
    Write-Host "[RUN] $($test.Name)" -ForegroundColor Cyan
    $args = @($runner, $test.FullName)
    if ($Pretty) {
        $args += "--pretty"
    }
    try {
        & $PythonExe @args
    } catch {
        Write-Error "Execution echouee pour $($test.Name): $_"
        $failures++
    }
}

if ($failures -gt 0) {
    throw "$failures test(s) en echec."
} else {
    Write-Host "Tous les tests ont reussi." -ForegroundColor Green
}
