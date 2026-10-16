import os
from datetime import datetime

# Path to the weekly report PDF in the static folder
pdf_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'weekly_report.pdf'))

# Simple PDF content (minimal PDF) with current date
def generate_pdf(content_text: str) -> bytes:
    # Very minimal PDF structure with a single line of text
    pdf_template = f"""%PDF-1.4
%âãÏÓ
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >>
endobj
4 0 obj
<< /Length 44 >>
stream
BT /F1 24 Tf 100 700 Td ({content_text}) Tj ET
endstream
endobj
xref
0 5
0000000000 65535 f 
0000000010 00000 n 
0000000060 00000 n 
0000000117 00000 n 
0000000217 00000 n 
trailer
<< /Root 1 0 R /Size 5 >>
startxref
317
%%EOF"""
    return pdf_template.encode('latin-1')

if __name__ == '__main__':
    today = datetime.now().strftime('%Y-%m-%d')
    content = f"Weekly Report {today}"
    pdf_bytes = generate_pdf(content)
    # Ensure the static folder exists
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    with open(pdf_path, 'wb') as f:
        f.write(pdf_bytes)
    print(f"Weekly report PDF generated at {pdf_path}")
