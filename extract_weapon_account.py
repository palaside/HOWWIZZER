import sys
import fitz  # PyMuPDF

def extract_text(pdf_path: str, output_path: str | None = None) -> None:
    """Extract all textual content from the given PDF.

    Args:
        pdf_path: Path to the PDF file.
        output_path: Optional path to write the extracted text.
                     If omitted, the text is printed to stdout.
    """
    doc = fitz.open(pdf_path)
    full_text = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        full_text.append(page.get_text())
    result = "\n".join(full_text)
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"Extracted text saved to {output_path}")
    else:
        print(result)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_weapon_account.py <pdf_path> [output.txt]")
        sys.exit(1)
    pdf_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    extract_text(pdf_path, output_path)
