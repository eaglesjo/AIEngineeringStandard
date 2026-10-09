param(
    [string]$RepositoryRoot = (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
)

$ErrorActionPreference = "Stop"
$Installer = Join-Path $RepositoryRoot "scripts/installers/install-domains.ps1"
if (-not (Test-Path -LiteralPath $Installer)) { throw "Installer not found: $Installer" }

$tokens = $null; $errors = $null
[System.Management.Automation.Language.Parser]::ParseFile($Installer, [ref]$tokens, [ref]$errors) | Out-Null
if ($errors.Count -gt 0) { $errors | Format-List | Out-String | Write-Error; throw "PowerShell syntax validation failed" }

$root = Join-Path $env:RUNNER_TEMP ("codingstandard-windows-{0}" -f [guid]::NewGuid().ToString("N")); New-Item -ItemType Directory -Force -Path $root | Out-Null
function Invoke-Installer {
    param([string]$Target,[string]$Language,[ValidateSet("common", "ml", "llm", "vision", "colab", "all")][string]$Domain,[ValidateSet("Ask", "Merge", "Overwrite", "Skip")][string]$ConflictAction = "Overwrite",[switch]$DryRun)
    $arguments = @{Target=$Target; Language=$Language; Domain=$Domain; ConflictAction=$ConflictAction}; if ($DryRun) { $arguments.DryRun=$true }; & $Installer @arguments
}
try {
    foreach ($language in @("en", "ko")) {
        foreach ($domain in @("common", "ml", "llm", "vision", "colab", "all")) {
            $target = Join-Path $root "$language-$domain"; New-Item -ItemType Directory -Force -Path $target | Out-Null
            Invoke-Installer -Target $target -Language $language -Domain $domain
            if (-not (Test-Path (Join-Path $target "AGENTS.md"))) { throw "AGENTS.md missing: $language/$domain" }
            if ($domain -in @("ml", "all") -and -not (Test-Path (Join-Path $target "domains/ml/AGENT.md"))) { throw "domains/ml/AGENT.md missing: $language/$domain" }
            if ($domain -in @("llm", "all") -and -not (Test-Path (Join-Path $target "domains/llm/AGENT.md"))) { throw "domains/llm/AGENT.md missing: $language/$domain" }
            if ($domain -in @("vision", "all") -and -not (Test-Path (Join-Path $target "domains/vision/AGENT.md"))) { throw "domains/vision/AGENT.md missing: $language/$domain" }
            if ($domain -in @("colab", "all") -and -not (Test-Path (Join-Path $target "platform/colab/AGENT.md"))) { throw "platform/colab/AGENT.md missing: $language/$domain" }
            if ($domain -eq "common" -and (Test-Path (Join-Path $target "domains/ml/AGENT.md"))) { throw "Common-only install unexpectedly contains ML domain" }
            if ($domain -eq "common" -and (Test-Path (Join-Path $target "domains/llm/AGENT.md"))) { throw "Common-only install unexpectedly contains LLM domain" }
            if ($domain -eq "common" -and (Test-Path (Join-Path $target "domains/vision/AGENT.md"))) { throw "Common-only install unexpectedly contains Vision domain" }
            if ($domain -eq "common" -and (Test-Path (Join-Path $target "platform/colab/AGENT.md"))) { throw "Common-only install unexpectedly contains Colab policy" }
            if ($domain -eq "ml" -and (Test-Path (Join-Path $target "domains/llm/AGENT.md"))) { throw "ML-only install unexpectedly contains LLM domain" }
            if ($domain -eq "llm" -and (Test-Path (Join-Path $target "domains/vision/AGENT.md"))) { throw "LLM-only install unexpectedly contains Vision domain" }
            if ($domain -eq "vision" -and (Test-Path (Join-Path $target "domains/llm/AGENT.md"))) { throw "Vision-only install unexpectedly contains LLM domain" }
        }
    }
    $dryTarget = Join-Path $root "dry-run"; New-Item -ItemType Directory -Force -Path $dryTarget | Out-Null; Invoke-Installer -Target $dryTarget -Language ko -Domain all -DryRun
    if (Get-ChildItem -Force -LiteralPath $dryTarget) { throw "Dry-run modified the target" }
    $mergeTarget = Join-Path $root "merge"; New-Item -ItemType Directory -Force -Path $mergeTarget | Out-Null
    $agents = Join-Path $mergeTarget "AGENTS.md"
    Set-Content -LiteralPath $agents -Value @("# Local rule","","<!-- BEGIN CODINGSTANDARD MANAGED BLOCK -->","old managed content","<!-- END CODINGSTANDARD MANAGED BLOCK -->") -Encoding utf8
    Invoke-Installer -Target $mergeTarget -Language en -Domain common -ConflictAction Merge
    $merged = Get-Content -Raw -LiteralPath $agents
    if ($merged -notmatch "# Local rule") { throw "Merge did not preserve local content" }
    if ($merged -match "(?m)^old managed content$") { throw "Merge did not replace managed block" }
    $spaceTarget = Join-Path $root "한국어 공백 경로"; New-Item -ItemType Directory -Force -Path $spaceTarget | Out-Null; Invoke-Installer -Target $spaceTarget -Language ko -Domain ml
    if (-not (Test-Path (Join-Path $spaceTarget "domains/ml/AGENT.md"))) { throw "Installation failed in Unicode/space path" }
    Write-Host "Windows installer tests passed."
} finally { Remove-Item -Recurse -Force -ErrorAction SilentlyContinue $root }