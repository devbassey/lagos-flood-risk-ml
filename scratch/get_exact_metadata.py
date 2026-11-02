import urllib.request, json, re

titles = [
    'File:Lekki_flooding_2024.jpg',
    'File:Flooded_road_in_Lagos.jpg',
    'File:Lagos_Street_at_high_tide.jpg',
    'File:Extremely_blocked_drainage,_in_Lagos_state.jpg',
    'File:Lagos_drainage_services.jpg',
    'File:Iba_town_in_ojo_area,_Lagos_state.jpg',
    'File:A_broken_down_car.jpg',
    'File:Street_Flood.jpg',
    'File:Lekki_flooding_2.jpg',
    'File:No_Proper_Drainage_2.jpg',
    'File:A_flooded_building_in_the_swampy_waters_of_the_lekki_conservation_park_in_Lagos.jpg',
    'File:FEEDER_ROAD_IN_NIGERIA_MAZAMAZA.jpg'
]

url = 'https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=imageinfo&iiprop=url|extmetadata&titles=' + '|'.join(titles)
req = urllib.request.Request(url, headers={'User-Agent': 'LagosFloodStudy/1.0 (academic research; contact@lagosstudy.org)'})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))

pages = data.get('query', {}).get('pages', {})
for pid, p in sorted(pages.items(), key=lambda x: x[1].get('title', '')):
    title = p.get('title')
    info = p.get('imageinfo', [{}])[0]
    meta = info.get('extmetadata', {})
    artist = meta.get('Artist', {}).get('value', 'Unknown')
    artist_clean = re.sub(r'<[^>]+>', '', artist).strip()
    date = meta.get('DateTimeOriginal', {}).get('value', meta.get('DateTime', {}).get('value', 'Unknown')).strip()
    license_name = meta.get('LicenseShortName', {}).get('value', 'CC BY-SA 4.0').strip()
    desc = meta.get('ImageDescription', {}).get('value', '').strip()
    desc_clean = re.sub(r'<[^>]+>', '', desc).strip()[:100]
    page_url = info.get('descriptionurl', '')
    print(f'TITLE: {title}')
    print(f'  Artist: {artist_clean}')
    print(f'  Date: {date}')
    print(f'  License: {license_name}')
    print(f'  Desc: {desc_clean}')
    print(f'  Page URL: {page_url}')
