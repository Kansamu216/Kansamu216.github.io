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

## 部署

生成后的 `public/` 是纯静态文件，可放到 GitHub Pages / Vercel / Netlify / 任意静态服务器。
