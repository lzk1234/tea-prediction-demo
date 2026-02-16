# Git推送脚本
Set-Location $PSScriptRoot

Write-Host "===== 初始化并推送Git仓库 ====="

# 初始化（如果还没有）
if (-not (Test-Path ".git")) {
    git init
}

# 添加所有文件
git add -A

# 配置用户
git config user.name "lzk1234"
git config user.email "lzk1234@github.com"

# 提交
git commit -m "Initial commit: 茶叶销量预测Streamlit应用"

# 添加远程仓库
git remote remove origin 2>$null
git remote add origin https://github.com/lzk1234/tea-prediction-demo.git

# 推送到GitHub
Write-Host "正在推送到GitHub..."
git push -u origin master

Write-Host "===== 完成！====="
