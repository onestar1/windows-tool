@echo off

REM ʹ�� PyInstaller ���
pyinstaller -F -w --uac-admin -i favicon.ico --add-data "favicon.ico;."  -n "�����ļ�" findFile.py


pause
