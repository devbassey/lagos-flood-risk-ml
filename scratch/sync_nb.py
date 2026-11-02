import json

with open('notebooks/09_risk_index.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

with open('scratch/generate_interactive_map.py', 'r', encoding='utf-8') as f:
    script_content = f.read()

# Extract from '# Prepare GeoJSON' to end of template write
start_marker = '# Prepare GeoJSON with embedded metrics for every LGA across all scenario-period combinations'
idx_start = script_content.find(start_marker)
source_code = script_content[idx_start:]
# Replace OUT_HTML with MAP_OUT_PATH
source_code = source_code.replace('OUT_HTML.write_text(html_content, encoding="utf-8")', 'MAP_OUT_PATH.write_text(html_content, encoding="utf-8")')
source_code = source_code.replace('OUT_HTML.resolve()', 'MAP_OUT_PATH.resolve()')
source_code = source_code.replace('OUT_HTML.stat()', 'MAP_OUT_PATH.stat()')

nb['cells'][15]['source'] = [line + '\n' for line in source_code.split('\n')[:-1]] + [source_code.split('\n')[-1]]

with open('notebooks/09_risk_index.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Synchronized notebook cell 15 with clean script!")
