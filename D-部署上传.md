# Agent D：部署上传

## 一、工作职责
将两个仓库的更新推送到 GitHub，使线上页面保持最新。
- Flask 系统推送 → 网页版（Railway/5020）更新
- GitHub Pages 推送 → APP 版更新

不负责：数据采集、预测分析、APP 同步。

## 二、工作目录
- Flask 仓库：`D:\V3.3.3-Core` → `https://github.com/athomas8285/V3.3.3-Core.git`
- GitHub Pages 仓库：`C:\Users\gjj\Documents\Codex\2026-06-14\app-app\outputs` → `https://github.com/athomas8285/worldcup2026.git`

## 三、输入输出
- 输入：Agent A/B/C 更新后产生的文件变更
- 输出：git push 到 origin/main

## 四、工作流程

### 前置条件
在开始之前确认 Agent C 已完成 APP 同步，Analysis.json 和 config.json 已是最新。

### 步骤 1：推送 Flask 仓库
```powershell
cd D:\V3.3.3-Core
$env:Path += ";C:\Program Files\Git\bin"
git status
git add .
git commit -m "update"
git push
```

### 步骤 2：推送 GitHub Pages 仓库
```powershell
cd "C:\Users\gjj\Documents\Codex\2026-06-14\app-app\outputs"
$env:Path += ";C:\Program Files\Git\bin"
git status
git add .
git commit -m "update"
git push
```

### 注意事项
- git 安装在：`C:\Program Files\Git\bin`
- 首次 push 如遇 SSL 错误：`git config http.sslVerify false`
- push 前先 git status 确认要推的文件正确
- 如果遇到冲突（非 fast-forward），先 git pull --rebase 再 push

### 步骤 3：验证线上状态
推送完成后，访问以下两个地址确认更新：
- Flask 版：https://web-production-5a133.up.railway.app/
- APP 版：https://athomas8285.github.io/worldcup2026/

### 步骤 4：日志记录
在本文档"五、工作日志"末尾追加一条记录。

## 五、工作日志

### 2026-06-21
- 首次创建本文档。当前状态：
  - Flask 仓库比 origin/main 领先 3 个 commit，有 3 个文件修改未提交
  - GitHub Pages 仓库未领先，有 2 个文件修改未提交
  - 待 Agent C 完成同步后再推送
