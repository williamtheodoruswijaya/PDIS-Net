param(
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$DemoRoot = Split-Path -Parent $PSScriptRoot
$RepoRoot = $DemoRoot
while ($RepoRoot -and -not (Test-Path (Join-Path $RepoRoot "model"))) {
    $Parent = Split-Path -Parent $RepoRoot
    if ($Parent -eq $RepoRoot) {
        throw "Could not find repository root containing a model directory."
    }
    $RepoRoot = $Parent
}
$ModelsRoot = Join-Path $DemoRoot "models"

$Links = @(
    @{
        Name = "segformer"
        Target = Join-Path $RepoRoot "model\20261205 - Segformer (mIoU=0.81)"
    },
    @{
        Name = "dinov3"
        Target = Join-Path $RepoRoot "model\20261305 - DinoV3 (mIoU=0.7916)"
    }
)

New-Item -ItemType Directory -Path $ModelsRoot -Force | Out-Null

foreach ($Link in $Links) {
    $LinkPath = Join-Path $ModelsRoot $Link.Name
    $TargetPath = Resolve-Path $Link.Target

    if (Test-Path $LinkPath) {
        if (-not $Force) {
            Write-Host "Exists: $LinkPath"
            continue
        }
        Remove-Item -LiteralPath $LinkPath -Force
    }

    New-Item -ItemType Junction -Path $LinkPath -Target $TargetPath | Out-Null
    Write-Host "Linked $LinkPath -> $TargetPath"
}
