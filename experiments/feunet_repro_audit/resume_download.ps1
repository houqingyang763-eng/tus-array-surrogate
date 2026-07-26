param(
    [int]$RetryDelaySeconds = 10,
    [string]$ArtifactDir = 'D:\tus-array-surrogate-experiments\feunet_repro_audit\artifact'
)

$ErrorActionPreference = 'Stop'

$artifactDir = $ArtifactDir
$outputPath = Join-Path $artifactDir 'JASACode.rar'
$statePath = Join-Path $artifactDir 'download-state.log'
$ariaLogPath = Join-Path $artifactDir 'aria2.log'
$completePath = Join-Path $artifactDir 'DOWNLOAD_COMPLETE.txt'
$url = 'https://ndownloader.figshare.com/files/44328011'
$expectedBytes = 16087955914L
$expectedMd5 = '0b737a28fbbb2843eb63ee07c78fd302'

New-Item -ItemType Directory -Force $artifactDir | Out-Null

function Write-State {
    param([string]$Message)
    $line = '{0:u} {1}' -f (Get-Date), $Message
    $line | Tee-Object -FilePath $statePath -Append
}

$aria = Get-Command aria2c -ErrorAction SilentlyContinue
if ($aria) {
    $ariaPath = $aria.Source
} else {
    $ariaPath = Get-ChildItem `
        (Join-Path $env:LOCALAPPDATA 'Microsoft\WinGet\Packages') `
        -Recurse -Filter 'aria2c.exe' -ErrorAction SilentlyContinue |
        Select-Object -First 1 -ExpandProperty FullName
}

if (-not $ariaPath -or -not (Test-Path $ariaPath)) {
    throw 'aria2c.exe was not found. Install aria2 before running this script.'
}

Remove-Item $completePath -Force -ErrorAction SilentlyContinue
$stalledAttempts = 0

while ($true) {
    $beforeBytes = if (Test-Path $outputPath) {
        (Get-Item $outputPath).Length
    } else {
        0L
    }

    if ($beforeBytes -eq $expectedBytes) {
        break
    }
    if ($beforeBytes -gt $expectedBytes) {
        throw "Archive is larger than expected: $beforeBytes > $expectedBytes bytes."
    }

    $percent = 100.0 * $beforeBytes / $expectedBytes
    Write-State ("Starting fresh signed-URL attempt at {0:N2}% ({1} bytes)." -f $percent, $beforeBytes)

    $ariaArgs = @(
        '--continue=true'
        '--max-connection-per-server=1'
        '--split=1'
        '--file-allocation=none'
        '--auto-file-renaming=false'
        '--allow-overwrite=true'
        '--max-tries=3'
        '--retry-wait=5'
        '--connect-timeout=30'
        '--timeout=60'
        '--lowest-speed-limit=128K'
        '--summary-interval=30'
        '--console-log-level=notice'
        "--dir=$artifactDir"
        '--out=JASACode.rar'
        $url
    )

    & $ariaPath @ariaArgs 2>&1 | Out-File $ariaLogPath -Append -Encoding utf8
    $ariaExit = $LASTEXITCODE

    $afterBytes = if (Test-Path $outputPath) {
        (Get-Item $outputPath).Length
    } else {
        0L
    }
    $gainedBytes = $afterBytes - $beforeBytes
    Write-State "aria2 exited with code $ariaExit; gained $gainedBytes bytes."

    if ($afterBytes -eq $expectedBytes) {
        break
    }

    if ($gainedBytes -le 0) {
        $stalledAttempts++
        $delay = [Math]::Min(120, $RetryDelaySeconds * $stalledAttempts)
    } else {
        $stalledAttempts = 0
        $delay = $RetryDelaySeconds
    }
    Write-State "Retrying with a new Figshare signed URL in $delay seconds."
    Start-Sleep -Seconds $delay
}

Write-State 'Expected byte count reached. Computing MD5.'
$actualMd5 = (Get-FileHash $outputPath -Algorithm MD5).Hash.ToLowerInvariant()
if ($actualMd5 -ne $expectedMd5) {
    Write-State "MD5 FAILED: expected $expectedMd5; actual $actualMd5."
    throw 'Download reached the expected size but failed the official Figshare MD5 check.'
}

$completion = @(
    'JASACode_FEUNet download verified.'
    "bytes=$expectedBytes"
    "md5=$actualMd5"
    ('completed_utc={0:u}' -f (Get-Date).ToUniversalTime())
)
$completion | Set-Content $completePath -Encoding ascii
Write-State 'DOWNLOAD COMPLETE: size and official Figshare MD5 both match.'
