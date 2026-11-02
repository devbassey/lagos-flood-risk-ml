import urllib.request, json, time
from pathlib import Path

titles = [
    'File:Lekki_flooding.jpg',
    'File:Lekki_flooding_2.jpg',
    'File:Street_Flood.jpg',
    'File:Flooded_area_during_rainy_season_in_Nigeria.jpg',
    'File:FEEDER_ROAD_IN_NIGERIA_MAZAMAZA.jpg',
    'File:No_Proper_Drainage_2.jpg',
    'File:Swimming_Car.jpg',
    'File:A_broken_down_car.jpg',
    'File:A_flooded_building_in_the_swampy_waters_of_the_lekki_conservation_park_in_Lagos.jpg',
    'File:Intense_Rainfall.jpg'
]

url = 'https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=imageinfo&iiprop=url|size|extmetadata&titles=' + '|'.join(titles)
req = urllib.request.Request(url, headers={'User-Agent': 'LagosFloodStudy/1.0 (academic research; contact@lagosstudy.org)'})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))

out_dir = Path('outputs/figures/photos')
out_dir.mkdir(parents=True, exist_ok=True)

for pid, p in data['query']['pages'].items():
    title = p.get('title')
    info = p.get('imageinfo', [{}])[0]
    meta = info.get('extmetadata', {})
    desc = meta.get('ImageDescription', {}).get('value', '')[:120]
    date = meta.get('DateTimeOriginal', {}).get('value', 'Unknown')
    img_url = info.get('url')
    w = info.get('width')
    h = info.get('height')
    print(f'{title} | {w}x{h} | {date}')
    print(f'  URL: {img_url}')
    print(f'  Desc: {desc}')
