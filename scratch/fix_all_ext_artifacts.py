from pathlib import Path
import re

files_to_clean = [
    Path("outputs/Final_Project_Report.md"),
    Path("outputs/In_Depth_Research_and_Benchmarks.md"),
    Path("outputs/Presentation_Speaker_Notes.md"),
    Path("outputs/Defense_QA_Preparation_Guide.md"),
    Path("outputs/Portfolio_and_LinkedIn_Writeup.md"),
    Path(r"C:\Users\LENOVO\.gemini\antigravity\brain\dbbda659-ab1c-425a-952f-42069ce27ace\final_project_report.md"),
    Path(r"C:\Users\LENOVO\.gemini\antigravity\brain\dbbda659-ab1c-425a-952f-42069ce27ace\in_depth_research_and_benchmarks.md"),
]

def clean_text_artifacts(content):
    # Fix patterns like \text{...}, \text {...}, \t ext{...}, \text, \t ext
    # Also fix $ext{...}$ or \text{mm} -> mm
    content = re.sub(r'\\?text\s*\{([^}]+)\}', r'\1', content)
    content = re.sub(r'\text\s*\{([^}]+)\}', r'\1', content)
    content = re.sub(r'\text\b', '', content)
    # Fix tab + ext{...}
    content = re.sub(r'\text\{([^}]+)\}', r'\1', content)
    content = re.sub(r'[\t\\]ext\{([^}]+)\}', r'\1', content)
    content = re.sub(r'ext\{([^}]+)\}', r'\1', content)
    
    # Fix any residual $...$ around single words or units like $BS$ or $60.0 mm$
    content = content.replace(r'\text', '')
    return content

for f in files_to_clean:
    if f.exists():
        txt = f.read_text(encoding="utf-8")
        cleaned = clean_text_artifacts(txt)
        f.write_text(cleaned, encoding="utf-8")
        print(f"Cleaned {f.name}")

print("All text artifacts thoroughly purged!")
