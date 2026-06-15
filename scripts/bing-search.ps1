# bing-search.ps1 — web search via Bing through proxy
param([string]$q, [int]$n = 5)
$enc = [Uri]::EscapeDataString($q)
$html = Invoke-RestMethod -Uri "https://www.bing.com/search?q=$enc&count=$n&mkt=en-US&setlang=en" `
  -Headers @{"User-Agent"="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"; "Accept-Language"="en-US,en;q=0.9"} `
  -TimeoutSec 15

$pattern = '<li class="b_algo"[^>]*>(.+?)</li>'
$blocks = [regex]::Matches($html, $pattern, 'Singleline')
$i = 0

foreach ($b in $blocks) {
  if ($i -ge $n) { break }
  $block = $b.Groups[1].Value
  $title = ''; $url = ''; $desc = ''
  if ($block -match '<a\s+(?:[^>]*?\s+)?href="([^"]+)"[^>]*>(.+?)</a>') { 
    $url = $matches[1]; $title = $matches[2] -replace '<[^>]+>','' -replace '\s+',' '
  }
  if ($block -match '<p[^>]*>(.+?)</p>') { 
    $desc = $matches[1] -replace '<[^>]+>','' -replace '\s+',' ' 
  }
  if ($title -and $url) {
    $i++
    Write-Host "$i. $title"
    Write-Host "   $url"
    if ($desc) { Write-Host "   $desc" }
    Write-Host ""
  }
}
if ($i -eq 0) { Write-Host "[bing-search] 0 results" }
