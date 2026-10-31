"""
Thoroughly brush through outputs/Final_Project_Report.md and update scratch/build_native_docx.py.
Fixes:
1. All #### headings properly styled in Word (Deep Navy, Bold, 11pt, clean spacing).
2. All bullet points standardized to '- ' with proper multi-level indentation in Word.
3. All asterisks used for emphasis/sub-headers converted to clean bold **Text:**.
4. Zero stray or literal asterisks in Word OpenXML output.
5. Upgrade runs_xml to handle ***bold-italic***, **bold**, *italic*, and `code`.
"""

from pathlib import Path
import re

# -----------------------------------------------------------------------------
# 1. Update outputs/Final_Project_Report.md
# -----------------------------------------------------------------------------
REPORT_PATH = Path("outputs/Final_Project_Report.md")
md_text = REPORT_PATH.read_text(encoding="utf-8")

# Fix lines like "*when- floods occur" or "*documented- flood event"
md_text = md_text.replace("*when- floods occur", "**when** floods occur")
md_text = md_text.replace("*where- flooding concentrates", "**where** flooding concentrates")
md_text = md_text.replace("*documented- flood event", "**documented** flood event")
md_text = md_text.replace("*absence of a documented report", "**absence of a documented report**")
md_text = md_text.replace("*hazard intensity per km²*", "**hazard intensity per km²**")
md_text = md_text.replace("*human vulnerability and economic disruption*", "**human vulnerability and economic disruption**")

# Standardize all '* **' or '* ' bullets to '- **' or '- '
md_text = re.sub(r"^\*\s+(\*\*.*?\*\*|\w+)", r"- \1", md_text, flags=re.MULTILINE)
md_text = re.sub(r"^(\s*)\*\s+", r"\1- ", md_text, flags=re.MULTILINE)

# Convert any '- *Subhead:*' to '- **Subhead:**'
md_text = re.sub(r"(\s*[-•]\s*)\*([^*:\n]+:)\*", r"\1**\2**", md_text)
md_text = re.sub(r"(\s*[-•]\s*)\*([^*:\n]+)\*", r"\1**\2**", md_text)

# Ensure all #### headings in Section 3.8 have clean formatting
md_text = re.sub(r"^####\s+(\d+\.\d+\.\d+)\s+(.*?)$", r"#### \1: \2", md_text, flags=re.MULTILINE)
# Fix double colons if any: e.g. "#### 3.8.1: Why...:" -> "#### 3.8.1: Why..."
md_text = re.sub(r"^####\s+(\d+\.\d+\.\d+):\s*:\s*", r"#### \1: ", md_text, flags=re.MULTILINE)

REPORT_PATH.write_text(md_text, encoding="utf-8")
print("outputs/Final_Project_Report.md thoroughly updated and cleaned!")

# -----------------------------------------------------------------------------
# 2. Update scratch/build_native_docx.py
# -----------------------------------------------------------------------------
DOCX_SCRIPT_PATH = Path(r"C:\Users\LENOVO\.gemini\antigravity\brain\dbbda659-ab1c-425a-952f-42069ce27ace\scratch\build_native_docx.py")
docx_code = DOCX_SCRIPT_PATH.read_text(encoding="utf-8")

# Upgrade runs_xml in build_native_docx.py
OLD_RUNS_XML = '''def runs_xml(text, sz_half_pts=22, bold_default=False, italic_default=False, color_hex="1E293B"):
    text = clean_text(text)
    tokens = re.split(r"(\*\*[^*]+\*\*|`[^`]+`)", text)
    out = []
    for tok in tokens:
        if not tok:
            continue
        is_b = bold_default
        is_code = False
        val = tok
        if tok.startswith("**") and tok.endswith("**"):
            is_b = True
            val = tok[2:-2]
        elif tok.startswith("`") and tok.endswith("`"):
            is_code = True
            val = tok[1:-1]
        font_name = "Consolas" if is_code else "Calibri"
        rpr = [
            f'<w:rFonts w:ascii="{font_name}" w:hAnsi="{font_name}" w:cs="{font_name}"/>',
            f'<w:sz w:val="{sz_half_pts}"/><w:szCs w:val="{sz_half_pts}"/>',
            f'<w:color w:val="{color_hex}"/>',
        ]
        if is_b:
            rpr.append("<w:b/>")
        if italic_default:
            rpr.append("<w:i/>")
        out.append(f'<w:r><w:rPr>{"".join(rpr)}</w:rPr><w:t xml:space="preserve">{escape(val)}</w:t></w:r>')
    return "".join(out)'''

NEW_RUNS_XML = '''def runs_xml(text, sz_half_pts=22, bold_default=False, italic_default=False, color_hex="1E293B"):
    text = clean_text(text)
    # Tokenize bold-italic (***...***), bold (**...**), italic (*...*), or code (`...`)
    tokens = re.split(r"(\*\*\*[^*]+\*\*\*|\*\*[^*]+\*\*|(?<!\*)\*[^*]+\*(?!\*)|`[^`]+`)", text)
    out = []
    for tok in tokens:
        if not tok:
            continue
        is_b = bold_default
        is_i = italic_default
        is_code = False
        val = tok
        if tok.startswith("***") and tok.endswith("***") and len(tok) > 6:
            is_b = True
            is_i = True
            val = tok[3:-3]
        elif tok.startswith("**") and tok.endswith("**") and len(tok) > 4:
            is_b = True
            val = tok[2:-2]
        elif tok.startswith("*") and tok.endswith("*") and not tok.startswith("**") and len(tok) > 2:
            is_i = True
            val = tok[1:-1]
        elif tok.startswith("`") and tok.endswith("`") and len(tok) > 2:
            is_code = True
            val = tok[1:-1]
        
        # Purge any rogue stray asterisks inside val so zero literal asterisks print
        val = val.replace("*", "")
        if not val:
            continue
            
        font_name = "Consolas" if is_code else "Calibri"
        rpr = [
            f'<w:rFonts w:ascii="{font_name}" w:hAnsi="{font_name}" w:cs="{font_name}"/>',
            f'<w:sz w:val="{sz_half_pts}"/><w:szCs w:val="{sz_half_pts}"/>',
            f'<w:color w:val="{color_hex}"/>',
        ]
        if is_b:
            rpr.append("<w:b/>")
        if is_i:
            rpr.append("<w:i/>")
        out.append(f'<w:r><w:rPr>{"".join(rpr)}</w:rPr><w:t xml:space="preserve">{escape(val)}</w:t></w:r>')
    return "".join(out)'''

docx_code = docx_code.replace(OLD_RUNS_XML, NEW_RUNS_XML)

# Add support for #### headings and improved bullet handling in build_native_docx()
OLD_HEADINGS = '''        if line.startswith("# "):
            body_elements.append(para_xml(line[2:].strip(), sz_half_pts=34, bold=True, color_hex="0F172A", align="center", space_before=120, space_after=240))
            i += 1
            continue
        if line.startswith("## "):
            body_elements.append(para_xml(line[3:].strip(), sz_half_pts=28, bold=True, color_hex="0F172A", align="left", space_before=260, space_after=100))
            i += 1
            continue
        if line.startswith("### "):
            body_elements.append(para_xml(line[4:].strip(), sz_half_pts=24, bold=True, color_hex="1E3A8A", align="left", space_before=180, space_after=80))
            i += 1
            continue'''

NEW_HEADINGS = '''        if line.startswith("# "):
            body_elements.append(para_xml(line[2:].strip(), sz_half_pts=34, bold=True, color_hex="0F172A", align="center", space_before=120, space_after=240))
            i += 1
            continue
        if line.startswith("## "):
            body_elements.append(para_xml(line[3:].strip(), sz_half_pts=28, bold=True, color_hex="0F172A", align="left", space_before=260, space_after=100))
            i += 1
            continue
        if line.startswith("### "):
            body_elements.append(para_xml(line[4:].strip(), sz_half_pts=24, bold=True, color_hex="1E3A8A", align="left", space_before=180, space_after=80))
            i += 1
            continue
        if line.startswith("#### "):
            # Sub-heading level 4: bold, Deep Navy, clean spacing
            body_elements.append(para_xml(line[5:].strip(), sz_half_pts=22, bold=True, color_hex="1E3A8A", align="left", space_before=140, space_after=60))
            i += 1
            continue'''

docx_code = docx_code.replace(OLD_HEADINGS, NEW_HEADINGS)

# Upgrade bullet and numbered list handling
OLD_LISTS = '''        if line.startswith("- ") or re.match(r"^\d+\.\s+", line):
            m_num = re.match(r"^(\d+\.)\s+(.*)$", line)
            if m_num:
                txt = f"{m_num.group(1)} {m_num.group(2)}"
            else:
                txt = f"• {line[2:]}"
            body_elements.append(para_xml(txt, sz_half_pts=22, color_hex="1E293B", left_indent=360, space_before=30, space_after=40))
            i += 1
            continue'''

NEW_LISTS = '''        # Handle bullet lists: '- ', '* ', '+ ' with indentation
        m_bullet = re.match(r"^(\s*)[-*+]\s+(.*)$", line)
        if m_bullet:
            indent_spaces = len(m_bullet.group(1))
            indent_level = indent_spaces // 2
            content = m_bullet.group(2)
            bullet_sym = "•" if indent_level == 0 else "⁃"
            txt = f"{bullet_sym} {content}"
            body_elements.append(para_xml(txt, sz_half_pts=22, color_hex="1E293B", left_indent=360 + indent_level * 240, space_before=30, space_after=40))
            i += 1
            continue

        # Handle numbered lists: '1. ', '2. ', etc. with indentation
        m_num = re.match(r"^(\s*)(\d+\.)\s+(.*)$", line)
        if m_num:
            indent_spaces = len(m_num.group(1))
            indent_level = indent_spaces // 2
            num_str = m_num.group(2)
            content = m_num.group(3)
            txt = f"{num_str} {content}"
            body_elements.append(para_xml(txt, sz_half_pts=22, color_hex="1E293B", left_indent=360 + indent_level * 240, space_before=30, space_after=40))
            i += 1
            continue'''

docx_code = docx_code.replace(OLD_LISTS, NEW_LISTS)

DOCX_SCRIPT_PATH.write_text(docx_code, encoding="utf-8")
print("scratch/build_native_docx.py updated successfully!")
