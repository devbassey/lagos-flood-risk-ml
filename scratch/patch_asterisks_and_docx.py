from pathlib import Path
import re

# 1. Update outputs/Final_Project_Report.md
p = Path('outputs/Final_Project_Report.md')
text = p.read_text(encoding='utf-8')

text = text.replace('*Annual Flood Outlooks-', '**Annual Flood Outlooks**')
text = text.replace('*when- flooding will occur', '**when** flooding will occur')
text = text.replace('*before- computing land elevation', '**before** computing land elevation')
text = text.replace('*prior- to monthly aggregation', '**prior** to monthly aggregation')
text = text.replace('*fastest accelerating risk frontiers-', '**fastest accelerating risk frontiers**')
text = text.replace('*\"what happens if infrastructure does not keep pace with climate and urban growth?\"- ---', '**\"what happens if infrastructure does not keep pace with climate and urban growth?\"** ---')
text = text.replace('*backward- up through the storm drains', '**backward** up through the storm drains')
text = text.replace('*Climate Change 2021: The Physical Science Basis.- Contribution', '*Climate Change 2021: The Physical Science Basis*. Contribution')
text = text.replace('*Climate Change 2022: Impacts, Adaptation and Vulnerability.- Contribution', '*Climate Change 2022: Impacts, Adaptation and Vulnerability*. Contribution')
text = text.replace('*2024 Annual Flood Outlook (AFO).- Nigeria', '*2024 Annual Flood Outlook (AFO)*. Nigeria')
text = text.replace('*ESA WorldCover 10 m 2021 v200.- European', '*ESA WorldCover 10 m 2021 v200*. European')

p.write_text(text, encoding='utf-8')
print('outputs/Final_Project_Report.md fixed!')

# 2. Update C:\Users\LENOVO\.gemini\antigravity\brain\dbbda659-ab1c-425a-952f-42069ce27ace\scratch\build_native_docx.py
docx_path = Path(r'C:\Users\LENOVO\.gemini\antigravity\brain\dbbda659-ab1c-425a-952f-42069ce27ace\scratch\build_native_docx.py')
d_text = docx_path.read_text(encoding='utf-8')

# Target lines 275-283
pattern = r'(\s+if line\.startswith\("- "\) or re\.match\(r"\^\\d\+\\.\\s\+", line\):.*?\n\s+continue)'

new_list_code = '''        # Handle bullet lists: '- ', '* ', '+ ' with indentation
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

d_text_new, count = re.subn(pattern, lambda m: new_list_code, d_text, flags=re.DOTALL)
if count > 0:
    docx_path.write_text(d_text_new, encoding='utf-8')
    print(f'build_native_docx.py successfully patched ({count} replacement)!')
else:
    print('Pattern not matched in build_native_docx.py')
