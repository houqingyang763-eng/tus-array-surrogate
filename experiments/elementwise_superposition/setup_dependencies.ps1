param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
)

$external = Join-Path $RepoRoot 'external'
New-Item -ItemType Directory -Force -Path $external | Out-Null

$benchmark = Join-Path $external 'transcranial-ultrasound-benchmarks'
if (-not (Test-Path -LiteralPath $benchmark)) {
    git clone --depth 1 https://github.com/ucl-bug/transcranial-ultrasound-benchmarks.git $benchmark
}

$iso2mesh = Join-Path $external 'iso2mesh'
if (-not (Test-Path -LiteralPath $iso2mesh)) {
    git clone --depth 1 https://github.com/fangq/iso2mesh.git $iso2mesh
}

Write-Host "Dependencies ready under $external"
