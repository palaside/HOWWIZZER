import re
from pythainlp.tokenize import word_tokenize
from pythainlp.corpus import thai_words
from pythainlp.util import dict_trie

# Military Custom Lexicon: Specialized military terms, ranks, unit designators, equipment & forms
MILITARY_TERMS = {
    # Ranks
    "พล.อ.", "พล.ท.", "พล.ต.", "พ.อ.", "พ.ท.", "พ.ต.",
    "ร.อ.", "ร.ท.", "ร.ต.", "จ.ส.อ.", "จ.ส.ท.", "จ.ส.ต.",
    "ส.อ.", "ส.ท.", "ส.ต.", "พลทหาร",
    # Units & Commands
    "ป.๔", "พัน.๔", "ร้อย.๑", "ร้อย.๒", "ร้อย.๓", "บก.ร้อย",
    "ผบ.พัน.ป.", "ผบ.ร้อย.ป.", "ผบ.ป.๔", "ผบ.พัน", "ผบ.ร้อย",
    "ส.หน.สย.", "ผบ.หมู่", "หมู่ส่งกำลังบำรุงฯ", "นายสิบส่งกำลัง",
    # Weapons & Equipment
    "ปบค.๙๕", "เอ็ม ๑๐๑ เอ ๑", "เอ็ม.๑๐๑", "เอ็ม ๑๐๑", "ขนาด ๑๐๕ มม.",
    "คส. ๔", "สพ.๔๖๐", "สาย สพ.", "สป.สาย สพ.", "ยุทธภัณฑ์",
    # Military Forms & Staff Terms
    "ทบ.๔๐๐-๐๑๒", "ทบ.๔๖๘-๒๐๔", "ทบ.๔๐๐-๐๐๕", "ทบ.๔๐๐-๐๑๑",
    "ทบ.๔๐๐-๐๗๑", "สด.๑", "ปรนนิบัติบำรุง", "สิ่งอุปกรณ์",
    "ตรวจถูกต้อง", "ผู้ตรวจสอบ", "ผู้เบิก", "ผู้จ่าย", "ผู้รับ"
}

class ThaiTypographyEngine:
    def __init__(self):
        # Merge standard Thai corpus with military custom terms
        combined_words = set(thai_words()).union(MILITARY_TERMS)
        self.custom_trie = dict_trie(dict_source=combined_words)
        self.tag_entity_pattern = re.compile(r'(<[^>]+>|&[a-zA-Z0-9#]+;)')
        # Match chunks of Thai characters (including Thai tone marks and vowels)
        self.token_splitter = re.compile(r'([\u0e00-\u0e7f]+)')

    def process_text(self, text: str) -> str:
        if not text:
            return ""

        chunks = self.token_splitter.split(text)
        processed_chunks = []
        for chunk in chunks:
            if not chunk:
                continue
            # If Thai text chunk, segment and insert ZWS
            if re.search(r'[\u0e00-\u0e7f]', chunk):
                words = word_tokenize(chunk, engine="newmm", custom_dict=self.custom_trie, keep_whitespace=True)
                processed_chunks.append("\u200b".join(words))
            else:
                # English, punctuation, numbers untouched
                processed_chunks.append(chunk)

        return "".join(processed_chunks)

    def process_html(self, html_content: str) -> str:
        if not html_content:
            return ""

        parts = self.tag_entity_pattern.split(html_content)
        result = []
        in_skip_block = False

        for part in parts:
            if not part:
                continue

            # Check if this part is an opening or closing script/style tag
            lower_part = part.lower()
            if lower_part.startswith('<script') or lower_part.startswith('<style'):
                in_skip_block = True
                result.append(part)
                continue
            elif lower_part.startswith('</script') or lower_part.startswith('</style'):
                in_skip_block = False
                result.append(part)
                continue

            if in_skip_block or self.tag_entity_pattern.match(part):
                # Verbatim HTML tag or entity
                result.append(part)
            else:
                # Real text content inside HTML
                result.append(self.process_text(part))

        return "".join(result)
