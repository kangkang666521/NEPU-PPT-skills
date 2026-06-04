param(
  [Parameter(Mandatory = $true)][string]$InputPptx,
  [string]$OutputPptx = "",
  [ValidateSet("auto", "powerpoint", "wps")][string]$Engine = "auto",
  [switch]$ValidateOnly,
  [switch]$Visible
)

$ErrorActionPreference = "Stop"

function New-OfficeApp {
  param([string]$ProgId)
  try {
    return New-Object -ComObject $ProgId
  } catch {
    return $null
  }
}

function Close-ComObject {
  param($Object)
  if ($null -ne $Object) {
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($Object) | Out-Null
  }
}

function Test-PresentationWithApp {
  param(
    [string]$ProgId,
    [string]$Name,
    [string]$InputPath,
    [string]$Output,
    [bool]$DoSave,
    [bool]$VisibleApp
  )
  $app = $null
  $pres = $null
  try {
    $app = New-OfficeApp -ProgId $ProgId
    if ($null -eq $app) {
      return [pscustomobject]@{ engine = $Name; ok = $false; error = "COM ProgID unavailable"; slides = 0; output = $null }
    }
    try { $app.Visible = $(if ($VisibleApp) { -1 } else { 0 }) } catch {}
    $pres = $app.Presentations.Open($InputPath)
    $slides = $pres.Slides.Count
    if ($DoSave) {
      $outDir = Split-Path -Parent $Output
      if ($outDir) { New-Item -ItemType Directory -Force -Path $outDir | Out-Null }
      try {
        # PowerPoint and WPS both use 24 for Open XML presentation in the PowerPoint object model.
        $pres.SaveAs($Output, 24)
      } catch {
        $pres.SaveAs($Output)
      }
      if (Test-Path -LiteralPath $Output) {
        Set-ItemProperty -LiteralPath $Output -Name IsReadOnly -Value $false -ErrorAction SilentlyContinue
        Unblock-File -LiteralPath $Output -ErrorAction SilentlyContinue
      }
      $saved = $Output
    } else {
      $saved = $null
    }
    $pres.Close()
    Close-ComObject $pres
    $pres = $null
    return [pscustomobject]@{ engine = $Name; ok = $true; error = $null; slides = $slides; output = $saved }
  } catch {
    return [pscustomobject]@{ engine = $Name; ok = $false; error = $_.Exception.Message; slides = 0; output = $null }
  } finally {
    if ($null -ne $pres) {
      try { $pres.Close() } catch {}
      Close-ComObject $pres
    }
    if ($null -ne $app) {
      try { $app.Quit() } catch {}
      Close-ComObject $app
    }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
  }
}

$resolvedInput = (Resolve-Path -LiteralPath $InputPptx).Path
$resolvedOutput = ""
if (-not $ValidateOnly) {
  if ([string]::IsNullOrWhiteSpace($OutputPptx)) {
    throw "OutputPptx is required unless -ValidateOnly is used. In-place saves are disabled."
  }
  $resolvedOutput = [System.IO.Path]::GetFullPath($OutputPptx)
  if ($resolvedOutput -eq $resolvedInput) {
    throw "OutputPptx must differ from InputPptx. In-place saves are disabled."
  }
  if (Test-Path -LiteralPath $resolvedOutput) {
    throw "Output already exists: $resolvedOutput. Use a new versioned path."
  }
}

$engines = @()
if ($Engine -eq "powerpoint" -or $Engine -eq "auto") {
  $engines += @{ progid = "PowerPoint.Application"; name = "powerpoint" }
}
if ($Engine -eq "wps" -or $Engine -eq "auto") {
  $engines += @{ progid = "KWPP.Application"; name = "wps" }
}

$results = @()
foreach ($engineInfo in $engines) {
  $result = Test-PresentationWithApp `
    -ProgId $engineInfo.progid `
    -Name $engineInfo.name `
    -InputPath $resolvedInput `
    -Output $resolvedOutput `
    -DoSave (-not $ValidateOnly) `
    -VisibleApp ([bool]$Visible)
  $results += $result
  if ($result.ok) { break }
}

$results | ConvertTo-Json -Depth 4
if (-not ($results | Where-Object { $_.ok } | Select-Object -First 1)) {
  exit 1
}
