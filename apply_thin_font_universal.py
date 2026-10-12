import os
import sys
import glob
import re

sys.stdout.reconfigure(encoding='utf-8')

UNIFIED_STYLE_BLOCK = """<!-- UNIFIED MILITARY SARABUN FONT-ENGINE & RULE 9 THIN/LIGHT STANDARD -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sarabun:ital,wght@0,100;0,200;0,300;0,400;0,600;0,700;1,100;1,300;1,400;1,700&display=swap" rel="stylesheet">
<style id="rta-universal-thin-font-engine">
    @font-face {
        font-family: 'Sarabun';
        font-style: normal;
        font-weight: 100;
        src: url('/fonts/Sarabun-Thin.ttf') format('truetype'),
             url('fonts/Sarabun-Thin.ttf') format('truetype'),
             url('../fonts/Sarabun-Thin.ttf') format('truetype'),
             url('../../fonts/Sarabun-Thin.ttf') format('truetype');
    }
    @font-face {
        font-family: 'Sarabun';
        font-style: normal;
        font-weight: 200;
        src: url('/fonts/Sarabun-ExtraLight.ttf') format('truetype'),
             url('fonts/Sarabun-ExtraLight.ttf') format('truetype'),
             url('../fonts/Sarabun-ExtraLight.ttf') format('truetype'),
             url('../../fonts/Sarabun-ExtraLight.ttf') format('truetype');
    }
    @font-face {
        font-family: 'Sarabun';
        font-style: normal;
        font-weight: 300;
        src: url('/fonts/Sarabun-Light.ttf') format('truetype'),
             url('fonts/Sarabun-Light.ttf') format('truetype'),
             url('../fonts/Sarabun-Light.ttf') format('truetype'),
             url('../../fonts/Sarabun-Light.ttf') format('truetype');
    }
    @font-face {
        font-family: 'Sarabun';
        font-style: normal;
        font-weight: 400;
        src: url('/fonts/Sarabun-Regular.ttf') format('truetype'),
             url('fonts/Sarabun-Regular.ttf') format('truetype'),
             url('../fonts/Sarabun-Regular.ttf') format('truetype'),
             url('../../fonts/Sarabun-Regular.ttf') format('truetype');
    }
    @font-face {
        font-family: 'Sarabun';
        font-style: normal;
        font-weight: 700;
        src: url('/fonts/Sarabun-Bold.ttf') format('truetype'),
             url('fonts/Sarabun-Bold.ttf') format('truetype'),
             url('../fonts/Sarabun-Bold.ttf') format('truetype'),
             url('../../fonts/Sarabun-Bold.ttf') format('truetype');
    }

    /* Force Windows to alias legacy TH Sarabun names to genuine Sarabun Thin/Light */
    @font-face {
        font-family: 'TH Sarabun New';
        font-style: normal;
        font-weight: 100;
        src: url('/fonts/Sarabun-Thin.ttf') format('truetype'),
             url('fonts/Sarabun-Thin.ttf') format('truetype'),
             url('../fonts/Sarabun-Thin.ttf') format('truetype'),
             url('../../fonts/Sarabun-Thin.ttf') format('truetype');
    }
    @font-face {
        font-family: 'TH Sarabun New';
        font-style: normal;
        font-weight: 300;
        src: url('/fonts/Sarabun-Light.ttf') format('truetype'),
             url('fonts/Sarabun-Light.ttf') format('truetype'),
             url('../fonts/Sarabun-Light.ttf') format('truetype'),
             url('../../fonts/Sarabun-Light.ttf') format('truetype');
    }
    @font-face {
        font-family: 'TH Sarabun PSK';
        font-style: normal;
        font-weight: 100;
        src: url('/fonts/Sarabun-Thin.ttf') format('truetype'),
             url('fonts/Sarabun-Thin.ttf') format('truetype'),
             url('../fonts/Sarabun-Thin.ttf') format('truetype'),
             url('../../fonts/Sarabun-Thin.ttf') format('truetype');
    }
    @font-face {
        font-family: 'TH Sarabun PSK';
        font-style: normal;
        font-weight: 300;
        src: url('/fonts/Sarabun-Light.ttf') format('truetype'),
             url('fonts/Sarabun-Light.ttf') format('truetype'),
             url('../fonts/Sarabun-Light.ttf') format('truetype'),
             url('../../fonts/Sarabun-Light.ttf') format('truetype');
    }

    /* RULE 9: THIN FONT-WEIGHT MANDATE (Non-headings = 300 Thin/Light, Headings = 700 Bold) */
    body, div, p, span, td, li, a, input, textarea, label, select, button,
    section, article, main, header, footer,
    .memo-p, .memo-body, .memo-closing, .memo-content, .memo-text, .content-para,
    .memo-meta-dots, .meta-fill-dotted, .dotted-line, .memo-att-row, .memo-att-desc, .memo-att-qty,
    .salutation-row, .salutation, .reference-section, .attachment-section, .attachment-row, .attachment-item,
    .sig-name, .sig-pos, .sig-date, .sig-rank-anchor,
    .staff-grid, .staff-grid div, .staff-col, .form-table td, table td,
    .doc-desc, .stat-pill, .btn-action, .meta-row, .meta-half-col,
    .meta-fill-dotted div {
        font-family: 'Sarabun', 'TH Sarabun New', 'TH Sarabun PSK', Tahoma, sans-serif !important;
        font-weight: 300 !important;
    }

    /* Exclusively Headings & Titles are Bold (700) */
    b, strong, .font-bold, .bold, th, table th,
    .memo-title, .doc-title, .meta-label, .memo-meta-label,
    .form-header-title, .form-header-sub, .form-title,
    .photo-cert-text, .sig-verify,
    .brand-title, .brand-badge, .badge, .doc-code,
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Sarabun', 'TH Sarabun New', 'TH Sarabun PSK', Tahoma, sans-serif !important;
        font-weight: 700 !important;
    }
</style>
"""

def update_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Clean out legacy 400-only font links and imports
    legacy_imports = [
        r"@import\s+url\(['\"]https://fonts\.googleapis\.com/css2\?family=Sarabun:wght@400[^'\"]*['\"]\);\s*",
        r"<link\s+href=['\"]https://fonts\.googleapis\.com/css2\?family=Sarabun:wght@400[^'\"]*['\"]\s+rel=['\"]stylesheet['\"]>\s*",
        r"<link\s+href=['\"]https://fonts\.googleapis\.com/css2\?family=Sarabun:wght@400[^'\"]*['\"][^>]*>\s*",
    ]
    for leg in legacy_imports:
        content = re.sub(leg, '', content)

    # 2. If already injected, replace the whole old block
    if '<style id="rta-universal-thin-font-engine">' in content or '<!-- UNIFIED MILITARY SARABUN FONT-ENGINE' in content:
        pattern = r'(?:<!-- UNIFIED MILITARY SARABUN FONT-ENGINE & RULE 9 THIN/LIGHT STANDARD -->\s*)?(?:<link rel="preconnect" href="https://fonts\.googleapis\.com">\s*<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>\s*<link href="https://fonts\.googleapis\.com/css2\?family=Sarabun:[^"]*" rel="stylesheet">\s*)?<style id="rta-universal-thin-font-engine">[\s\S]*?</style>'
        new_content = re.sub(pattern, UNIFIED_STYLE_BLOCK, content)
    else:
        # Inject right before </head> or at the top of <head>
        if '</head>' in content:
            new_content = content.replace('</head>', f'{UNIFIED_STYLE_BLOCK}\n</head>')
        elif '<style>' in content:
            new_content = content.replace('<style>', f'{UNIFIED_STYLE_BLOCK}\n<style>')
        else:
            new_content = UNIFIED_STYLE_BLOCK + '\n' + content

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    target_files = []
    
    # 1. Root documents (including index.html)
    for f in glob.glob('*.html'):
        if f.startswith('test_'):
            continue
        target_files.append(f)
        
    # 2. Reference documents
    for f in glob.glob('references/**/*.html', recursive=True):
        target_files.append(f)
        
    # 3. Ready to print documents
    for f in glob.glob('hotfolder/ready_to_print/*.html'):
        target_files.append(f)
        
    # 4. Frontend templates
    for f in glob.glob('frontend/**/*.html', recursive=True):
        target_files.append(f)

    # De-duplicate
    target_files = sorted(list(set(target_files)))

    updated_count = 0
    print(f"Targeting {len(target_files)} HTML files for Universal Thin Typography...")
    for tf in target_files:
        changed = update_html_file(tf)
        status = "UPDATED" if changed else "UNCHANGED"
        print(f"[{status}] {tf}")
        if changed:
            updated_count += 1
            
    print(f"\nSuccessfully applied Universal Thin Engine to {updated_count}/{len(target_files)} files!")

if __name__ == '__main__':
    main()
