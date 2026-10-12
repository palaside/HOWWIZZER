@echo off
chcp 65001 > nul
title ถอนการติดตั้งเมนูคลิกขวา - พิกัด PDF
echo กำลังถอนการติดตั้งเมนู "พิกัด PDF"...
python uninstall_menu.py
echo.
pause
