@echo off
rem ------------------------------------------------------------------
rem Weekly update script – สร้าง PDF รายสัปดาห์และคัดลอกเป็นไฟล์ต่อไป
rem ------------------------------------------------------------------

rem 1. รันสคริปต์ Python (ใช้ตัวรัน py -3 เพื่อให้ทำงานบน Windows)
py -3 "%~dp0\generate_weekly_report.py"

rem 2. คัดลอก PDF รายสัปดาห์เป็นไฟล์สัปดาห์หน้า
copy /Y "%~dp0\static\weekly_report.pdf" "%~dp0\static\weekly_report_next.pdf"

rem จบสคริปต์
exit /b 0
