@echo off
chcp 65001 >nul
echo ===============================================================================
echo [WEPAPP] SUPERCLONE DOCUMENT ENGINE LAUNCHER
echo ===============================================================================
echo.
echo Running Document Compiler (HTML, DOCX, XLSX)...
echo.

if exist "C:\Users\EVE\miniconda3\python.exe" (
    "C:\Users\EVE\miniconda3\python.exe" "d:\Project\WEPAPP\build_superclone_weekly_inspection.py"
) else (
    python "d:\Project\WEPAPP\build_superclone_weekly_inspection.py"
)

echo.
echo ===============================================================================
echo Compilation finished! Check files:
echo - บันทึกรายงานผลการตรวจประจำสัปดาห์_Rebuild_Thai.html
echo - บันทึกรายงานผลการตรวจประจำสัปดาห์_Rebuild_Thai.docx
echo - บันทึกรายงานผลการตรวจประจำสัปดาห์_Rebuild_Thai.xlsx
echo ===============================================================================
pause
