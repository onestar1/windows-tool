@echo off

REM 使用 PyInstaller 打包
pyinstaller -F -w --uac-admin -i favicon.ico --add-data "favicon.ico;."  -n "搜索文件" findFile.py


pause
