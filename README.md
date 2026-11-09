# 我的博客（Hexo + Fluid）

基于 [Hexo 8](https://hexo.io/) + [Fluid](https://hexo.fluid-dev.com/) 主题的静态博客。

## 环境说明

本机没有全局 Node/npm，依赖已用 DSH 自带 Node + pnpm 安装完成。
如需在命令行手动运行，可先让 node 可用：

```powershell
$nodeDir = "C:\Users\26703\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\node\bin"
$env:PATH = "$nodeDir;$env:PATH"
```

## 常用命令

在 `my-blog/` 目录下执行：

```bash
npx hexo new "文章标题"     # 新建文章 -> source/_posts/
npx hexo server             # 本地预览 http://localhost:4000
npx hexo generate           # 生成静态文件到 public/
npx hexo clean              # 清理缓存和 public/
npx hexo deploy             # 部署（需先配置 deploy）
```

若本机 node 未在 PATH，可改用完整路径：

```powershell
& "C:\Users\26703\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\node\bin\node.exe" node_modules\hexo\bin\hexo server
```

## 目录结构

- `source/_posts/` —— 文章（Markdown）
- `source/about/` —— 关于页
- `_config.yml` —— 站点配置（标题、作者、URL、部署）
- `_config.fluid.yml` —— 主题配置（导航、配色、暗色、搜索等）

## 写文章

新建的 `.md` 使用 front-matter：

```markdown
---
title: 标题
date: 2026-11-09 12:00:00
tags: [随笔]
categories: [记录]
---
正文……
```

正文里 `<!--more-->` 之前的内容会作为首页摘要。

## 部署（GitHub Pages，已配好）

本博客已发布到 **https://kansamu216.github.io/**，仓库：`Kansamu216/Kansamu216.github.io`。

发布方式是通用的 **gh-pages 分支**：`main` 存源码，`gh-pages` 存生成的静态文件。

写完文章后，一条命令即可发布：

```powershell
pwsh -ExecutionPolicy Bypass -File .\deploy.ps1
```

它会自动 `hexo clean` + `hexo generate`，然后把 `public/` 推到 `gh-pages` 分支，约 1 分钟后线上生效。

> 说明：本机 `gh` 的登录 token 没有 `workflow` 权限，所以没有使用 GitHub Actions，改用 gh-pages 分支发布。
> 若以后想改成 Actions 自动部署，可在 GitHub 给 token 加上 `workflow` 权限后，新建 `.github/workflows/deploy.yml` 配置 Pages 的 Actions 构建。

生成后的 `public/` 也是纯静态文件，可放到 Vercel / Netlify / 任意静态服务器。
