import json

with open('notebooks/09_risk_index.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for idx, cell in enumerate(nb['cells']):
    src = ''.join(cell.get('source', []))
    if 'lagos_flood_risk_interactive.html' in src or 'cartocdn' in src:
        print(f"Cell {idx}: type={cell.get('cell_type')}")
        print(src[:400])
        print("="*60)
