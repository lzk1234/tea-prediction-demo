@echo off
cd /d "%~dp0"

echo ===== 初始化Git仓库并推送到GitHub =====

git init
git add .
git config user.name "lzk1234"
git config user.email "lzk1234@github.com"
git commit -m "Initial commit: 茶叶销量预测Streamlit应用"

echo.
echo 请在以下URL输入你的GitHub账号密码来推送:
echo https://github.com/lzk1234/tea-prediction-demo.git
echo.

git remote add origin https://github.com/lzk1234/tea-prediction-demo.git
git push -u origin master

echo.
echo ===== 完成！=====
pause
