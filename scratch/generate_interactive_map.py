import json
from pathlib import Path
import geopandas as gpd
import pandas as pd

# 1. Load data
LGA_PATH = Path("data/clean/lagos_lgas.gpkg")
FRI_PATH = Path("data/clean/flood_risk_index_lga.csv")
OUT_HTML = Path("outputs/maps/lagos_flood_risk_interactive.html")

lagos = gpd.read_file(LGA_PATH)
df_fri = pd.read_csv(FRI_PATH)

lagos_wgs84 = lagos.to_crs("EPSG:4326").copy()
lagos_wgs84["geometry"] = lagos_wgs84.geometry.simplify(0.0008, preserve_topology=True)

# 2. Build dictionary of metrics by LGA and Scenario__Period
records_by_lga = {}
for lga_name, grp in df_fri.groupby("lga"):
    d = {}
    for _, r in grp.iterrows():
        key = f"{r['scenario']}__{r['period']}"
        d[key] = {
            "fri": float(round(r["fri_score"], 1)),
            "fri_min": float(round(r["fri_min"], 1)),
            "fri_max": float(round(r["fri_max"], 1)),
            "tier": str(r["risk_tier"]),
            "rank": int(r["lga_rank"]),
            "wet_prob": float(round(r["wet_season_prob_pct"], 1)),
            "wet_min": float(round(r["wet_season_min_pct"], 1)),
            "wet_max": float(round(r["wet_season_max_pct"], 1)),
            "annual_prob": float(round(r["mean_prob_pct"], 1)),
            "exp_months": float(round(r["exp_flood_months_yr"], 1)),
            "pop": int(r["population"]),
            "exp_pop": int(r["exposed_population"]),
            "elev": float(round(r["elev_mean_base"], 1)),
            "low5": float(round(r["low5_share"] * 100, 1)),
            "low10": float(round(r.get("low10_share", 0) * 100, 1)),
            "built": float(round(r["built_share"] * 100, 1)),
            "mangrove": float(round(r.get("wetland_mangrove_share", 0) * 100, 1)),
            "rain_mm": float(round(r["annual_rain_mm"], 0)),
            "slr_m": float(round(r["slr_m"], 2)),
        }
    records_by_lga[lga_name] = d

# 3. Embed metrics into GeoJSON features
geojson_dict = json.loads(lagos_wgs84.to_json())
for feat in geojson_dict["features"]:
    lga_n = feat["properties"]["lga"]
    feat["properties"]["metrics"] = records_by_lga.get(lga_n, {})

# 4. Generate standalone HTML map
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Lagos State Spatio-Temporal Flood Risk Explorer (2010&ndash;2050)</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <!-- Leaflet CSS & JS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
  <style>
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #0f172a; color: #1e293b; overflow: hidden; }}
    #header {{ background: #0b1329; color: #f8fafc; padding: 12px 24px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #1e293b; height: 60px; }}
    #header h1 {{ margin: 0; font-size: 18px; font-weight: 700; letter-spacing: -0.3px; color: #f1f5f9; }}
    #header p {{ margin: 2px 0 0 0; font-size: 12px; color: #94a3b8; }}
    .header-badge {{ display: inline-flex; align-items: center; background: #1e293b; border: 1px solid #334155; padding: 4px 10px; border-radius: 9999px; font-size: 11px; color: #38bdf8; font-weight: 600; }}
    #container {{ display: flex; height: calc(100vh - 60px); }}
    #map {{ flex: 1; height: 100%; position: relative; background: #e2e8f0; }}
    #sidebar {{ width: 400px; background: #ffffff; border-left: 1px solid #cbd5e1; padding: 16px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; box-shadow: -3px 0 16px rgba(0,0,0,0.06); }}
    .ctrl-group {{ display: flex; flex-direction: column; gap: 4px; }}
    .ctrl-label {{ font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: #475569; }}
    select {{ width: 100%; padding: 8px 10px; border-radius: 6px; border: 1px solid #cbd5e1; font-size: 13px; background: #f8fafc; font-weight: 600; color: #0f172a; cursor: pointer; outline: none; }}
    select:focus {{ border-color: #2563eb; ring: 2px solid #93c5fd; }}
    .card {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; transition: all 0.2s; }}
    .card h3 {{ margin: 0 0 6px 0; font-size: 14px; color: #0f172a; font-weight: 700; display: flex; justify-content: space-between; align-items: center; }}
    .badge-tier {{ padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700; text-transform: uppercase; color: #fff; }}
    .stat-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 11.5px; margin-top: 8px; }}
    .stat-box {{ background: #ffffff; padding: 8px 10px; border-radius: 6px; border: 1px solid #e2e8f0; }}
    .stat-val {{ font-size: 15px; font-weight: 700; color: #0f172a; display: block; margin-bottom: 1px; }}
    .stat-sub {{ font-size: 10.5px; color: #64748b; }}
    .table-container {{ max-height: 260px; overflow-y: auto; border: 1px solid #e2e8f0; border-radius: 6px; background: #fff; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 11.5px; text-align: left; }}
    th {{ position: sticky; top: 0; background: #f1f5f9; color: #475569; font-weight: 700; padding: 6px 8px; border-bottom: 1px solid #cbd5e1; z-index: 1; }}
    td {{ padding: 6px 8px; border-bottom: 1px solid #f1f5f9; cursor: pointer; }}
    tr:hover td {{ background: #eff6ff; }}
    tr.active-row td {{ background: #dbeafe !important; font-weight: 600; }}
    .legend {{ background: rgba(255, 255, 255, 0.95); padding: 10px 14px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.18); font-size: 11.5px; line-height: 20px; border: 1px solid #e2e8f0; }}
    .legend-title {{ font-weight: 700; margin-bottom: 4px; color: #0f172a; font-size: 12px; }}
    .legend i {{ width: 14px; height: 14px; float: left; margin-right: 8px; opacity: 0.9; border-radius: 2px; border: 1px solid rgba(0,0,0,0.15); }}
    .reset-btn {{ position: absolute; top: 12px; left: 52px; z-index: 1000; background: #fff; border: 2px solid rgba(0,0,0,0.2); border-radius: 4px; padding: 5px 10px; font-size: 11.5px; font-weight: 600; color: #334155; cursor: pointer; box-shadow: 0 1px 5px rgba(0,0,0,0.2); }}
    .reset-btn:hover {{ background: #f1f5f9; color: #0f172a; }}
  </style>
</head>
<body>
  <div id="header">
    <div>
      <h1>Lagos State Spatio-Temporal Flood Risk Explorer (2010&ndash;2050)</h1>
      <p>CatBoost Susceptibility & CMIP6 Climate Projections (5-GCM NEX-GDDP Ensemble, SSP2-4.5 & SSP5-8.5)</p>
    </div>
    <div>
      <span class="header-badge">20 LGAs &bull; 140 Climate Runs &bull; Zero Watermarks</span>
    </div>
  </div>
  <div id="container">
    <div id="map">
      <button class="reset-btn" id="resetZoomBtn" title="Reset Map View">&#8635; Reset Zoom</button>
    </div>
    <div id="sidebar">
      <div class="ctrl-group">
        <label class="ctrl-label" for="periodSelect">Climate Scenario & Time Horizon</label>
        <select id="periodSelect">
          <option value="Historical__Baseline (2010-2025)">Historical Baseline (2010&ndash;2025)</option>
          <option value="ssp245__2030s (2030-2039)">2030s (2030&ndash;2039) &ndash; SSP2-4.5 (Moderate)</option>
          <option value="ssp245__2040s (2040-2049)">2040s (2040&ndash;2049) &ndash; SSP2-4.5 (Moderate)</option>
          <option value="ssp245__2050 (2046-2050)">2050 (2046&ndash;2050) &ndash; SSP2-4.5 (Moderate)</option>
          <option value="ssp585__2030s (2030-2039)">2030s (2030&ndash;2039) &ndash; SSP5-8.5 (High Emissions)</option>
          <option value="ssp585__2040s (2040-2049)">2040s (2040&ndash;2049) &ndash; SSP5-8.5 (High Emissions)</option>
          <option value="ssp585__2050 (2046-2050)" selected>2050 (2046&ndash;2050) &ndash; SSP5-8.5 (High Emissions)</option>
        </select>
      </div>

      <div class="ctrl-group">
        <label class="ctrl-label" for="lgaSelect">Quick Jump to LGA</label>
        <select id="lgaSelect">
          <option value="">-- Select an LGA to focus --</option>
        </select>
      </div>

      <div class="card" id="lgaDetail">
        <h3>LGA Risk Dossier</h3>
        <p style="font-size:12px;color:#64748b;margin:0;">Hover or click any LGA polygon on the map, or select from the dropdown above to inspect detailed multi-hazard projections.</p>
      </div>

      <div class="card" style="padding: 10px 12px; flex: 1; display: flex; flex-direction: column;">
        <h3 style="margin-bottom:8px;">LGA Risk Rankings <span style="font-size:11px;font-weight:normal;color:#64748b;">(Click row to focus)</span></h3>
        <div class="table-container">
          <table id="rankTable">
            <thead>
              <tr>
                <th>#</th>
                <th>LGA</th>
                <th>FRI</th>
                <th>Wet Prob</th>
                <th>Exp. Pop</th>
              </tr>
            </thead>
            <tbody></tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

  <script>
    const geoData = {json.dumps(geojson_dict)};
    const initialCenter = [6.52, 3.58];
    const initialZoom = 10;

    // 1. Initialize Map
    const map = L.map('map', {{
      center: initialCenter,
      zoom: initialZoom,
      zoomControl: true
    }});

    // 2. High-performance, 100% Free, Non-watermarked Basemap Layers (Zero API Key)
    const baseLight = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{{z}}/{{y}}/{{x}}', {{
      attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ',
      maxZoom: 16
    }});

    const baseOSM = L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      maxZoom: 18
    }});

    const baseSatellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{{z}}/{{y}}/{{x}}', {{
      attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
      maxZoom: 18
    }});

    const baseTopo = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{{z}}/{{y}}/{{x}}', {{
      attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, USGS, FAO, NPS, NRCAN',
      maxZoom: 18
    }});

    // Add default basemap
    baseLight.addTo(map);

    // Layer control
    const baseMaps = {{
      "Clean Light Canvas": baseLight,
      "OpenStreetMap": baseOSM,
      "Satellite Imagery": baseSatellite,
      "Topographic Map": baseTopo
    }};
    L.control.layers(baseMaps, null, {{ position: 'topright' }}).addTo(map);

    // 3. Color styling based on FRI
    function getColor(fri) {{
      return fri >= 62 ? '#b91c1c' : // Very High (Red)
             fri >= 52 ? '#ea580c' : // High (Orange-Red)
             fri >= 42 ? '#f59e0b' : // Elevated (Amber)
             fri >= 32 ? '#facc15' : // Moderate (Yellow)
                         '#84cc16';  // Low (Lime)
    }}

    function getTierColor(tier) {{
      if (tier === 'Very High') return '#b91c1c';
      if (tier === 'High') return '#ea580c';
      if (tier === 'Elevated') return '#d97706';
      if (tier === 'Moderate') return '#ca8a04';
      return '#65a30d';
    }}

    let geojsonLayer;
    let layerByLga = {{}};
    let selectedLga = null;
    const periodSelect = document.getElementById('periodSelect');
    const lgaSelect = document.getElementById('lgaSelect');

    // Populate LGA Quick Selector dropdown
    const lgaList = geoData.features.map(f => f.properties.lga).sort();
    lgaList.forEach(lga => {{
      const opt = document.createElement('option');
      opt.value = lga;
      opt.textContent = lga;
      lgaSelect.appendChild(opt);
    }});

    // Update Detail Dossier Card
    function updateDetails(lgaName, m) {{
      if (!m) return;
      selectedLga = lgaName;
      lgaSelect.value = lgaName;

      // Highlight active row in ranking table
      document.querySelectorAll('#rankTable tbody tr').forEach(tr => {{
        if (tr.getAttribute('data-lga') === lgaName) {{
          tr.classList.add('active-row');
          tr.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
        }} else {{
          tr.classList.remove('active-row');
        }}
      }});

      const tierColor = getTierColor(m.tier);
      document.getElementById('lgaDetail').innerHTML = `
        <h3>
          <span>${{lgaName}}</span>
          <span class="badge-tier" style="background:${{tierColor}};">${{m.tier}} (Rank #${{m.rank}})</span>
        </h3>
        <div class="stat-grid">
          <div class="stat-box">
            <span class="stat-val" style="color:${{tierColor}};">${{m.fri.toFixed(1)}} / 100</span>
            <span class="stat-sub">FRI Range: ${{m.fri_min.toFixed(1)}} &ndash; ${{m.fri_max.toFixed(1)}}</span>
          </div>
          <div class="stat-box">
            <span class="stat-val">${{m.wet_prob.toFixed(1)}}%</span>
            <span class="stat-sub">Wet-Season (5-GCM: ${{m.wet_min.toFixed(1)}}&ndash;${{m.wet_max.toFixed(1)}}%)</span>
          </div>
          <div class="stat-box">
            <span class="stat-val">${{m.exp_pop.toLocaleString()}}</span>
            <span class="stat-sub">Exposed (${{((m.exp_pop / m.pop) * 100).toFixed(1)}}% of ${{m.pop.toLocaleString()}})</span>
          </div>
          <div class="stat-box">
            <span class="stat-val">${{m.elev.toFixed(1)}} m</span>
            <span class="stat-sub">Elevation (${{m.low5}}% &lt; 5m, ${{m.low10}}% &lt; 10m)</span>
          </div>
          <div class="stat-box">
            <span class="stat-val">${{m.built}}%</span>
            <span class="stat-sub">Built Urban Footprint</span>
          </div>
          <div class="stat-box">
            <span class="stat-val">${{m.exp_months.toFixed(1)}} mo/yr</span>
            <span class="stat-sub">Expected Flood Inundation</span>
          </div>
        </div>
      `;
    }}

    // Zoom and highlight LGA
    function focusLga(lgaName) {{
      const layer = layerByLga[lgaName];
      if (layer) {{
        map.fitBounds(layer.getBounds(), {{ padding: [30, 30], maxZoom: 13, animate: true }});
        const key = periodSelect.value;
        const feat = geoData.features.find(f => f.properties.lga === lgaName);
        if (feat) {{
          updateDetails(lgaName, feat.properties.metrics[key]);
          highlightLayer(layer);
        }}
      }}
    }}

    let currentlyHighlighted = null;
    function highlightLayer(layer) {{
      if (currentlyHighlighted && geojsonLayer) {{
        geojsonLayer.resetStyle(currentlyHighlighted);
      }}
      layer.setStyle({{
        weight: 3.5,
        color: '#0f172a',
        fillOpacity: 0.88,
        dashArray: ''
      }});
      if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {{
        layer.bringToFront();
      }}
      currentlyHighlighted = layer;
    }}

    // Render Choropleth
    function renderLayer() {{
      const key = periodSelect.value;
      if (geojsonLayer) map.removeLayer(geojsonLayer);
      layerByLga = {{}};
      currentlyHighlighted = null;

      const rows = [];
      geojsonLayer = L.geoJson(geoData, {{
        style: function(feature) {{
          const m = feature.properties.metrics[key];
          return {{
            fillColor: getColor(m ? m.fri : 0),
            weight: 1.5,
            opacity: 1,
            color: '#334155',
            fillOpacity: 0.75
          }};
        }},
        onEachFeature: function(feature, layer) {{
          const lga = feature.properties.lga;
          layerByLga[lga] = layer;
          const m = feature.properties.metrics[key];
          if (m) rows.push({{ lga, ...m }});

          layer.bindTooltip(`
            <div style="font-size:12px;line-height:1.4;">
              <b style="font-size:13px;color:#0f172a;">${{lga}}</b><br/>
              <b>FRI:</b> ${{m ? m.fri.toFixed(1) : 'N/A'}} (${{m ? m.tier : ''}})<br/>
              <b>Wet-Season Prob:</b> ${{m ? m.wet_prob.toFixed(1) : 0}}%<br/>
              <b>Exposed Pop:</b> ${{m ? m.exp_pop.toLocaleString() : 0}}
            </div>
          `, {{ sticky: true, opacity: 0.95 }});

          layer.on({{
            mouseover: function(e) {{
              if (currentlyHighlighted !== e.target) {{
                e.target.setStyle({{ weight: 2.5, color: '#0f172a', fillOpacity: 0.85 }});
              }}
            }},
            mouseout: function(e) {{
              if (currentlyHighlighted !== e.target) {{
                geojsonLayer.resetStyle(e.target);
              }}
            }},
            click: function(e) {{
              focusLga(lga);
            }}
          }});
        }}
      }}).addTo(map);

      // Populate Ranking Table
      rows.sort((a, b) => b.fri - a.fri);
      const tbody = document.querySelector('#rankTable tbody');
      tbody.innerHTML = rows.map((r, idx) => `
        <tr data-lga="${{r.lga}}">
          <td><b>${{idx + 1}}</b></td>
          <td><b>${{r.lga}}</b></td>
          <td><span style="color:${{getTierColor(r.tier)}};font-weight:700;">${{r.fri.toFixed(1)}}</span></td>
          <td>${{r.wet_prob.toFixed(1)}}%</td>
          <td>${{Math.round(r.exp_pop / 1000).toLocaleString()}}k</td>
        </tr>
      `).join('');

      // Add table click handler
      tbody.querySelectorAll('tr').forEach(tr => {{
        tr.addEventListener('click', function() {{
          const lga = this.getAttribute('data-lga');
          focusLga(lga);
        }});
      }});

      // Retain or select top LGA
      const targetLga = selectedLga || (rows.length > 0 ? rows[0].lga : null);
      if (targetLga) {{
        const targetFeat = geoData.features.find(f => f.properties.lga === targetLga);
        if (targetFeat) updateDetails(targetLga, targetFeat.properties.metrics[key]);
      }}
    }}

    // Reset zoom button
    document.getElementById('resetZoomBtn').addEventListener('click', () => {{
      map.setView(initialCenter, initialZoom, {{ animate: true }});
      if (currentlyHighlighted && geojsonLayer) {{
        geojsonLayer.resetStyle(currentlyHighlighted);
        currentlyHighlighted = null;
      }}
      lgaSelect.value = '';
    }});

    // Dropdown change handlers
    periodSelect.addEventListener('change', () => {{
      renderLayer();
    }});

    lgaSelect.addEventListener('change', (e) => {{
      if (e.target.value) {{
        focusLga(e.target.value);
      }} else {{
        map.setView(initialCenter, initialZoom, {{ animate: true }});
      }}
    }});

    // Legend Control
    const legend = L.control({{ position: 'bottomleft' }});
    legend.onAdd = function() {{
      const div = L.DomUtil.create('div', 'legend');
      div.innerHTML = `
        <div class="legend-title">Flood Risk Index (FRI)</div>
        <div><i style="background:#b91c1c"></i> 62+ (Very High)</div>
        <div><i style="background:#ea580c"></i> 52 &ndash; 62 (High)</div>
        <div><i style="background:#f59e0b"></i> 42 &ndash; 52 (Elevated)</div>
        <div><i style="background:#facc15"></i> 32 &ndash; 42 (Moderate)</div>
        <div><i style="background:#84cc16"></i> &lt; 32 (Low)</div>
      `;
      return div;
    }};
    legend.addTo(map);

    // Initial render
    renderLayer();
  </script>
</body>
</html>
"""

OUT_HTML.write_text(html_content, encoding="utf-8")
print(f"Successfully generated updated interactive map at: {OUT_HTML.resolve()} ({OUT_HTML.stat().st_size / 1024:.1f} KB)")
