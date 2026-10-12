# convert_to_pdf.py
import pathlib
import sys

BASE_DIR = pathlib.Path(r"d:/Project/WEPAPP/docs/thai-docx.skill/ระบบเอกสาร")

def convert_excel(src: pathlib.Path, dst: pathlib.Path) -> None:
    """Convert .xlsx to PDF via xlsx2pdf library."""
    try:
        from xlsx2pdf import convert as xlsx_convert
    except ImportError:
        print("xlsx2pdf not installed", file=sys.stderr)
        raise
    xlsx_convert(str(src), str(dst))

def convert_docx(src: pathlib.Path, dst: pathlib.Path) -> None:
    """Convert .docx to PDF via docx2pdf library."""
    from docx2pdf import convert as docx_convert
    docx_convert(str(src), str(dst))

def main() -> None:
    for entry in BASE_DIR.iterdir():
        if entry.is_dir():
            continue
        name_lower = entry.name.lower()
        if name_lower.endswith('.pdf'):
            continue
        target = entry.with_name(entry.stem + '_converted.pdf')
        try:
            if name_lower.endswith(('.xlsx', '.xls')):
                print(f"Converting Excel: {entry.name} -> {target.name}")
                convert_excel(entry, target)
            elif name_lower.endswith('.docx'):
                print(f"Converting Word: {entry.name} -> {target.name}")
                convert_docx(entry, target)
            else:
                print(f"Skipping unsupported file: {entry.name}")
        except Exception as e:
            print(f"Failed to convert {entry.name}: {e}", file=sys.stderr)

if __name__ == '__main__':
    main()
