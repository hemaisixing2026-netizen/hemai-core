# academic-search.ps1 — academic paper search via Semantic Scholar + arXiv
param([string]$q, [int]$n = 5)

# Semantic Scholar (free, no key)
$enc = [Uri]::EscapeDataString($q)
try {
  $r = Invoke-RestMethod -Uri "https://api.semanticscholar.org/graph/v1/paper/search?query=$enc&limit=$n&fields=title,year,url,abstract,authors" -TimeoutSec 15
  $i = 1
  foreach ($p in $r.data) {
    $authors = ($p.authors | ForEach-Object { $_.name }) -join ', '
    Write-Host "$i. $($p.title)"
    Write-Host "   $($p.year) · $authors"
    Write-Host "   $($p.url)"
    $abs = $p.abstract; if ($abs) { Write-Host "   $($abs.Substring(0, [Math]::Min(200, $abs.Length)))..." }
    Write-Host ""
    $i++
  }
  if ($i -eq 1) { Write-Host "[Semantic Scholar] 0 results" }
} catch {
  Write-Host "[Semantic Scholar] FAILED: $_"
}
