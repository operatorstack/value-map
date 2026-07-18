param(
  [Parameter(Mandatory = $true)]
  [ValidateSet("codex", "cursor", "claude")]
  [string]$HostName,
  [string]$Repo = (Get-Location).Path,
  [string]$Version = "latest"
)

$ErrorActionPreference = "Stop"
$repository = "operator-stack/value-map"
$base = if ($Version -eq "latest") {
  "https://github.com/$repository/releases/latest/download"
} else {
  "https://github.com/$repository/releases/download/$Version"
}

$temporary = Join-Path ([System.IO.Path]::GetTempPath()) ("value-map-" + [guid]::NewGuid())
New-Item -ItemType Directory -Path $temporary | Out-Null
try {
  $skill = Join-Path $temporary "value-map-SKILL.md"
  $checksum = Join-Path $temporary "value-map-SKILL.md.sha256"
  Invoke-WebRequest "$base/value-map-SKILL.md" -OutFile $skill
  Invoke-WebRequest "$base/value-map-SKILL.md.sha256" -OutFile $checksum
  $expected = ((Get-Content $checksum -Raw).Trim() -split "\s+")[0].ToLowerInvariant()
  $actual = (Get-FileHash $skill -Algorithm SHA256).Hash.ToLowerInvariant()
  if ($expected -ne $actual) { throw "Value Map checksum mismatch" }

  switch ($HostName) {
    "codex" {
      $codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }
      $destination = Join-Path $codexHome "skills/value-map/SKILL.md"
    }
    "claude" { $destination = Join-Path $HOME ".claude/skills/value-map/SKILL.md" }
    "cursor" {
      if (-not (Test-Path $Repo -PathType Container)) { throw "Cursor repository does not exist: $Repo" }
      $destination = Join-Path $Repo ".cursor/commands/value-map.md"
    }
  }

  New-Item -ItemType Directory -Force -Path (Split-Path $destination) | Out-Null
  Copy-Item $skill $destination -Force
  Write-Host "Installed Value Map for $HostName at $destination"
} finally {
  Remove-Item $temporary -Recurse -Force -ErrorAction SilentlyContinue
}
