import streamlit as st
import pandas as pd
import pydeck as pdk
import h3
import random
from snowflake.snowpark.context import get_active_session
from utils.styles import render_common_styles, render_page_header

st.set_page_config(page_title="Map Visualization | BICS", page_icon=":material/map:", layout="wide")

st.logo("logo.png")
render_common_styles()
render_page_header("Map Visualization", "H3 hexagon visualization of foot traffic density")

if 'show_anomalies' not in st.session_state:
    st.session_state.show_anomalies = False
if 'selected_city' not in st.session_state:
    st.session_state.selected_city = "Brussels"
if 'show_flow_arcs' not in st.session_state:
    st.session_state.show_flow_arcs = False
if 'show_hotspots' not in st.session_state:
    st.session_state.show_hotspots = False
if 'show_pois' not in st.session_state:
    st.session_state.show_pois = True
if 'show_demographics' not in st.session_state:
    st.session_state.show_demographics = False

CITY_CENTERS = {
    "Brussels": {"lat": 50.8503, "lon": 4.3517},
    "Antwerp": {"lat": 51.2194, "lon": 4.4025},
    "Ghent": {"lat": 51.0543, "lon": 3.7174},
    "Charleroi": {"lat": 50.4108, "lon": 4.4446},
    "Liege": {"lat": 50.6326, "lon": 5.5797},
    "Bruges": {"lat": 51.2093, "lon": 3.2247},
    "Namur": {"lat": 50.4674, "lon": 4.8720},
    "Leuven": {"lat": 50.8798, "lon": 4.7005},
    "Mons": {"lat": 50.4542, "lon": 3.9563},
    "Mechelen": {"lat": 51.0259, "lon": 4.4776},
    "Hasselt": {"lat": 50.9307, "lon": 5.3375},
    "Kortrijk": {"lat": 50.8279, "lon": 3.2649},
    "Ostend": {"lat": 51.2254, "lon": 2.9187},
    "Arlon": {"lat": 49.6835, "lon": 5.8167},
}

AGE_GROUPS = ["18-24", "25-34", "35-44", "45-54", "55+"]
GENDERS = ["Male", "Female"]
NATIONALITIES = ["Belgian", "French", "Dutch", "Moroccan", "Turkish", "Italian", "Romanian", "Polish", "German", "Portuguese", "Other"]

DEMOGRAPHIC_COLORS = {
    "18-24": [65, 105, 225, 200],
    "25-34": [30, 144, 255, 200],
    "35-44": [0, 191, 255, 200],
    "45-54": [135, 206, 250, 200],
    "55+": [176, 224, 230, 200],
    "Male": [8, 145, 178, 200],
    "Female": [219, 112, 147, 200],
    "Belgian": [0, 0, 0, 200],
    "French": [0, 35, 149, 200],
    "Dutch": [255, 79, 0, 200],
    "Moroccan": [0, 100, 0, 200],
    "Turkish": [227, 10, 23, 200],
    "Italian": [0, 140, 69, 200],
    "Romanian": [0, 43, 127, 200],
    "Polish": [220, 20, 60, 200],
    "German": [255, 206, 0, 200],
    "Portuguese": [0, 102, 0, 200],
    "Other": [128, 128, 128, 200],
}

POI_DATA = {
    "Brussels": [
        {"name": "Brussels Airport (BRU)", "lat": 50.9014, "lon": 4.4844, "type": "airport", "icon": "✈️"},
        {"name": "Grand Place", "lat": 50.8467, "lon": 4.3525, "type": "landmark", "icon": "🏛️"},
        {"name": "City2 Shopping", "lat": 50.8535, "lon": 4.3560, "type": "mall", "icon": "🛍️"},
        {"name": "Atomium", "lat": 50.8950, "lon": 4.3416, "type": "landmark", "icon": "🏛️"},
        {"name": "King Baudouin Stadium", "lat": 50.8957, "lon": 4.3356, "type": "stadium", "icon": "🏟️"},
        {"name": "European Parliament", "lat": 50.8384, "lon": 4.3730, "type": "landmark", "icon": "🏛️"},
    ],
    "Antwerp": [
        {"name": "Antwerp Central Station", "lat": 51.2172, "lon": 4.4212, "type": "landmark", "icon": "🚂"},
        {"name": "Stadsfeestzaal", "lat": 51.2188, "lon": 4.4010, "type": "mall", "icon": "🛍️"},
        {"name": "MAS Museum", "lat": 51.2291, "lon": 4.4050, "type": "landmark", "icon": "🏛️"},
        {"name": "Sportpaleis", "lat": 51.2316, "lon": 4.4363, "type": "stadium", "icon": "🏟️"},
        {"name": "Wijnegem Shopping", "lat": 51.2350, "lon": 4.4912, "type": "mall", "icon": "🛍️"},
    ],
    "Ghent": [
        {"name": "Gravensteen Castle", "lat": 51.0575, "lon": 3.7208, "type": "landmark", "icon": "🏛️"},
        {"name": "Ghent Sint-Pieters Station", "lat": 51.0363, "lon": 3.7108, "type": "landmark", "icon": "🚂"},
        {"name": "Shopping Gent Zuid", "lat": 51.0416, "lon": 3.7246, "type": "mall", "icon": "🛍️"},
    ],
    "Bruges": [
        {"name": "Markt Square", "lat": 51.2089, "lon": 3.2247, "type": "landmark", "icon": "🏛️"},
        {"name": "Belfry of Bruges", "lat": 51.2083, "lon": 3.2247, "type": "landmark", "icon": "🏛️"},
        {"name": "Bruges Station", "lat": 51.1976, "lon": 3.2168, "type": "landmark", "icon": "🚂"},
    ],
    "Liege": [
        {"name": "Liege-Guillemins Station", "lat": 50.6243, "lon": 5.5664, "type": "landmark", "icon": "🚂"},
        {"name": "Mediacite Shopping", "lat": 50.6318, "lon": 5.5942, "type": "mall", "icon": "🛍️"},
        {"name": "Liege Airport (LGG)", "lat": 50.6374, "lon": 5.4432, "type": "airport", "icon": "✈️"},
    ],
}

def get_pois_for_city(city):
    if city in POI_DATA:
        return pd.DataFrame(POI_DATA[city])
    return pd.DataFrame()

def generate_flow_arcs(hex_df, city, num_arcs=15, seed=42):
    if len(hex_df) < 10:
        return pd.DataFrame()
    
    random.seed(seed)
    
    top_hexes = hex_df.nlargest(20, 'TRAFFIC_COUNT').reset_index(drop=True)
    arcs = []
    n = len(top_hexes)
    
    for i in range(num_arcs):
        src_idx = random.randint(0, n - 1)
        tgt_idx = random.randint(0, n - 1)
        source = top_hexes.iloc[src_idx]
        target = top_hexes.iloc[tgt_idx]
        
        if source['HEXAGON_ID'] != target['HEXAGON_ID']:
            flow_volume = random.randint(500, 5000)
            arcs.append({
                'source_lat': source['lat'],
                'source_lon': source['lon'],
                'target_lat': target['lat'],
                'target_lon': target['lon'],
                'flow_volume': flow_volume,
                'source_name': f"Zone {source['HEXAGON_ID'][:8]}",
                'target_name': f"Zone {target['HEXAGON_ID'][:8]}",
            })
    
    if city in POI_DATA and len(top_hexes) > 0:
        pois = POI_DATA[city]
        for j, poi in enumerate(pois[:3]):
            src_idx = random.randint(0, n - 1)
            source = top_hexes.iloc[src_idx]
            flow_volume = random.randint(1000, 8000)
            arcs.append({
                'source_lat': source['lat'],
                'source_lon': source['lon'],
                'target_lat': poi['lat'],
                'target_lon': poi['lon'],
                'flow_volume': flow_volume,
                'source_name': f"Zone {source['HEXAGON_ID'][:8]}",
                'target_name': poi['name'],
            })
    
    return pd.DataFrame(arcs)

def generate_hotspots(hex_df, num_hotspots=8, seed=42):
    if len(hex_df) < num_hotspots:
        return pd.DataFrame()
    
    random.seed(seed)
    top_hexes = hex_df.nlargest(num_hotspots * 2, 'TRAFFIC_COUNT').sample(num_hotspots, random_state=seed)
    
    hotspots = []
    for _, row in top_hexes.iterrows():
        intensity = row['normalized']
        hotspots.append({
            'lat': row['lat'],
            'lon': row['lon'],
            'intensity': intensity,
            'traffic': row['TRAFFIC_COUNT'],
            'radius': 200 + (intensity * 400),
            'inner_radius': 100 + (intensity * 200),
        })
    
    return pd.DataFrame(hotspots)

def detect_anomalies(df):
    anomalies = []
    traffic_mean = df['TRAFFIC_COUNT'].mean()
    traffic_std = df['TRAFFIC_COUNT'].std()
    dwell_mean = df['AVG_DWELL'].mean()
    dwell_std = df['AVG_DWELL'].std()
    
    traffic_high_thresh = traffic_mean + 2 * traffic_std
    traffic_low_thresh = max(traffic_mean - 1.5 * traffic_std, df['TRAFFIC_COUNT'].quantile(0.05))
    dwell_high_thresh = dwell_mean + 2 * dwell_std
    dwell_low_thresh = max(dwell_mean - 1.5 * dwell_std, 1)
    
    for _, row in df.iterrows():
        reasons = []
        severity = 0
        anomaly_type = None
        
        high_traffic = row['TRAFFIC_COUNT'] > traffic_high_thresh
        low_traffic = row['TRAFFIC_COUNT'] < traffic_low_thresh
        high_dwell = row['AVG_DWELL'] > dwell_high_thresh
        low_dwell = row['AVG_DWELL'] < dwell_low_thresh
        
        if high_traffic and high_dwell:
            anomaly_type = "Congestion Hotspot"
            reasons.append(f"Traffic {row['TRAFFIC_COUNT']:,.0f} ({((row['TRAFFIC_COUNT']-traffic_mean)/traffic_std):.1f}σ above avg)")
            reasons.append(f"Dwell {row['AVG_DWELL']:.1f}min ({((row['AVG_DWELL']-dwell_mean)/dwell_std):.1f}σ above avg)")
            severity = 3
        elif high_traffic and low_dwell:
            anomaly_type = "Rapid Transit Zone"
            reasons.append(f"High traffic ({row['TRAFFIC_COUNT']:,.0f}) but very short dwell ({row['AVG_DWELL']:.1f}min)")
            severity = 2
        elif low_traffic and high_dwell:
            anomaly_type = "Unusual Gathering"
            reasons.append(f"Low traffic ({row['TRAFFIC_COUNT']:,.0f}) but extended dwell ({row['AVG_DWELL']:.1f}min)")
            severity = 2
        elif high_traffic:
            anomaly_type = "Traffic Spike"
            reasons.append(f"Traffic {((row['TRAFFIC_COUNT']-traffic_mean)/traffic_std):.1f}σ above average")
            severity = 1
        elif high_dwell:
            anomaly_type = "Extended Dwell"
            reasons.append(f"Dwell time {((row['AVG_DWELL']-dwell_mean)/dwell_std):.1f}σ above average")
            severity = 1
        
        if anomaly_type:
            anomalies.append({
                'HEXAGON_ID': row['HEXAGON_ID'],
                'lat': row['lat'],
                'lon': row['lon'],
                'TRAFFIC_COUNT': row['TRAFFIC_COUNT'],
                'AVG_DWELL': row['AVG_DWELL'],
                'anomaly_type': anomaly_type,
                'reasons': " | ".join(reasons),
                'severity': severity
            })
    
    return pd.DataFrame(anomalies) if anomalies else pd.DataFrame()

@st.cache_data(ttl=600)
def get_hexagon_data(city, hour):
    session = get_active_session()
    where_clauses = [f"HOUR = {hour}"]
    if city != "All Cities":
        where_clauses.append(f"SUBSCRIBER_HOME_CITY = '{city}'")
    where_sql = " AND ".join(where_clauses)
    query = f"""
        SELECT HEXAGON_ID, 
               COUNT(*) as TRAFFIC_COUNT,
               AVG(AVG_STAYING_DURATION_MIN) as AVG_DWELL
        FROM BICS_TELCO.MOBILITY_DATA.BICS_TELCO_MOBILITY_DATA
        WHERE {where_sql}
        GROUP BY HEXAGON_ID
        ORDER BY TRAFFIC_COUNT DESC
        LIMIT 5000
    """
    return session.sql(query).to_pandas()

@st.cache_data(ttl=600)
def get_combined_demographic_data(city, hour, ages, genders, nationalities):
    session = get_active_session()
    where_clauses = [f"HOUR = {hour}"]
    if city != "All Cities":
        where_clauses.append(f"SUBSCRIBER_HOME_CITY = '{city}'")
    
    if ages:
        age_list = ",".join([f"'{a}'" for a in ages])
        where_clauses.append(f"AGE_GROUP IN ({age_list})")
    if genders:
        gender_list = ",".join([f"'{g}'" for g in genders])
        where_clauses.append(f"GENDER IN ({gender_list})")
    if nationalities:
        nat_list = ",".join([f"'{n}'" for n in nationalities])
        where_clauses.append(f"NATIONALITY IN ({nat_list})")
    
    where_sql = " AND ".join(where_clauses)
    query = f"""
        SELECT HEXAGON_ID, 
               COUNT(*) as TRAFFIC_COUNT,
               AVG(AVG_STAYING_DURATION_MIN) as AVG_DWELL
        FROM BICS_TELCO.MOBILITY_DATA.BICS_TELCO_MOBILITY_DATA
        WHERE {where_sql}
        GROUP BY HEXAGON_ID
        ORDER BY TRAFFIC_COUNT DESC
        LIMIT 3000
    """
    return session.sql(query).to_pandas()

def h3_to_lat_lon(h3_index):
    try:
        lat, lon = h3.cell_to_latlng(h3_index)
        return lat, lon
    except Exception:
        try:
            lat, lon = h3.h3_to_geo(h3_index)
            return lat, lon
        except Exception:
            return None, None

st.markdown("#### :material/location_on: Quick City Jump")
city_cols = st.columns(7)
quick_cities = ["Brussels", "Antwerp", "Ghent", "Bruges", "Liege", "Leuven", "Namur"]
for i, city in enumerate(quick_cities):
    with city_cols[i]:
        if st.button(city, use_container_width=True, type="secondary" if city != st.session_state.selected_city else "primary"):
            st.session_state.selected_city = city

with st.sidebar:
    st.subheader(":material/tune: Map Controls", anchor=False)
    
    selected_city = st.selectbox(
        "Focus City",
        options=["All Cities"] + list(CITY_CENTERS.keys()),
        index=list(["All Cities"] + list(CITY_CENTERS.keys())).index(st.session_state.selected_city) if st.session_state.selected_city in CITY_CENTERS else 0
    )
    if selected_city != st.session_state.selected_city and selected_city != "All Cities":
        st.session_state.selected_city = selected_city
    
    selected_hour = st.slider(
        "Hour of Day",
        min_value=0,
        max_value=23,
        value=12,
        help="Filter data by hour"
    )
    
    time_label = "AM" if selected_hour < 12 else "PM"
    display_hour = selected_hour if selected_hour <= 12 else selected_hour - 12
    if display_hour == 0:
        display_hour = 12
    st.caption(f"Showing: **{display_hour}:00 {time_label}**")
    
    st.divider()
    
    color_scale = st.selectbox(
        "Color By",
        options=["Traffic Density", "Dwell Time"],
        index=0
    )
    
    st.divider()
    
    st.subheader(":material/group: Demographics", anchor=False)
    
    show_demographics = st.toggle(
        "Enable Demographic Layers",
        value=st.session_state.show_demographics,
        help="Show population segments on the map"
    )
    if show_demographics != st.session_state.show_demographics:
        st.session_state.show_demographics = show_demographics
    
    selected_ages = []
    selected_genders = []
    selected_nationalities = []
    
    if st.session_state.show_demographics:
        st.caption("Select segments to overlay on map:")
        
        selected_ages = st.multiselect(
            "Age Groups",
            options=AGE_GROUPS,
            default=[],
            help="Select age groups to display"
        )
        
        selected_genders = st.multiselect(
            "Gender",
            options=GENDERS,
            default=[],
            help="Select genders to display"
        )
        
        selected_nationalities = st.multiselect(
            "Nationality",
            options=NATIONALITIES,
            default=[],
            help="Select nationalities to display"
        )
        
        filter_parts = []
        if selected_ages:
            filter_parts.append(f"{len(selected_ages)} age(s)")
        if selected_genders:
            filter_parts.append(f"{len(selected_genders)} gender(s)")
        if selected_nationalities:
            filter_parts.append(f"{len(selected_nationalities)} nationality(ies)")
        if filter_parts:
            st.caption(f"Filtering: {' + '.join(filter_parts)}")
    
    st.divider()
    
    st.subheader(":material/layers: Visual Layers", anchor=False)
    
    show_pois = st.toggle(
        "📍 Points of Interest",
        value=st.session_state.show_pois,
        help="Show airports, malls, stations, landmarks"
    )
    if show_pois != st.session_state.show_pois:
        st.session_state.show_pois = show_pois
    
    show_flow_arcs = st.toggle(
        "🌊 Flow Arcs",
        value=st.session_state.show_flow_arcs,
        help="Show movement patterns between zones"
    )
    if show_flow_arcs != st.session_state.show_flow_arcs:
        st.session_state.show_flow_arcs = show_flow_arcs
    
    show_hotspots = st.toggle(
        "🔥 Pulsing Hotspots",
        value=st.session_state.show_hotspots,
        help="Highlight high-traffic areas with pulse effect"
    )
    if show_hotspots != st.session_state.show_hotspots:
        st.session_state.show_hotspots = show_hotspots
    
    st.divider()
    
    st.subheader(":material/warning: Anomaly Detection", anchor=False)
    show_anomalies = st.toggle(
        "Highlight Anomalies",
        value=st.session_state.show_anomalies,
        help="Show unusual traffic patterns in red"
    )
    
    if show_anomalies != st.session_state.show_anomalies:
        st.session_state.show_anomalies = show_anomalies
        st.rerun()
    
    if st.session_state.show_anomalies:
        st.caption(":material/error: Red hexagons = anomalies")

current_city = st.session_state.selected_city if st.session_state.selected_city in CITY_CENTERS else selected_city

with st.spinner("Loading hexagon data..."):
    hex_df = get_hexagon_data(current_city, selected_hour)

if len(hex_df) > 0:
    coords = hex_df['HEXAGON_ID'].apply(h3_to_lat_lon)
    hex_df['lat'] = coords.apply(lambda x: x[0])
    hex_df['lon'] = coords.apply(lambda x: x[1])
    hex_df = hex_df.dropna(subset=['lat', 'lon'])
    
    max_traffic = hex_df['TRAFFIC_COUNT'].max()
    hex_df['normalized'] = hex_df['TRAFFIC_COUNT'] / max_traffic
    
    if color_scale == "Traffic Density":
        hex_df['color_r'] = (hex_df['normalized'] * 8 + (1 - hex_df['normalized']) * 30).astype(int)
        hex_df['color_g'] = (hex_df['normalized'] * 145 + (1 - hex_df['normalized']) * 58).astype(int)
        hex_df['color_b'] = (hex_df['normalized'] * 178 + (1 - hex_df['normalized']) * 95).astype(int)
        hex_df['opacity'] = (hex_df['normalized'] * 200 + 55).astype(int)
        legend_colors = "linear-gradient(90deg, #1E3A5F, #0891B2)"
        legend_label_low = "Low Traffic"
        legend_label_high = "High Traffic"
    else:
        max_dwell = hex_df['AVG_DWELL'].max()
        hex_df['dwell_norm'] = hex_df['AVG_DWELL'] / max_dwell
        hex_df['color_r'] = 212
        hex_df['color_g'] = (hex_df['dwell_norm'] * 175 + (1 - hex_df['dwell_norm']) * 100).astype(int)
        hex_df['color_b'] = (hex_df['dwell_norm'] * 55 + (1 - hex_df['dwell_norm']) * 30).astype(int)
        hex_df['opacity'] = (hex_df['dwell_norm'] * 200 + 55).astype(int)
        legend_colors = "linear-gradient(90deg, #D46420, #D4AF37)"
        legend_label_low = "Short Dwell"
        legend_label_high = "Long Dwell"
    
    if current_city != "All Cities" and current_city in CITY_CENTERS:
        center = CITY_CENTERS[current_city]
        view_lat, view_lon = center["lat"], center["lon"]
        zoom = 12
    else:
        view_lat = hex_df['lat'].mean()
        view_lon = hex_df['lon'].mean()
        zoom = 8
    
    layers = []
    demographic_layers_info = []
    
    has_demographics = st.session_state.show_demographics and (selected_ages or selected_genders or selected_nationalities)
    
    if not has_demographics:
        layer = pdk.Layer(
            "H3HexagonLayer",
            hex_df,
            pickable=True,
            stroked=True,
            filled=True,
            extruded=False,
            get_hexagon="HEXAGON_ID",
            get_fill_color=["color_r", "color_g", "color_b", "opacity"],
            get_line_color=[30, 58, 95, 100],
            line_width_min_pixels=1
        )
        layers.append(layer)
    
    if has_demographics:
        demo_df = get_combined_demographic_data(current_city, selected_hour, selected_ages, selected_genders, selected_nationalities)
        if len(demo_df) > 0:
            coords = demo_df['HEXAGON_ID'].apply(h3_to_lat_lon)
            demo_df['lat'] = coords.apply(lambda x: x[0])
            demo_df['lon'] = coords.apply(lambda x: x[1])
            demo_df = demo_df.dropna(subset=['lat', 'lon'])
            
            max_traffic = demo_df['TRAFFIC_COUNT'].max()
            demo_df['normalized'] = demo_df['TRAFFIC_COUNT'] / max_traffic
            demo_df['color_r'] = (demo_df['normalized'] * 212 + (1 - demo_df['normalized']) * 8).astype(int)
            demo_df['color_g'] = (demo_df['normalized'] * 175 + (1 - demo_df['normalized']) * 145).astype(int)
            demo_df['color_b'] = (demo_df['normalized'] * 55 + (1 - demo_df['normalized']) * 178).astype(int)
            demo_df['opacity'] = (demo_df['normalized'] * 200 + 55).astype(int)
            
            filter_label_parts = []
            if selected_ages:
                filter_label_parts.append(", ".join(selected_ages))
            if selected_genders:
                filter_label_parts.append(", ".join(selected_genders))
            if selected_nationalities:
                filter_label_parts.append(", ".join(selected_nationalities))
            filter_label = " + ".join(filter_label_parts)
            demo_df['demographic'] = filter_label
            
            demo_layer = pdk.Layer(
                "H3HexagonLayer",
                demo_df,
                pickable=True,
                stroked=True,
                filled=True,
                extruded=False,
                get_hexagon="HEXAGON_ID",
                get_fill_color=["color_r", "color_g", "color_b", "opacity"],
                get_line_color=[255, 255, 255, 150],
                line_width_min_pixels=1
            )
            layers.append(demo_layer)
            demographic_layers_info.append({"name": filter_label, "color": "linear-gradient(90deg, #0891B2, #D4AF37)", "count": len(demo_df), "traffic": demo_df['TRAFFIC_COUNT'].sum()})
    
    anomaly_df = pd.DataFrame()
    
    if st.session_state.show_anomalies and not has_demographics:
        anomaly_df = detect_anomalies(hex_df)
        if len(anomaly_df) > 0:
            anomaly_df['color_r'] = 220
            anomaly_df['color_g'] = 38
            anomaly_df['color_b'] = 38
            anomaly_df['opacity'] = 230
            
            anomaly_layer = pdk.Layer(
                "H3HexagonLayer",
                anomaly_df,
                pickable=True,
                stroked=True,
                filled=True,
                extruded=False,
                get_hexagon="HEXAGON_ID",
                get_fill_color=["color_r", "color_g", "color_b", "opacity"],
                get_line_color=[180, 20, 20, 200],
                line_width_min_pixels=2
            )
            layers.append(anomaly_layer)
    
    if st.session_state.show_flow_arcs:
        if has_demographics and 'demo_df' in dir() and len(demo_df) > 0:
            arc_df = generate_flow_arcs(demo_df, current_city)
            arc_source_color = [212, 175, 55, 200]
            arc_target_color = [8, 145, 178, 200]
        else:
            arc_df = generate_flow_arcs(hex_df, current_city)
            arc_source_color = [8, 145, 178, 200]
            arc_target_color = [212, 175, 55, 200]
        
        if len(arc_df) > 0:
            arc_df['width'] = (arc_df['flow_volume'] / arc_df['flow_volume'].max() * 8 + 2).astype(int)
            
            arc_layer = pdk.Layer(
                "ArcLayer",
                arc_df,
                pickable=True,
                get_source_position=["source_lon", "source_lat"],
                get_target_position=["target_lon", "target_lat"],
                get_source_color=arc_source_color,
                get_target_color=arc_target_color,
                get_width="width",
                get_height=0.3,
                great_circle=True,
            )
            layers.append(arc_layer)
    
    if st.session_state.show_hotspots:
        if has_demographics and 'demo_df' in dir() and len(demo_df) > 0:
            hotspot_df = generate_hotspots(demo_df)
        else:
            hotspot_df = generate_hotspots(hex_df)
        
        if len(hotspot_df) > 0:
            hotspot_outer = pdk.Layer(
                "ScatterplotLayer",
                hotspot_df,
                pickable=False,
                opacity=0.3,
                stroked=False,
                filled=True,
                get_position=["lon", "lat"],
                get_fill_color=[212, 175, 55, 80],
                get_radius="radius",
                radius_min_pixels=20,
                radius_max_pixels=100,
            )
            
            hotspot_inner = pdk.Layer(
                "ScatterplotLayer",
                hotspot_df,
                pickable=True,
                opacity=0.7,
                stroked=False,
                filled=True,
                get_position=["lon", "lat"],
                get_fill_color=[220, 80, 40, 180],
                get_radius="inner_radius",
                radius_min_pixels=10,
                radius_max_pixels=50,
            )
            
            hotspot_core = pdk.Layer(
                "ScatterplotLayer",
                hotspot_df,
                pickable=False,
                opacity=1,
                stroked=False,
                filled=True,
                get_position=["lon", "lat"],
                get_fill_color=[255, 255, 255, 200],
                get_radius=50,
                radius_min_pixels=5,
                radius_max_pixels=15,
            )
            
            layers.extend([hotspot_outer, hotspot_inner, hotspot_core])
    
    if st.session_state.show_pois and current_city != "All Cities":
        poi_df = get_pois_for_city(current_city)
        if len(poi_df) > 0:
            poi_df['color'] = poi_df['type'].apply(lambda t: {
                'airport': [30, 144, 255, 220],
                'mall': [255, 140, 0, 220],
                'stadium': [50, 205, 50, 220],
                'landmark': [148, 0, 211, 220],
            }.get(t, [100, 100, 100, 200]))
            
            poi_layer = pdk.Layer(
                "ScatterplotLayer",
                poi_df,
                pickable=True,
                opacity=0.9,
                stroked=True,
                filled=True,
                get_position=["lon", "lat"],
                get_fill_color="color",
                get_line_color=[255, 255, 255, 255],
                get_radius=300,
                radius_min_pixels=12,
                radius_max_pixels=30,
                line_width_min_pixels=2,
            )
            layers.append(poi_layer)
            
            text_layer = pdk.Layer(
                "TextLayer",
                poi_df,
                pickable=False,
                get_position=["lon", "lat"],
                get_text="icon",
                get_size=20,
                get_color=[255, 255, 255, 255],
                get_alignment_baseline="'center'",
            )
            layers.append(text_layer)
    
    view_state = pdk.ViewState(latitude=view_lat, longitude=view_lon, zoom=zoom, pitch=0)
    
    deck = pdk.Deck(
        layers=layers,
        initial_view_state=view_state,
        tooltip={
            "html": "<b>Traffic:</b> {TRAFFIC_COUNT}<br/><b>Avg Dwell:</b> {AVG_DWELL:.1f} min<br/><b>{demographic}</b>",
            "style": {"backgroundColor": "#1E3A5F", "color": "white", "borderRadius": "8px", "padding": "8px"}
        }
    )
    
    active_layers = []
    if has_demographics:
        active_layers.append(f"👥 {len(demographic_layers_info)} Demographics")
    if st.session_state.show_pois and current_city != "All Cities":
        active_layers.append("📍 POIs")
    if st.session_state.show_flow_arcs and not has_demographics:
        active_layers.append("🌊 Flows")
    if st.session_state.show_hotspots and not has_demographics:
        active_layers.append("🔥 Hotspots")
    if st.session_state.show_anomalies and not has_demographics:
        active_layers.append("⚠️ Anomalies")
    
    with st.container(horizontal=True):
        st.metric("Hexagons", f"{len(hex_df):,}", border=True)
        st.metric("Total Traffic", f"{hex_df['TRAFFIC_COUNT'].sum():,}", border=True)
        st.metric("Avg Dwell", f"{hex_df['AVG_DWELL'].mean():.1f} min", border=True)
        if active_layers:
            st.metric("Active Layers", " ".join(active_layers[:2]), border=True)
        else:
            st.metric("Peak Hex", f"{hex_df['TRAFFIC_COUNT'].max():,}", border=True)
    
    with st.container(border=True):
        st.pydeck_chart(deck, use_container_width=True, height=550)
    
    if has_demographics and demographic_layers_info:
        legend_items = " &nbsp;&nbsp; ".join([
            f'<span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:{d["color"]};margin-right:4px;"></span>{d["name"]}'
            for d in demographic_layers_info
        ])
        st.html(f"""
        <div style="background: white; border: 1px solid #e2e8f0; border-radius: 10px; padding: 0.75rem 1rem;">
            <div style="font-weight: 600; font-size: 0.85rem; color: #1E3A5F; margin-bottom: 0.5rem;">Demographic Layers</div>
            <div style="font-size: 0.8rem; color: #334155;">{legend_items}</div>
        </div>
        """)
        
        with st.expander(":material/group: **Demographic Breakdown** - Traffic by segment", expanded=True):
            demo_cols = st.columns(len(demographic_layers_info))
            for i, demo in enumerate(demographic_layers_info):
                with demo_cols[i]:
                    st.markdown(f"<div style='text-align:center;'><span style='display:inline-block;width:16px;height:16px;border-radius:50%;background:{demo['color']};'></span></div>", unsafe_allow_html=True)
                    st.metric(demo['name'], f"{demo['traffic']:,}", f"{demo['count']} hexagons", border=True)
    else:
        col_legend, col_info = st.columns([2, 1])
        with col_legend:
            st.html(f"""
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 10px; padding: 0.75rem 1rem;">
                <div style="font-weight: 600; font-size: 0.85rem; color: #1E3A5F; margin-bottom: 0.5rem;">Color Legend</div>
                <div style="height: 10px; border-radius: 5px; background: {legend_colors}; margin-bottom: 0.3rem;"></div>
                <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #64748b;">
                    <span>{legend_label_low}</span>
                    <span>{legend_label_high}</span>
                </div>
            </div>
            """)
        with col_info:
            if st.session_state.show_pois or st.session_state.show_flow_arcs or st.session_state.show_hotspots:
                st.html("""
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.5rem 0.75rem; font-size: 0.75rem;">
                    <span style="color: #1E90FF;">●</span> Airport &nbsp;
                    <span style="color: #FF8C00;">●</span> Mall &nbsp;
                    <span style="color: #32CD32;">●</span> Stadium &nbsp;
                    <span style="color: #9400D3;">●</span> Landmark
                </div>
                """)
            else:
                st.caption("H3 Resolution 9 hexagons (~174m edge). Zoom to explore.")
    
    if st.session_state.show_flow_arcs and not has_demographics:
        with st.expander(":material/trending_up: **Flow Arc Details** - Movement patterns between zones", expanded=False):
            arc_df = generate_flow_arcs(hex_df, current_city)
            if len(arc_df) > 0:
                st.dataframe(
                    arc_df[['source_name', 'target_name', 'flow_volume']].rename(columns={
                        'source_name': 'Origin',
                        'target_name': 'Destination', 
                        'flow_volume': 'Flow Volume'
                    }),
                    use_container_width=True,
                    hide_index=True
                )
    
    if st.session_state.show_anomalies and len(anomaly_df) > 0 and not has_demographics:
        with st.expander(f":material/warning: **{len(anomaly_df)} Anomalies Detected** - Click to expand", expanded=False):
            severity_icons = {3: "🔴", 2: "🟠", 1: "🟡"}
            
            for idx, row in anomaly_df.head(5).iterrows():
                severity_icon = severity_icons.get(row['severity'], "⚪")
                with st.container(border=True):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.markdown(f"**{severity_icon} {row['anomaly_type']}**")
                        st.caption(f"Hex: `{row['HEXAGON_ID'][:16]}...`")
                    with col2:
                        st.metric("Traffic", f"{row['TRAFFIC_COUNT']:,.0f}")
                    with col3:
                        st.metric("Dwell", f"{row['AVG_DWELL']:.1f} min")
                    st.caption(row['reasons'])
            
            if len(anomaly_df) > 5:
                st.info(f"Showing top 5 of {len(anomaly_df)} anomalies")
else:
    st.warning("No data available for the selected filters. Try adjusting the city or hour.", icon=":material/warning:")
