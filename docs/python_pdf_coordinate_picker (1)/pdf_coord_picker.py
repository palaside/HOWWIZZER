#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pdf_coord_picker.py - เครื่องมือชี้พิกัด PDF / หน้าจอ และ Auto-Inject ส่งเข้าแชทอัตโนมัติ
ทำงานด้วย Pure Python Standard Library (Tkinter + ctypes) ไม่ต้องลง library เพิ่มเติม
"""

import sys
import time
import os

try:
    import tkinter as tk
except ImportError:
    print("[ERROR] กรุณาติดตั้งหรือเปิดใช้งาน Tkinter สำหรับ Python")
    sys.exit(1)

# ตรวจสอบระบบปฏิบัติการ Windows สำหรับ ctypes keyboard event
IS_WINDOWS = sys.platform.startswith("win")
if IS_WINDOWS:
    import ctypes
    user32 = ctypes.windll.user32
    VK_CONTROL = 0x11
    VK_V = 0x56
    VK_RETURN = 0x0D
    KEYEVENTF_KEYUP = 0x0002

class CoordinatePicker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 0.35)  # ความโปร่งใส 35%
        self.root.config(cursor="crosshair")
        self.root.attributes("-topmost", True)

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.canvas = tk.Canvas(self.root, cursor="crosshair", bg="#0a1914", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.start_x = None
        self.start_y = None
        self.rect_id = None
        self.hud_text_id = None

        # ข้อความคำแนะนำด้านบนหน้าจอ
        self.canvas.create_text(
            self.screen_width // 2, 40,
            text="🎯 โหมดชี้พิกัด PDF: คลิกเลือกจุด หรือคลิกลากเมาส์ครอบ Bounding Box  (กด ESC เพื่อยกเลิก)",
            fill="#34d399",
            font=("Segoe UI", 16, "bold")
        )

        # ผูกเหตุการณ์เมาส์และคีย์บอร์ด
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.root.bind("<Escape>", lambda e: self.root.destroy())

        self.result_text = None

    def on_mouse_move(self, event):
        # แสดงพิกัดเคอร์เซอร์สดแบบเรียลไทม์
        hud_msg = f"พิกัดเคอร์เซอร์: X = {event.x} px | Y = {event.y} px"
        if self.hud_text_id:
            self.canvas.delete(self.hud_text_id)
        self.hud_text_id = self.canvas.create_text(
            event.x + 20, event.y + 20,
            text=hud_msg,
            anchor="nw",
            fill="#ffffff",
            font=("Consolas", 11, "bold")
        )

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        self.rect_id = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline="#ef4444", width=2, fill="#ef4444", stipple="gray25"
        )

    def on_mouse_drag(self, event):
        cur_x = event.x
        cur_y = event.y
        self.canvas.coords(self.rect_id, self.start_x, self.start_y, cur_x, cur_y)
        w = abs(cur_x - self.start_x)
        h = abs(cur_y - self.start_y)
        if self.hud_text_id:
            self.canvas.delete(self.hud_text_id)
        self.hud_text_id = self.canvas.create_text(
            cur_x + 15, cur_y + 15,
            text=f"กรอบ: {w} × {h} px",
            anchor="nw",
            fill="#fbbf24",
            font=("Consolas", 12, "bold")
        )

    def on_button_release(self, event):
        end_x = event.x
        end_y = event.y

        # คำนวณพิกัด Bounding Box: x0 (Left), y0 (Top), x1 (Right), y1 (Bottom)
        x0 = min(self.start_x, end_x)
        y0 = min(self.start_y, end_y)
        x1 = max(self.start_x, end_x)
        y1 = max(self.start_y, end_y)

        width = x1 - x0
        height = y1 - y0

        # กรณีคลิกเดี่ยว (Single Click Point) ไม่ได้ลากกรอบ
        if width < 5 and height < 5:
            click_point = f"X = {end_x} px, Y = {end_y} px"
            # กำหนดกรอบสมมติรอบจุด 10x10 px
            x0 = max(0, end_x - 5)
            y0 = max(0, end_y - 5)
            x1 = end_x + 5
            y1 = end_y + 5
            width = 10
            height = 10
        else:
            click_point = f"กึ่งกลาง X = {(x0 + x1) // 2} px, Y = {(y0 + y1) // 2} px"

        # ตรวจสอบ Orientation (แนวตั้ง / แนวนอน)
        if width >= height:
            orientation = "แนวนอน (Landscape)"
        else:
            orientation = "แนวตั้ง (Portrait)"

        # จัดรูปแบบข้อความพิกัดให้สวยงาม
        self.result_text = (
            f"📍 [พิกัดหน้าจอ/PDF - Bounding Box]\n"
            f"• ตำแหน่งเคอร์เซอร์: {click_point}\n"
            f"• ทิศทาง (Orientation): {orientation}\n"
            f"• Bounding Box:\n"
            f"   - x0 (Left)   : {x0} px\n"
            f"   - y0 (Top)    : {y0} px\n"
            f"   - x1 (Right)  : {x1} px\n"
            f"   - y1 (Bottom) : {y1} px\n"
            f"• ขนาดกรอบ (Dimension): กว้าง {width} px | สูง {height} px\n"
            f"• หน้าจออ้างอิง: {self.screen_width} × {self.screen_height} px"
        )

        # บันทึกลง Clipboard
        self.root.clipboard_clear()
        self.root.clipboard_append(self.result_text)
        self.root.update()

        # ปิดหน้าต่าง Overlay
        self.root.destroy()

        # ส่งข้อความเข้าช่องแชทอัตโนมัติ
        self.auto_inject_and_send()

    def auto_inject_and_send(self):
        """จำลองการกด Ctrl + V และ Enter ส่งเข้าช่องแชททันที"""
        # รอให้หน้าต่างเดิม (ช่องแชท) ได้รับ Focus คืนมา
        time.sleep(0.35)

        if IS_WINDOWS:
            # 1. วางข้อความ (Ctrl + V)
            user32.keybd_event(VK_CONTROL, 0, 0, 0)
            user32.keybd_event(VK_V, 0, 0, 0)
            user32.keybd_event(VK_V, 0, KEYEVENTF_KEYUP, 0)
            user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)

            time.sleep(0.15)

            # 2. กดปุ่ม Enter ส่งข้อความทันที
            user32.keybd_event(VK_RETURN, 0, 0, 0)
            user32.keybd_event(VK_RETURN, 0, KEYEVENTF_KEYUP, 0)
        else:
            # Fallback บน Linux (ถ้ามี xdotool)
            try:
                import subprocess
                subprocess.run(["xdotool", "key", "ctrl+v"], check=False)
                time.sleep(0.1)
                subprocess.run(["xdotool", "key", "Return"], check=False)
            except Exception:
                pass

        print("\n[SUCCESS] คัดลอกและส่งพิกัดเข้าช่องแชทเรียบร้อยแล้ว:")
        print(self.result_text)

def main():
    picker = CoordinatePicker()
    picker.root.mainloop()

if __name__ == "__main__":
    main()
