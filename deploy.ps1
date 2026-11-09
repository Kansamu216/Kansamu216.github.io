# 一键发布到 GitHub Pages（gh-pages 分支）
# 用法：在 my-blog 目录下执行  powershell -ExecutionPolicy Bypass -File .\deploy.ps1
$ErrorActionPreference = "Stop"
$env:GIT_TERMINAL_PROMPT = "0"

# 让 node 可用（优先用 DSH 自带 node，其次用系统 PATH 里的 node）
$dshNode = "C:\Users\26703\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\node\bin\node.exe"
if (Test-Path $dshNode) {
  $node = $dshNode
} elseif (Get-Command node -ErrorAction SilentlyContinue) {
  $node = "node"
} else {
  throw "找不到 node，请先安装 Node.js 或确保 node 在 PATH 中"
}

$repo = "Kansamu216/Kansamu216.github.io"

Write-Host "==> 清理并生成静态文件"
& $node "node_modules\hexo\bin\hexo" clean | Out-Null
& $node "node_modules\hexo\bin\hexo" generate

# 让 GitHub Pages 按静态文件原样提供，不做 Jekyll 处理
New-Item -ItemType File -Force -Path "public\.nojekyll" | Out-Null

Write-Host "==> 推送到 gh-pages 分支"
Push-Location "public"
try {
  if (Test-Path ".git") { Remove-Item -Recurse -Force ".git" }
  git init -b gh-pages | Out-Null
  git add -A
  git -c user.name="Kansamu216" -c user.email="340139661+Kansamu216@users.noreply.github.com" commit -m "Publish $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" | Out-Null

  $tok = $null
  try { $tok = (gh auth token) 2>$null } catch {}
  if (-not $tok) {
    # 没有 gh token 时，使用默认 git 凭据
    git remote add origin "https://github.com/$repo.git"
  }

  $ok = $false
  for ($attempt = 1; $attempt -le 6; $attempt++) {
    if ($tok) {
      $url = "https://Kansamu216:$tok@github.com/$repo.git"
      git push $url gh-pages:gh-pages -f
    } else {
      git push origin gh-pages:gh-pages -f
    }
    if ($LASTEXITCODE -eq 0) { $ok = $true; break }
    Write-Host "推送失败（可能是网络抖动），第 $attempt 次，3 秒后重试..." -ForegroundColor Yellow
    Start-Sleep -Seconds 3
  }
  if (-not $ok) { throw "推送到 GitHub 失败，请检查网络后重试" }

  Write-Host "==> 完成：https://kansamu216.github.io/ （约 1 分钟后生效）"
}
finally {
  Pop-Location
  Remove-Item -Recurse -Force "public\.git" -ErrorAction SilentlyContinue
}
