import streamlit as st
import pandas as pd
import pydeck as pdk
from snowflake.snowpark.context import get_active_session
from utils.styles import render_common_styles, render_page_header, BICS_COLORS

st.set_page_config(page_title="IoT Device Map | BICS", page_icon=":material/location_on:", layout="wide")

st.logo("logo.png")
render_common_styles()
render_page_header("IoT Device Map", "Geographic view of BICS IoT device deployments across Belgium")

STATUS_COLORS = {
    "active": [16, 185, 129, 200],
    "warning": [245, 158, 11, 200],
    "critical": [239, 68, 68, 200],
    "offline": [148, 163, 184, 140],
}

INDUSTRY_COLORS = {
    "Agriculture": [16, 185, 129, 200],
    "Healthcare": [236, 72, 153, 200],
    "Industrial Manufacturing": [249, 115, 22, 200],
    "Transport & Logistics": [8, 145, 178, 200],
    "OEM": [139, 92, 246, 200],
}


@st.cache_data(ttl=300)
def load_device_locations(industry_filter, status_filter):
    session = get_active_session()
    conditions = []
    if industry_filter != "All Industries":
        conditions.append(f"INDUSTRY = '{industry_filter}'")
    if status_filter != "All Statuses":
        conditions.append(f"DEVICE_STATUS = '{status_filter.lower()}'")
    where = "WHERE " + " AND ".join(conditions) if conditions else ""
    return session.sql(f"""
        SELECT DEVICE_ID, INDUSTRY, DEVICE_TYPE, CONNECTIVITY_TYPE, SIM_TYPE,
               CITY, SITE_NAME, LATITUDE, LONGITUDE, DEVICE_STATUS,
               COUNT(*) AS reading_count,
               SUM(CASE WHEN ALERT_FLAG THEN 1 ELSE 0 END) AS alert_count,
               ROUND(AVG(SIGNAL_STRENGTH_DBM), 1) AS avg_signal,
               ROUND(AVG(BATTERY_LEVEL_PCT), 1) AS avg_battery,
               ROUND(SUM(DATA_USAGE_KB)/1024, 2) AS data_mb
        FROM BICS_TELCO.IOT_DATA.BICS_IOT_TELEMETRY
        {where}
        GROUP BY DEVICE_ID, INDUSTRY, DEVICE_TYPE, CONNECTIVITY_TYPE, SIM_TYPE,
                 CITY, SITE_NAME, LATITUDE, LONGITUDE, DEVICE_STATUS
        ORDER BY alert_count DESC
    """).to_pandas()


@st.cache_data(ttl=300)
def load_site_summary(industry_filter):
    session = get_active_session()
    where = f"WHERE INDUSTRY = '{industry_filter}'" if industry_filter != "All Industries" else ""
    return session.sql(f"""
        SELECT SITE_NAME, CITY, INDUSTRY,
               COUNT(DISTINCT DEVICE_ID) AS devices,
               SUM(CASE WHEN ALERT_FLAG THEN 1 ELSE 0 END) AS alerts,
               ROUND(AVG(LATITUDE), 6) AS lat,
               ROUND(AVG(LONGITUDE), 6) AS lon
        FROM BICS_TELCO.IOT_DATA.BICS_IOT_TELEMETRY
        {where}
        GROUP BY SITE_NAME, CITY, INDUSTRY
        ORDER BY devices DESC
    """).to_pandas()


with st.sidebar:
    st.subheader("Map Filters")
    industry_filter = st.selectbox("Industry", [
        "All Industries", "Agriculture", "Healthcare",
        "Industrial Manufacturing", "Transport & Logistics", "OEM"
    ])
    status_filter = st.selectbox("Device Status", [
        "All Statuses", "Active", "Warning", "Critical", "Offline"
    ])
    color_by = st.radio("Color By", ["Status", "Industry"], horizontal=True)

try:
    df = load_device_locations(industry_filter, status_filter)

    if df.empty:
        st.warning("No devices match the selected filters.")
        st.stop()

    total = len(df)
    active = len(df[df["DEVICE_STATUS"] == "active"])
    alerting = int(df["ALERT_COUNT"].sum())
    avg_sig = round(df["AVG_SIGNAL"].mean(), 1) if not df["AVG_SIGNAL"].isna().all() else 0

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Devices Shown", f"{total:,}")
    k2.metric("Active", f"{active:,}", delta=f"{active/total*100:.0f}%" if total else "0%")
    k3.metric("Total Alerts", f"{alerting:,}")
    k4.metric("Avg Signal", f"{avg_sig} dBm")

    if color_by == "Status":
        df["color"] = df["DEVICE_STATUS"].map(STATUS_COLORS)
    else:
        df["color"] = df["INDUSTRY"].map(INDUSTRY_COLORS)
    df["color"] = df["color"].apply(lambda x: x if isinstance(x, list) else [100, 100, 100, 150])

    df["radius"] = df["ALERT_COUNT"].apply(lambda a: min(800, 200 + a * 50))

    scatter = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["LONGITUDE", "LATITUDE"],
        get_radius="radius",
        get_fill_color="color",
        pickable=True,
        opacity=0.8,
        stroked=True,
        get_line_color=[255, 255, 255, 80],
        line_width_min_pixels=1,
    )

    tooltip = {
        "html": """
        <div style="padding:8px; font-family: sans-serif;">
            <b>{DEVICE_ID}</b><br/>
            <b>Type:</b> {DEVICE_TYPE}<br/>
            <b>Industry:</b> {INDUSTRY}<br/>
            <b>Site:</b> {SITE_NAME}<br/>
            <b>Status:</b> {DEVICE_STATUS}<br/>
            <b>Connectivity:</b> {CONNECTIVITY_TYPE} ({SIM_TYPE})<br/>
            <b>Readings:</b> {READING_COUNT} | <b>Alerts:</b> {ALERT_COUNT}<br/>
            <b>Signal:</b> {AVG_SIGNAL} dBm | <b>Data:</b> {DATA_MB} MB
        </div>
        """,
        "style": {"backgroundColor": "#1E3A5F", "color": "white", "border-radius": "8px"},
    }

    view = pdk.ViewState(latitude=50.85, longitude=4.35, zoom=7.5, pitch=30)

    st.pydeck_chart(pdk.Deck(
        layers=[scatter],
        initial_view_state=view,
        tooltip=tooltip,
        map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
    ))

    legend_items = STATUS_COLORS if color_by == "Status" else INDUSTRY_COLORS
    legend_html = " ".join([
        f'<span style="display:inline-block; width:12px; height:12px; border-radius:50%; '
        f'background:rgba({c[0]},{c[1]},{c[2]},{c[3]/255}); margin-right:4px; vertical-align:middle;"></span>'
        f'<span style="color:#64748b; font-size:0.8rem; margin-right:1rem;">{name}</span>'
        for name, c in legend_items.items()
    ])
    st.html(f'<div style="text-align:center; margin: 0.5rem 0;">{legend_html}</div>')

    st.subheader("Deployment Sites")
    sites_df = load_site_summary(industry_filter)
    if not sites_df.empty:
        st.dataframe(
            sites_df.rename(columns={
                "SITE_NAME": "Site", "CITY": "City", "INDUSTRY": "Industry",
                "DEVICES": "Devices", "ALERTS": "Alerts",
            })[["Site", "City", "Industry", "Devices", "Alerts"]],
            use_container_width=True, hide_index=True,
        )

except Exception as e:
    st.error(f"Error loading IoT map data: {e}")
    st.info("Ensure the IoT tables exist in BICS_TELCO.IOT_DATA schema. Run generate_iot_data.py to create the data.")
