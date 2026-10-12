#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
uninstall_menu.py - สคริปต์ถอนการติดตั้งเมนูคลิกขวา "พิกัด PDF" ออกจาก Windows
"""

import sys

if not sys.platform.startswith("win"):
    print("[ERROR] สคริปต์นี้สำหรับระบบปฏิบัติการ Windows เท่านั้น")
    sys.exit(1)

import winreg

def delete_key_recursively(root_key, sub_key):
    try:
        key = winreg.OpenKey(root_key, sub_key, 0, winreg.KEY_ALL_ACCESS)
        while True:
            try:
                sub = winreg.EnumKey(key, 0)
                delete_key_recursively(key, sub)
            except OSError:
                break
        winreg.CloseKey(key)
        winreg.DeleteKey(root_key, sub_key)
        return True
    except FileNotFoundError:
        return False
    except Exception as e:
        print(f"[!] ไม่สามารถลบ {sub_key}: {e}")
        return False

def uninstall_context_menu():
    reg_paths = [
        r"Software\Classes\Directory\Background\shell\PdfCoords",
        r"Software\Classes\*\shell\PdfCoords"
    ]

    for reg_path in reg_paths:
        res = delete_key_recursively(winreg.HKEY_CURRENT_USER, reg_path)
        if res:
            print(f"[-] ลบเมนูออกจาก: HKCU\\{reg_path}")
        else:
            print(f"[-] ไม่พบ Key หรือลบเรียบร้อยแล้ว: HKCU\\{reg_path}")

    print("\n✅ ถอนการติดตั้งเมนูคลิกขวา 'พิกัด PDF' เรียบร้อยแล้ว")

if __name__ == "__main__":
    uninstall_context_menu()
