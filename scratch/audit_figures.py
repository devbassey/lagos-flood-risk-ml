"""
Audit all figures in Final_Project_Report.md
"""
import re
from pathlib import Path

p = Path(r"c:\Users\LENOVO\Desktop\Portfolio Projects\lagos-flood-risk-ml\outputs\Final_Project_Report.md")
lines = p.read_text(encoding="utf-8").splitlines()

figures = []
for idx, line in enumerate(lines):
    m = re.match(r"^!\[(Figure\s+[\d\.]+:?[^\]]*)\]\(([^)]+)\)", line.strip())
    if m:
        caption, fpath = m.group(1), m.group(2)
        # Check next 8 lines
        next_text = "\n".join(lines[idx+1:idx+9])
        has_explanation = ("Key Findings" in next_text or "Key Insights" in next_text or 
                           "Detailed Explanation" in next_text or "**" in next_text)
        figures.append((idx+1, caption, fpath, has_explanation))

print(f"Total Figures Found: {len(figures)}")
for line_no, cap, fp, has_exp in figures:
    status = "OK" if has_exp else "MISSING EXPLANATION"
    print(f"Line {line_no:4d} | {cap[:60]} | {status}")
