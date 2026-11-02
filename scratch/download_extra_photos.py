import urllib.request, time
from pathlib import Path

out_dir = Path('outputs/figures/photos')
out_dir.mkdir(parents=True, exist_ok=True)

photos = {
    'photo_07_street_flood_deep.jpg': 'https://upload.wikimedia.org/wikipedia/commons/f/f2/Street_Flood.jpg',
    'photo_08_broken_down_car_flood.jpg': 'https://upload.wikimedia.org/wikipedia/commons/c/c2/A_broken_down_car.jpg',
    'photo_09_lekki_flooding_residential_2024.jpg': 'https://upload.wikimedia.org/wikipedia/commons/2/2d/Lekki_flooding_2.jpg',
    'photo_10_no_proper_drainage_unpaved.jpg': 'https://upload.wikimedia.org/wikipedia/commons/0/07/No_Proper_Drainage_2.jpg',
    'photo_11_swamp_lekki_conservation.jpg': 'https://upload.wikimedia.org/wikipedia/commons/f/fc/A_flooded_building_in_the_swampy_waters_of_the_lekki_conservation_park_in_Lagos.jpg',
    'photo_12_feeder_road_mazamaza.jpg': 'https://upload.wikimedia.org/wikipedia/commons/d/d2/FEEDER_ROAD_IN_NIGERIA_MAZAMAZA.jpg'
}

for fname, url in photos.items():
    dest = out_dir / fname
    if not dest.exists():
        time.sleep(2)
        req = urllib.request.Request(url, headers={'User-Agent': 'LagosFloodStudy/1.0 (academic research; contact@lagosstudy.org)'})
        try:
            with urllib.request.urlopen(req) as resp, open(dest, 'wb') as f:
                f.write(resp.read())
            print(f'Downloaded {fname}: {dest.stat().st_size / 1024:.1f} KB')
        except Exception as e:
            print(f'Failed {fname}: {e}')
    else:
        print(f'Already exists: {fname}')
