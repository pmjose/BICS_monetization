import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from snowflake.snowpark.context import get_active_session
from utils.styles import render_common_styles, render_page_header, BICS_COLORS

st.set_page_config(page_title="IoT Analytics | BICS", page_icon=":material/sensors:", layout="wide")

st.logo("logo.png")
render_common_styles()

st.html("""
<style>
    .iot-kpi {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border-radius: 16px;
        padding: 1.25rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .iot-kpi::before {
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 3px;
        background: linear-gradient(90deg, #0891B2, #D4AF37);
    }
    .iot-kpi-value {
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #0891B2, #10B981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .iot-kpi-label {
        color: #94a3b8;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.25rem;
    }
    .industry-badge {
        display: inline-block;
        padding: 0.35rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.25rem;
    }
</style>
""")

render_page_header("IoT Industry Analytics", "Real-time IoT device monitoring across BICS enterprise verticals")

INDUSTRY_COLORS = {
    "Agriculture": "#10B981",
    "Healthcare": "#EC4899",
    "Industrial Manufacturing": "#F97316",
    "Transport & Logistics": "#0891B2",
    "OEM": "#8B5CF6",
}

INDUSTRY_ICONS = {
    "Agriculture": "🌾",
    "Healthcare": "🏥",
    "Industrial Manufacturing": "🏭",
    "Transport & Logistics": "🚛",
    "OEM": "📡",
}


@st.cache_data(ttl=300)
def load_iot_summary():
    session = get_active_session()
    return session.sql("""
        SELECT
            INDUSTRY,
            COUNT(DISTINCT DEVICE_ID) AS total_devices,
            COUNT(*) AS total_readings,
            SUM(CASE WHEN DEVICE_STATUS = 'active' THEN 1 ELSE 0 END) AS active_readings,
            SUM(CASE WHEN ALERT_FLAG = TRUE THEN 1 ELSE 0 END) AS alert_count,
            ROUND(SUM(DATA_USAGE_KB) / 1024, 1) AS data_volume_mb,
            ROUND(AVG(SIGNAL_STRENGTH_DBM), 1) AS avg_signal,
            ROUND(AVG(BATTERY_LEVEL_PCT), 1) AS avg_battery
        FROM BICS_TELCO.IOT_DATA.BICS_IOT_TELEMETRY
        GROUP BY INDUSTRY
        ORDER BY INDUSTRY
    """).to_pandas()


@st.cache_data(ttl=300)
def load_device_status(industry_filter):
    session = get_active_session()
    where = f"WHERE INDUSTRY = '{industry_filter}'" if industry_filter != "All Industries" else ""
    return session.sql(f"""
        SELECT DEVICE_STATUS, COUNT(*) AS cnt
        FROM BICS_TELCO.IOT_DATA.BICS_IOT_TELEMETRY
        {where}
        GROUP BY DEVICE_STATUS
    """).to_pandas()


@st.cache_data(ttl=300)
def load_daily_trends(industry_filter):
    session = get_active_session()
    where = f"WHERE INDUSTRY = '{industry_filter}'" if industry_filter != "All Industries" else ""
    return session.sql(f"""
        SELECT DATE, COUNT(*) AS readings, SUM(CASE WHEN ALERT_FLAG THEN 1 ELSE 0 END) AS alerts,
               ROUND(AVG(SIGNAL_STRENGTH_DBM), 1) AS avg_signal,
               ROUND(SUM(DATA_USAGE_KB)/1024, 1) AS data_mb
        FROM BICS_TELCO.IOT_DATA.BICS_IOT_TELEMETRY
        {where}
        GROUP BY DATE ORDER BY DATE
    """).to_pandas()


@st.cache_data(ttl=300)
def load_connectivity_breakdown(industry_filter):
    session = get_active_session()
    where = f"WHERE INDUSTRY = '{industry_filter}'" if industry_filter != "All Industries" else ""
    return session.sql(f"""
        SELECT CONNECTIVITY_TYPE, COUNT(DISTINCT DEVICE_ID) AS devices, COUNT(*) AS readings
        FROM BICS_TELCO.IOT_DATA.BICS_IOT_TELEMETRY
        {where}
        GROUP BY CONNECTIVITY_TYPE ORDER BY devices DESC
    """).to_pandas()


@st.cache_data(ttl=300)
def load_sim_breakdown(industry_filter):
    session = get_active_session()
    where = f"WHERE INDUSTRY = '{industry_filter}'" if industry_filter != "All Industries" else ""
    return session.sql(f"""
        SELECT SIM_TYPE, COUNT(DISTINCT DEVICE_ID) AS devices
        FROM BICS_TELCO.IOT_DATA.BICS_IOT_TELEMETRY
        {where}
        GROUP BY SIM_TYPE ORDER BY devices DESC
    """).to_pandas()


@st.cache_data(ttl=300)
def load_top_alerting(industry_filter, limit=10):
    session = get_active_session()
    where = f"WHERE INDUSTRY = '{industry_filter}'" if industry_filter != "All Industries" else ""
    return session.sql(f"""
        SELECT DEVICE_ID, DEVICE_TYPE, CITY, SITE_NAME,
               SUM(CASE WHEN ALERT_FLAG THEN 1 ELSE 0 END) AS alerts,
               ROUND(AVG(SIGNAL_STRENGTH_DBM), 1) AS avg_signal
        FROM BICS_TELCO.IOT_DATA.BICS_IOT_TELEMETRY
        {where}
        GROUP BY DEVICE_ID, DEVICE_TYPE, CITY, SITE_NAME
        HAVING alerts > 0
        ORDER BY alerts DESC
        LIMIT {limit}
    """).to_pandas()


@st.cache_data(ttl=300)
def load_hourly_pattern(industry_filter):
    session = get_active_session()
    where = f"WHERE INDUSTRY = '{industry_filter}'" if industry_filter != "All Industries" else ""
    return session.sql(f"""
        SELECT HOUR, COUNT(*) AS readings, ROUND(AVG(DATA_USAGE_KB), 2) AS avg_data_kb
        FROM BICS_TELCO.IOT_DATA.BICS_IOT_TELEMETRY
        {where}
        GROUP BY HOUR ORDER BY HOUR
    """).to_pandas()


@st.cache_data(ttl=300)
def load_device_types(industry_filter):
    session = get_active_session()
    where = f"WHERE INDUSTRY = '{industry_filter}'" if industry_filter != "All Industries" else ""
    return session.sql(f"""
        SELECT DEVICE_TYPE, COUNT(DISTINCT DEVICE_ID) AS devices,
               ROUND(AVG(SIGNAL_STRENGTH_DBM), 1) AS avg_signal,
               ROUND(AVG(BATTERY_LEVEL_PCT), 1) AS avg_battery
        FROM BICS_TELCO.IOT_DATA.BICS_IOT_TELEMETRY
        {where}
        GROUP BY DEVICE_TYPE ORDER BY devices DESC
    """).to_pandas()


try:
    summary = load_iot_summary()

    industries = ["All Industries"] + sorted(summary["INDUSTRY"].unique().tolist())
    selected_industry = st.sidebar.selectbox("Select Industry", industries, index=0)

    total_devices = int(summary["TOTAL_DEVICES"].sum())
    total_readings = int(summary["TOTAL_READINGS"].sum())
    total_alerts = int(summary["ALERT_COUNT"].sum())
    total_data = round(summary["DATA_VOLUME_MB"].sum(), 1)

    if selected_industry != "All Industries":
        row = summary[summary["INDUSTRY"] == selected_industry].iloc[0]
        total_devices = int(row["TOTAL_DEVICES"])
        total_readings = int(row["TOTAL_READINGS"])
        total_alerts = int(row["ALERT_COUNT"])
        total_data = round(row["DATA_VOLUME_MB"], 1)

    k1, k2, k3, k4 = st.columns(4)
    for col, val, label in [
        (k1, f"{total_devices:,}", "Connected Devices"),
        (k2, f"{total_readings:,}", "Telemetry Readings"),
        (k3, f"{total_alerts:,}", "Active Alerts"),
        (k4, f"{total_data:,.0f} MB", "Data Volume"),
    ]:
        col.html(f"""
        <div class="iot-kpi">
            <div class="iot-kpi-value">{val}</div>
            <div class="iot-kpi-label">{label}</div>
        </div>
        """)

    if selected_industry == "All Industries":
        st.html('<div style="margin-top: 1.5rem;"></div>')
        ind_cols = st.columns(5)
        for i, (_, row) in enumerate(summary.iterrows()):
            ind = row["INDUSTRY"]
            color = INDUSTRY_COLORS.get(ind, "#64748b")
            icon = INDUSTRY_ICONS.get(ind, "📊")
            ind_cols[i].html(f"""
            <div style="background: linear-gradient(135deg, {color}15, {color}08); border: 1px solid {color}40;
                        border-radius: 14px; padding: 1rem; text-align: center;">
                <div style="font-size: 1.5rem;">{icon}</div>
                <div style="color: {color}; font-weight: 700; font-size: 1rem; margin: 0.3rem 0;">{ind}</div>
                <div style="color: #64748b; font-size: 0.8rem;">{int(row['TOTAL_DEVICES'])} devices &bull; {int(row['ALERT_COUNT'])} alerts</div>
            </div>
            """)

    c1, c2 = st.columns(2)

    with c1:
        status_df = load_device_status(selected_industry)
        status_colors = {"active": "#10B981", "warning": "#F59E0B", "critical": "#EF4444", "offline": "#94a3b8"}
        fig = px.pie(status_df, names="DEVICE_STATUS", values="CNT",
                     color="DEVICE_STATUS",
                     color_discrete_map=status_colors,
                     hole=0.5)
        fig.update_layout(
            title=dict(text="Device Status Distribution", font=dict(size=14, color="#1E3A5F")),
            margin=dict(l=20, r=20, t=50, b=20),
            height=350,
            legend=dict(orientation="h", y=-0.1),
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        conn_df = load_connectivity_breakdown(selected_industry)
        fig = px.bar(conn_df, x="CONNECTIVITY_TYPE", y="DEVICES",
                     color="CONNECTIVITY_TYPE",
                     color_discrete_sequence=[BICS_COLORS["teal"], BICS_COLORS["navy"],
                                              BICS_COLORS["gold"], BICS_COLORS["green"]])
        fig.update_layout(
            title=dict(text="Connectivity Technology", font=dict(size=14, color="#1E3A5F")),
            margin=dict(l=20, r=20, t=50, b=20),
            height=350,
            showlegend=False,
            xaxis_title="",
            yaxis_title="Devices",
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)

    trends_df = load_daily_trends(selected_industry)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=trends_df["DATE"], y=trends_df["READINGS"],
        name="Readings", mode="lines+markers",
        line=dict(color=BICS_COLORS["teal"], width=2),
        marker=dict(size=4),
    ))
    fig.add_trace(go.Bar(
        x=trends_df["DATE"], y=trends_df["ALERTS"],
        name="Alerts", marker_color="#EF4444", opacity=0.6,
        yaxis="y2",
    ))
    fig.update_layout(
        title=dict(text="Daily Telemetry Volume & Alerts", font=dict(size=14, color="#1E3A5F")),
        margin=dict(l=20, r=60, t=50, b=20),
        height=350,
        legend=dict(orientation="h", y=-0.15),
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(title="Readings", side="left"),
        yaxis2=dict(title="Alerts", side="right", overlaying="y"),
    )
    st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)

    with c3:
        sim_df = load_sim_breakdown(selected_industry)
        sim_colors = {"eSIM": BICS_COLORS["teal"], "Traditional SIM": BICS_COLORS["navy"], "iSIM": BICS_COLORS["gold"]}
        fig = px.pie(sim_df, names="SIM_TYPE", values="DEVICES",
                     color="SIM_TYPE", color_discrete_map=sim_colors, hole=0.45)
        fig.update_layout(
            title=dict(text="SIM Technology Distribution", font=dict(size=14, color="#1E3A5F")),
            margin=dict(l=20, r=20, t=50, b=20),
            height=320,
            legend=dict(orientation="h", y=-0.1),
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        hourly_df = load_hourly_pattern(selected_industry)
        fig = px.area(hourly_df, x="HOUR", y="READINGS",
                      color_discrete_sequence=[BICS_COLORS["teal"]])
        fig.update_layout(
            title=dict(text="Hourly Traffic Pattern", font=dict(size=14, color="#1E3A5F")),
            margin=dict(l=20, r=20, t=50, b=20),
            height=320,
            xaxis=dict(title="Hour of Day", dtick=3),
            yaxis_title="Readings",
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)

    dt_df = load_device_types(selected_industry)
    fig = px.bar(dt_df, x="DEVICES", y="DEVICE_TYPE", orientation="h",
                 color="AVG_SIGNAL",
                 color_continuous_scale=["#EF4444", "#F59E0B", "#10B981"],
                 labels={"AVG_SIGNAL": "Avg Signal (dBm)"})
    fig.update_layout(
        title=dict(text="Device Types - Fleet Size & Signal Quality", font=dict(size=14, color="#1E3A5F")),
        margin=dict(l=20, r=20, t=50, b=20),
        height=max(300, len(dt_df) * 35 + 80),
        yaxis=dict(autorange="reversed"),
        xaxis_title="Device Count",
        yaxis_title="",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top Alerting Devices")
    alerts_df = load_top_alerting(selected_industry)
    if not alerts_df.empty:
        st.dataframe(
            alerts_df.rename(columns={
                "DEVICE_ID": "Device", "DEVICE_TYPE": "Type", "CITY": "City",
                "SITE_NAME": "Site", "ALERTS": "Alerts", "AVG_SIGNAL": "Avg Signal (dBm)"
            }),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No alerts recorded for this selection.")

except Exception as e:
    st.error(f"Error loading IoT data: {e}")
    st.info("Ensure the IoT tables exist in BICS_TELCO.IOT_DATA schema. Run generate_iot_data.py to create the data.")
