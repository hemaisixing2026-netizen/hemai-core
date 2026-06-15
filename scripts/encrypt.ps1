# 数据加密脚本
# 用法：.\encrypt.ps1 -Action encrypt|decrypt -File <路径> [-Key <密钥>]

param([string]$Action, [string]$File, [string]$Key)

$keyFile = "$PSScriptRoot\..\.encryption-key"
if(-not $Key) {
    if(Test-Path $keyFile) { $Key = Get-Content $keyFile -Raw }
    else { Write-Host "[首次运行] 请输入加密密码:" -ForegroundColor Yellow; $Key = Read-Host -AsSecureString; $Key = [System.Net.NetworkCredential]::new('',$Key).Password }
}

$salt = [Text.Encoding]::UTF8.GetBytes("openclaw-salt-2026")
$derive = New-Object Security.Cryptography.Rfc2898DeriveBytes($Key, $salt, 10000, [Security.Cryptography.HashAlgorithmName]::SHA256)
$keyBytes = $derive.GetBytes(32)
$ivBytes = $derive.GetBytes(16)

if($Action -eq "encrypt") {
    $data = Get-Content $File -Raw -Encoding UTF8
    $aes = [Security.Cryptography.Aes]::Create(); $aes.Key = $keyBytes; $aes.IV = $ivBytes
    $encryptor = $aes.CreateEncryptor()
    $ms = New-Object IO.MemoryStream; $cs = New-Object Security.Cryptography.CryptoStream($ms, $encryptor, [Security.Cryptography.CryptoStreamMode]::Write)
    $sw = New-Object IO.StreamWriter($cs); $sw.Write($data); $sw.Close()
    [IO.File]::WriteAllBytes("$File.aes", $ms.ToArray())
    Write-Host "✅ 已加密: $File.aes"
}
elseif($Action -eq "decrypt") {
    $data = [IO.File]::ReadAllBytes($File)
    $aes = [Security.Cryptography.Aes]::Create(); $aes.Key = $keyBytes; $aes.IV = $ivBytes
    $decryptor = $aes.CreateDecryptor()
    $ms = New-Object IO.MemoryStream($data); $cs = New-Object Security.Cryptography.CryptoStream($ms, $decryptor, [Security.Cryptography.CryptoStreamMode]::Read)
    $sr = New-Object IO.StreamReader($cs); $plain = $sr.ReadToEnd()
    Write-Host "✅ 解密内容:"; Write-Host $plain
}
else { Write-Host "用法: .\encrypt.ps1 -Action encrypt|decrypt -File <路径> [-Key <密钥>]" }
