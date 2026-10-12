import glob
import os
import sys
from thai_typography_engine import ThaiTypographyEngine

sys.stdout.reconfigure(encoding='utf-8')

def main():
    engine = ThaiTypographyEngine()
    target_files = []
    
    # 1. Root HTML documents
    for f in glob.glob('*.html'):
        if not f.startswith('test_'):
            target_files.append(f)
            
    # 2. Reference HTML documents
    for f in glob.glob('references/**/*.html', recursive=True):
        target_files.append(f)
        
    # 3. HotFolder HTML documents
    for f in glob.glob('hotfolder/ready_to_print/*.html'):
        target_files.append(f)
        
    # 4. Frontend HTML documents
    for f in glob.glob('frontend/**/*.html', recursive=True):
        target_files.append(f)

    target_files = sorted(list(set(target_files)))
    print(f"Applying Thai ZWS Segmentation Engine to {len(target_files)} files...")
    
    updated_count = 0
    for file_path in target_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update CSS justification rules inside rta-universal-thin-font-engine style block
        if 'word-break: keep-all;' not in content and '<style id="rta-universal-thin-font-engine">' in content:
            content = content.replace(
                "text-justify: inter-cluster;",
                "text-justify: inter-cluster; word-break: keep-all; overflow-wrap: break-word;"
            )

        processed = engine.process_html(content)
        if processed != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(processed)
            updated_count += 1
            print(f"[ZWS APPLIED] {file_path}")
        else:
            print(f"[UNCHANGED] {file_path}")

    print(f"\nSuccessfully applied ZWS to {updated_count}/{len(target_files)} files!")

if __name__ == '__main__':
    main()
