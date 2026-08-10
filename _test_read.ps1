$htmlPath = "c:\Users\13003\OneDrive\桌面\3333333\Agent_v2\新六系本体论_人类易懂版.html"
$content = Get-Content $htmlPath -Raw -Encoding UTF8
Write-Host "文件读取完成，长度:" $content.Length
