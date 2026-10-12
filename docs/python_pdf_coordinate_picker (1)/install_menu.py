#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
install_menu.py - สคริปต์ลงทะเบียนเมนูคลิกขวา "พิกัด PDF" บน Windows
ใช้โมดูล winreg มาตรฐาน (ไม่ต้องใช้สิทธิ์ Administrator / UAC)
"""

import sys
import os

if not sys.platform.startswith("win"):
    print("[ERROR] สคริปต์นี้สำหรับติดตั้งบนระบบปฏิบัติการ Windows เท่านั้น")
    sys.exit(1)

import winreg

def install_context_menu():
    # หา path ของ pythonw.exe (รันแบบไม่มีหน้าต่างคอนโซลสีดำ)
    python_dir = os.path.dirname(sys.executable)
    pythonw_exe = os.path.join(python_dir, "pythonw.exe")
    if not os.path.exists(pythonw_exe):
        pythonw_exe = sys.executable

    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "pdf_coord_picker.py"))
    command = f'"{pythonw_exe}" "{script_path}"'

    menu_title = "พิกัด PDF"

    # ตำแหน่ง Registry ที่จะเพิ่มเมนู (สำหรับ Desktop/โฟลเดอร์ และคลิกขวาที่ไฟล์ใดๆ)
    reg_paths = [
        r"Software\Classes\Directory\Background\shell\PdfCoords",  # คลิกขวาบนพื้นที่ว่าง Desktop/โฟลเดอร์
        r"Software\Classes\*\shell\PdfCoords"                      # คลิกขวาบนไฟล์ใดๆ (เช่น ไฟล์ PDF)
    ]

    for reg_path in reg_paths:
        try:
            # สร้าง Key หลัก
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)
            winreg.SetValue(key, "", winreg.REG_SZ, menu_title)
            # ตั้งไอคอน Crosshair/แว่นขยายจาก shell32.dll
            winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, "shell32.dll,22")
            winreg.CloseKey(key)

            # สร้าง Key command
            cmd_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path + r"\command")
            winreg.SetValue(cmd_key, "", winreg.REG_SZ, command)
            winreg.CloseKey(cmd_key)

            print(f"[+] ติดตั้งเมนูสำเร็จที่: HKCU\\{reg_path}")
        except Exception as e:
            print(f"[!] เกิดข้อผิดพลาดที่ {reg_path}: {e}")

    print("\n" + "="*60)
    print("✅ ติดตั้งเมนูคลิกขวา 'พิกัด PDF' บน Windows เรียบร้อยแล้ว!")
    print("ทดลองใช้งาน: คลิกขวาที่หน้าจอ Desktop หรือในหน้าต่างใดๆ จะพบเมนู 'พิกัด PDF'")
    print("="*60)

if __name__ == "__main__":
    install_context_menu()
