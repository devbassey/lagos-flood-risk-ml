from pathlib import Path
import re

text = Path(r"C:\Users\LENOVO\.gemini\antigravity\brain\dbbda659-ab1c-425a-952f-42069ce27ace\scratch\build_pptx.py").read_text(encoding="utf-8")
matches = re.findall(r'"num":\s*(\d+).*?"title":\s*"([^"]+)".*?(?:"fig_name":\s*"([^"]+)")?', text, re.DOTALL)
for m in matches:
    print(f"Slide {m[0]}: {m[1]} | Fig: {m[2] if m[2] else 'None'}")
