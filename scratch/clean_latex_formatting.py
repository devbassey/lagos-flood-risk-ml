"""
Script to comprehensively clean LaTeX \\text{...} formatting artifacts from all markdown reports
and document generation pipelines.
"""

import re
from pathlib import Path

ROOT = Path(r"c:\Users\LENOVO\Desktop\Portfolio Projects\lagos-flood-risk-ml")
BRAIN = Path(r"C:\Users\LENOVO\.gemini\antigravity\brain\dbbda659-ab1c-425a-952f-42069ce27ace")

FILES_TO_CLEAN = [
    ROOT / "outputs" / "Final_Project_Report.md",
    ROOT / "outputs" / "In_Depth_Research_and_Benchmarks.md",
    ROOT / "outputs" / "Presentation_Speaker_Notes.md",
    ROOT / "outputs" / "Defense_QA_Preparation_Guide.md",
    ROOT / "outputs" / "Portfolio_and_LinkedIn_Writeup.md",
    BRAIN / "final_project_report.md",
    BRAIN / "in_depth_research_and_benchmarks.md",
]

def clean_markdown_latex(text: str) -> str:
    # 1. Clean common unit and symbol combinations first
    text = text.replace(r"\text{km}^2", "km²")
    text = text.replace(r"\text{/km}^2", "/km²")
    text = text.replace(r"\text{ km}^2", " km²")
    text = text.replace(r"\text{ m}", " m")
    text = text.replace(r"\text{ km}", " km")
    text = text.replace(r"\text{ mm}", " mm")
    text = text.replace(r"\text{ days}", " days")
    text = text.replace(r"\text{ day}", " day")
    text = text.replace(r"\text{ ms}", " ms")
    text = text.replace(r"\text{ms}", "ms")
    text = text.replace(r"\text{ mo/yr}", " mo/yr")
    text = text.replace(r"\text{ metres}", " metres")
    text = text.replace(r"\text{ records}", " records")
    text = text.replace(r"\text{ months}", " months")
    text = text.replace(r"\text{ LGAs}", " LGAs")
    text = text.replace(r"\text{ UTC}", " UTC")
    text = text.replace(r"\text{ arc-second}", " arc-second")
    text = text.replace(r"\Delta\text{SLR}", "ΔSLR")
    
    # 2. Clean general \text{...}
    text = re.sub(r"\\text\{([^}]+)\}", r"\1", text)
    
    # 3. Clean inline dollar signs around simple numbers and units, e.g. $5.5 km$ -> 5.5 km
    # But preserve LaTeX equations like $$\text{FRI} ... $$
    def clean_simple_math(match):
        inner = match.group(1).strip()
        # If it's just numbers, units, abbreviations, clean it
        if re.match(r"^[\d\.,\s\+\-–—±%km²/\(\)]+$", inner):
            return inner
        # Common unit expressions
        if inner in ["m", "km", "mm", "days", "day", "ms", "mo/yr", "km²", "/km²"]:
            return inner
        # Simple metrics
        if inner in ["BS", "BSS", "REL", "RES", "UNC", "POD", "FAR", "CSI", "FBI", "HSS", "ETS", "FRI", "SLR", "Rx1day", "Rx3day", "Rx5day", "Rx7day"]:
            return inner
        return f"${inner}$"

    # Replace inline single $...$ that only contain simple units/numbers
    text = re.sub(r"(?<!\$)\$([^$\n]+)\$(?!\$)", clean_simple_math, text)
    
    # 4. Clean common residual LaTeX constructs
    text = text.replace(r"\approx", "≈")
    text = text.replace(r"\ge", "≥")
    text = text.replace(r"\le", "≤")
    text = text.replace(r"\times", "×")
    text = text.replace(r"\pm", "±")
    text = text.replace(r"\to", "→")
    text = text.replace(r"\ne", "≠")
    text = text.replace(r"\%", "%")
    
    # 5. Filter any illegal control characters
    text = "".join(c for c in text if ord(c) >= 32 or c in "\n\r\t")
    
    return text

def main():
    cleaned_count = 0
    for p in FILES_TO_CLEAN:
        if p.exists():
            original = p.read_text(encoding="utf-8")
            cleaned = clean_markdown_latex(original)
            p.write_text(cleaned, encoding="utf-8")
            print(f"Cleaned {p.name}: {len(re.findall(r'\\\\text', cleaned))} residual \\text occurrences remaining.")
            cleaned_count += 1
    print(f"\nSuccessfully cleaned {cleaned_count} files!")

if __name__ == "__main__":
    main()
