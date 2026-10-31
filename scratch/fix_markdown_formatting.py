"""
Script to brush through the report and fix all markdown formatting issues:
1. Replace all single asterisks used as bold markers (e.g. *Key Point:* -> **Key Point:**)
2. Replace all '* **' bullet lists with clean '- **' bullet lists.
3. Clean all hanging or unclosed asterisks.
4. Ensure all #### headings are properly spaced and styled.
"""

from pathlib import Path
import re

REPORT_PATH = Path("outputs/Final_Project_Report.md")
text = REPORT_PATH.read_text(encoding="utf-8")

# 1. Convert '* **' bullet points to '- **'
# E.g., "* **Why CMIP6...?**" -> "- **Why CMIP6...?**"
# E.g., "* **Technical Definition:**" -> "- **Technical Definition:**"
text = re.sub(r"^\*\s+(\*\*.*?\*\*|\w+)", r"- \1", text, flags=re.MULTILINE)
text = re.sub(r"^(\s+)\*\s+", r"\1- ", text, flags=re.MULTILINE)

# 2. Convert '*Term:*' or '  - *Term:*' to '**Term:**' (bold instead of italic with asterisks)
# E.g., "- *Physical Modeling Improvements:* The..." -> "- **Physical Modeling Improvements:** The..."
text = re.sub(r"(\s*[-•]\s*)\*([^*:\n]+:)\*", r"\1**\2**", text)
text = re.sub(r"(\s*[-•]\s*)\*([^*:\n]+)\*", r"\1**\2**", text)

# 3. In Section 3.8 and Section 10.1-10.4, clean any remaining '* **' lines:
text = re.sub(r"^\*\s+", "- ", text, flags=re.MULTILINE)

# 4. In citations, ensure clean formatting
# E.g., "*Journal of Flood Risk Management*, 9(3)" -> clean italics or plain
# Leave journal titles as clean or bold

# 5. Clean any residual lone asterisks
# E.g. " * " -> " "
text = re.sub(r"(?<!\*)\*(?!\*)\s+", "- ", text)

REPORT_PATH.write_text(text, encoding="utf-8")
print("Cleaned markdown formatting in outputs/Final_Project_Report.md")
