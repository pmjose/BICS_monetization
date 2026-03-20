import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from snowflake.snowpark.context import get_active_session
from utils.styles import render_common_styles, render_page_header, BICS_COLORS

st.set_page_config(page_title="IoT Analytics | BICS", page_icon=":material/sensors:", layout="wide")
render_common_styles()

st.html("""<style>
    .iot-kpi {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border-radius: 16px; padding: 1rem; text-align: center;
        position: relative; overflow: hidden;
    }
    .iot-kpi::before {
        content: ''; position: absolute; top: 0; left: 0;
        width: 100%; height: 3px;
        background: linear-gradient(90deg, #0891B2, #D4AF37);
    }
    .iot-kpi-value {
        font-size: 1.5rem; font-weight: 800;
        background: linear-gradient(135deg, #0891B2, #10B981);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    }
    .iot-kpi-label {
        color: #94a3b8; font-size: 0.7rem;
        text-transform: uppercase; letter-spacing: 1px; margin-top: 0.2rem;
    }
    .ai-box {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #f0fdf4 100%);
        border: 1px solid #bae6fd; border-radius: 12px;
        padding: 1.1rem 1.25rem 0.7rem; margin: 0.25rem 0 1.5rem;
        position: relative;
    }
    .ai-box::before {
        content: 'AI Recommendation'; position: absolute; top: -10px; left: 16px;
        background: linear-gradient(135deg, #0891B2, #0369a1);
        color: white; font-size: 0.62rem; font-weight: 700;
        padding: 2px 10px; border-radius: 10px; letter-spacing: 0.5px;
    }
    .ai-s { padding: 0.25rem 0 0.25rem 0.75rem; border-left: 3px solid; margin: 0.35rem 0; }
    .ai-i { border-color: #0891B2; }
    .ai-a { border-color: #D4AF37; }
    .ai-o { border-color: #10B981; }
    .ai-l { font-size: 0.62rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin: 0; }
    .ai-i .ai-l { color: #0891B2; }
    .ai-a .ai-l { color: #B8860B; }
    .ai-o .ai-l { color: #059669; }
    .ai-t { color: #374151; font-size: 0.8rem; line-height: 1.45; margin: 0.1rem 0 0; }
</style>""")

render_page_header("IoT Industry Analytics", "Comprehensive IoT monitoring with AI-powered insights across BICS enterprise verticals")

INDUSTRIES = [
    ("Agriculture", "#10B981"),
    ("Healthcare", "#EC4899"),
    ("Industrial Manufacturing", "#F97316"),
    ("Transport & Logistics", "#0891B2"),
    ("OEM", "#8B5CF6"),
]

STATUS_COLORS = {"active": "#10B981", "warning": "#F59E0B", "critical": "#EF4444", "offline": "#94a3b8"}


def base_layout(**kw):
    d = dict(margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    d.update(kw)
    return d


def ctitle(text):
    return dict(text=text, font=dict(size=14, color="#1E3A5F"))


@st.cache_data(ttl=300)
def load_kpis(industry):
    return get_active_session().sql(f"""
        SELECT COUNT(DISTINCT DEVICE_ID) AS DEVICES, COUNT(*) AS READINGS,
               SUM(CASE WHEN DEVICE_STATUS='active' THEN 1 ELSE 0 END) AS ACTIVE,
               SUM(CASE WHEN ALERT_FLAG THEN 1 ELSE 0 END) AS ALERTS,
               ROUND(SUM(DATA_USAGE_KB)/1024,1) AS DATA_MB,
               ROUND(AVG(SIGNAL_STRENGTH_DBM),1) AS AVG_SIGNAL,
               ROUND(AVG(BATTERY_LEVEL_PCT),1) AS AVG_BATTERY
        FROM BICS_TELCO.IOT_DATA.BICS_IOT_TELEMETRY WHERE INDUSTRY='{industry}'
    """).to_pandas()


@st.cache_data(ttl=300)
def load_device_status(industry):
    return get_active_session().sql(f"""
        SELECT DEVICE_STATUS, COUNT(*) AS CNT
        FROM BICS_TELCO.IOT_DATA.BICS_IOT_TELEMETRY WHERE INDUSTRY='{industry}'
        GROUP BY DEVICE_STATUS
    """).to_pandas()


@st.cache_data(ttl=300)
def load_connectivity(industry):
    return get_active_session().sql(f"""
        SELECT CONNECTIVITY_TYPE, COUNT(DISTINCT DEVICE_ID) AS DEVICES
        FROM BICS_TELCO.IOT_DATA.BICS_IOT_TELEMETRY WHERE INDUSTRY='{industry}'
        GROUP BY CONNECTIVITY_TYPE ORDER BY DEVICES DESC
    """).to_pandas()


@st.cache_data(ttl=300)
def load_daily_trends(industry):
    return get_active_session().sql(f"""
        SELECT DATE, COUNT(*) AS READINGS,
               SUM(CASE WHEN ALERT_FLAG THEN 1 ELSE 0 END) AS ALERTS,
               ROUND(SUM(DATA_USAGE_KB)/1024,1) AS DATA_MB
        FROM BICS_TELCO.IOT_DATA.BICS_IOT_TELEMETRY WHERE INDUSTRY='{industry}'
        GROUP BY DATE ORDER BY DATE
    """).to_pandas()


@st.cache_data(ttl=300)
def load_sim(industry):
    return get_active_session().sql(f"""
        SELECT SIM_TYPE, COUNT(DISTINCT DEVICE_ID) AS DEVICES
        FROM BICS_TELCO.IOT_DATA.BICS_IOT_TELEMETRY WHERE INDUSTRY='{industry}'
        GROUP BY SIM_TYPE ORDER BY DEVICES DESC
    """).to_pandas()


@st.cache_data(ttl=300)
def load_hourly(industry):
    return get_active_session().sql(f"""
        SELECT HOUR, COUNT(*) AS READINGS, ROUND(AVG(DATA_USAGE_KB),2) AS AVG_DATA_KB
        FROM BICS_TELCO.IOT_DATA.BICS_IOT_TELEMETRY WHERE INDUSTRY='{industry}'
        GROUP BY HOUR ORDER BY HOUR
    """).to_pandas()


@st.cache_data(ttl=300)
def load_device_types(industry):
    return get_active_session().sql(f"""
        SELECT DEVICE_TYPE, COUNT(DISTINCT DEVICE_ID) AS DEVICES,
               ROUND(AVG(SIGNAL_STRENGTH_DBM),1) AS AVG_SIGNAL,
               ROUND(AVG(BATTERY_LEVEL_PCT),1) AS AVG_BATTERY
        FROM BICS_TELCO.IOT_DATA.BICS_IOT_TELEMETRY WHERE INDUSTRY='{industry}'
        GROUP BY DEVICE_TYPE ORDER BY DEVICES DESC
    """).to_pandas()


@st.cache_data(ttl=300)
def load_cities(industry):
    return get_active_session().sql(f"""
        SELECT CITY, COUNT(DISTINCT DEVICE_ID) AS DEVICES,
               SUM(CASE WHEN ALERT_FLAG THEN 1 ELSE 0 END) AS ALERTS,
               ROUND(AVG(SIGNAL_STRENGTH_DBM),1) AS AVG_SIGNAL
        FROM BICS_TELCO.IOT_DATA.BICS_IOT_TELEMETRY WHERE INDUSTRY='{industry}'
        GROUP BY CITY ORDER BY DEVICES DESC
    """).to_pandas()


@st.cache_data(ttl=300)
def load_device_health(industry):
    return get_active_session().sql(f"""
        SELECT DEVICE_ID, DEVICE_TYPE, CITY,
               ROUND(AVG(SIGNAL_STRENGTH_DBM),1) AS AVG_SIGNAL,
               ROUND(AVG(BATTERY_LEVEL_PCT),1) AS AVG_BATTERY,
               SUM(CASE WHEN ALERT_FLAG THEN 1 ELSE 0 END) AS ALERTS
        FROM BICS_TELCO.IOT_DATA.BICS_IOT_TELEMETRY WHERE INDUSTRY='{industry}'
        GROUP BY DEVICE_ID, DEVICE_TYPE, CITY
    """).to_pandas()


@st.cache_data(ttl=300)
def load_top_alerting(industry):
    return get_active_session().sql(f"""
        SELECT DEVICE_ID, DEVICE_TYPE, CITY, SITE_NAME,
               SUM(CASE WHEN ALERT_FLAG THEN 1 ELSE 0 END) AS ALERTS,
               ROUND(AVG(SIGNAL_STRENGTH_DBM),1) AS AVG_SIGNAL,
               ROUND(AVG(BATTERY_LEVEL_PCT),1) AS AVG_BATTERY
        FROM BICS_TELCO.IOT_DATA.BICS_IOT_TELEMETRY WHERE INDUSTRY='{industry}'
        GROUP BY DEVICE_ID, DEVICE_TYPE, CITY, SITE_NAME
        HAVING ALERTS > 0 ORDER BY ALERTS DESC LIMIT 10
    """).to_pandas()


AI_RECS = {
    "Agriculture": {
        "device_status": {
            "insight": "92% of agricultural sensors maintain active status despite challenging rural deployment conditions with limited cellular infrastructure.",
            "action": "Deploy NB-IoT/LTE-M dual-mode failover for the 8% non-active devices, prioritizing irrigation controllers in signal-weak zones below -75 dBm.",
            "outcome": "Projected 99.5% fleet uptime, preventing an estimated 15% of crop water stress incidents during peak growing season."
        },
        "connectivity": {
            "insight": "NB-IoT and LTE-M together account for 75% of agricultural connections, well-matched to low-bandwidth, low-power sensor profiles.",
            "action": "Migrate remaining 4G agricultural sensors to NB-IoT where data rates below 100 kbps are sufficient, cutting power consumption by 40%.",
            "outcome": "Battery life extension from 2 to 5 years for soil sensors, reducing field maintenance visits by 60% and saving ~12K EUR annually."
        },
        "daily_trends": {
            "insight": "Telemetry volume shows stable daily patterns with 8-12% variance. Alert spikes correlate with weather events impacting soil and climate readings.",
            "action": "Implement predictive alerting that cross-references weather forecasts with historical sensor patterns to pre-position field technicians.",
            "outcome": "30% faster response to weather-related sensor failures, preventing critical data gaps during irrigation and harvest windows."
        },
        "sim_type": {
            "insight": "eSIM adoption leads at 47%, driven by the need for remote provisioning of sensors deployed in hard-to-access agricultural fields.",
            "action": "Accelerate iSIM adoption for next-generation soil sensors, eliminating SIM slot requirements and improving outdoor weatherproofing.",
            "outcome": "25% reduction in device manufacturing costs and improved IP68 compliance for year-round outdoor agricultural deployments."
        },
        "hourly": {
            "insight": "Peak data transmission at 6-8 AM aligns with automated morning irrigation cycles. A secondary evening peak corresponds to livestock monitoring routines.",
            "action": "Implement BICS Smart Connectivity scheduling to prioritize bandwidth allocation during agricultural peak hours across rural cells.",
            "outcome": "20% improvement in data delivery latency during critical irrigation windows, ensuring real-time soil moisture response."
        },
        "device_types": {
            "insight": "GPS Tractor Trackers are the largest fleet segment (20%) and generate 35% of total data volume due to continuous location streaming.",
            "action": "Deploy edge-based data compression for tractor trackers, transmitting delta-only position updates instead of full GPS payloads.",
            "outcome": "45% reduction in data transmission costs for tractor tracking while maintaining sub-meter positioning accuracy."
        },
        "city": {
            "insight": "Leuven leads agricultural IoT adoption, driven by proximity to KU Leuven's precision agriculture research programs and AgriTech startups.",
            "action": "Target Bruges and Kortrijk regions for expansion, leveraging existing NB-IoT coverage from nearby industrial and logistics deployments.",
            "outcome": "30% fleet growth in West Flanders within 12 months, tapping into underserved horticultural and dairy farming markets."
        },
        "signal_battery": {
            "insight": "Main device cluster at -55 to -65 dBm signal / 65-80% battery indicates healthy fleet. Outliers below -80 dBm show 3x higher alert frequency.",
            "action": "Deploy solar-powered signal repeaters for the 12% of devices consistently below the -75 dBm reliability threshold in rural areas.",
            "outcome": "40% reduction in connectivity-related alerts and 25% battery life improvement for signal-challenged rural devices."
        },
    },
    "Healthcare": {
        "device_status": {
            "insight": "92.4% active rate meets baseline medical device compliance, but 0.8% critical-status devices require immediate attention for patient safety.",
            "action": "Implement automated cellular failover for all patient-facing monitors with less than 30-second recovery time objective (RTO).",
            "outcome": "Achieve 99.99% uptime for patient monitors, meeting Joint Commission requirements and eliminating connectivity-related care gaps."
        },
        "connectivity": {
            "insight": "4G dominates at 44% with 5G growing to 25%, reflecting the healthcare sector's need for reliable, low-latency patient data transmission.",
            "action": "Prioritize 5G migration for real-time patient monitors and infusion pumps requiring sub-10 ms latency guarantees.",
            "outcome": "Enable real-time remote patient monitoring across 15 additional hospital departments with guaranteed QoS SLAs."
        },
        "daily_trends": {
            "insight": "Consistent 24/7 telemetry pattern reflects continuous patient monitoring. Alert spikes correlate with shift handover periods (7 AM, 3 PM, 11 PM).",
            "action": "Deploy enhanced monitoring dashboards during shift transitions and automate device health checks at handover boundaries.",
            "outcome": "50% reduction in shift-handover alert backlogs, ensuring seamless patient care continuity across all nursing shifts."
        },
        "sim_type": {
            "insight": "Traditional SIM persists at 28% in legacy medical devices where physical SIM swaps in sterile environments create infection control risk.",
            "action": "Fast-track eSIM migration for legacy devices, enabling remote reprovisioning without breaking sterile seals in operating theaters.",
            "outcome": "40% faster device provisioning and elimination of sterile environment breaches related to SIM card maintenance."
        },
        "hourly": {
            "insight": "Near-constant 24/7 data flow with a subtle 3-5 AM dip reflects reduced elective monitoring. ICU devices maintain flat activity around the clock.",
            "action": "Schedule non-critical firmware updates and data syncs during the 3-5 AM maintenance window to minimize bandwidth contention.",
            "outcome": "Zero patient-impact maintenance windows while keeping all device firmware current with the latest security patches."
        },
        "device_types": {
            "insight": "Infusion Pump Monitors and Patient Monitors together form 43% of the fleet, both classified as life-critical connectivity tier.",
            "action": "Implement dedicated QoS lanes with guaranteed bandwidth reservation for infusion pumps and patient monitors at all times.",
            "outcome": "100% telemetry delivery rate for life-critical devices, supporting regulatory compliance and reducing adverse event risk."
        },
        "city": {
            "insight": "Brussels dominates with 69 devices across 3 major hospital networks. Ghent's 44 devices reflect UZ Gent's digital health innovation programs.",
            "action": "Expand deployment to regional hospitals in Liege and Leuven, offering bundled connectivity and device management packages.",
            "outcome": "50% more patients covered by IoT-enabled monitoring, enabling early discharge programs saving ~2.5K EUR per patient stay."
        },
        "signal_battery": {
            "insight": "Healthcare devices cluster tightly at -55 to -65 dBm, but battery variance (40-95%) reflects varying device ages across hospital floors.",
            "action": "Deploy in-building DAS (Distributed Antenna Systems) in hospital basements and shielded radiology departments for uniform coverage.",
            "outcome": "Uniform -50 dBm coverage across all medical facility floors, eliminating dead zones in critical patient care areas."
        },
    },
    "Industrial Manufacturing": {
        "device_status": {
            "insight": "92.3% active rate is solid, but 0.96% critical-status devices in manufacturing indicate potential safety sensors offline - a compliance risk.",
            "action": "Implement real-time critical-device escalation with automatic SMS/email to plant safety officers within 60 seconds of any status change.",
            "outcome": "Prevent an estimated 3 production line emergency stops per quarter, saving ~150K EUR in unplanned downtime costs."
        },
        "connectivity": {
            "insight": "4G and 5G together serve 63% of industrial connections, reflecting high-bandwidth needs for CNC monitoring and vibration analysis streams.",
            "action": "Evaluate private 5G network deployment for Hasselt and Antwerp manufacturing clusters to guarantee industrial-grade latency.",
            "outcome": "Dedicated industrial spectrum enabling less than 5 ms latency for safety-critical alerts and real-time quality control loops."
        },
        "daily_trends": {
            "insight": "Telemetry shows consistent 3-shift work patterns. Alert rates increase 15% during night shifts when human supervision is reduced.",
            "action": "Deploy AI-powered anomaly detection on night-shift telemetry streams to compensate for reduced human oversight on factory floors.",
            "outcome": "25% reduction in unplanned downtime events during night shifts, matching daytime operational reliability benchmarks."
        },
        "sim_type": {
            "insight": "Balanced SIM mix with eSIM at 38% reflects gradual modernization of legacy industrial equipment with embedded connectivity modules.",
            "action": "Standardize on eSIM for all new factory floor deployments, enabling centralized provisioning across multi-site operations.",
            "outcome": "Simplified device lifecycle management across 6 manufacturing sites, reducing IT provisioning overhead by 30% per device."
        },
        "hourly": {
            "insight": "Triple-peak pattern confirms 3-shift operations (6 AM, 2 PM, 10 PM). Data volume drops only 20% between shifts, indicating continuous process monitoring.",
            "action": "Implement dynamic bandwidth allocation that scales connectivity resources in sync with shift schedules and production plans.",
            "outcome": "Consistent data delivery across all 3 shifts with 15% bandwidth cost savings during inter-shift transition periods."
        },
        "device_types": {
            "insight": "Six distinct device types create a diverse monitoring ecosystem. CNC Machine Monitors and Vibration Sensors are most critical for predictive maintenance.",
            "action": "Deploy edge computing gateways for CNC and vibration sensors, enabling local anomaly detection with 50 ms response time.",
            "outcome": "Detect bearing failures 48 hours before breakdown, preventing cascading equipment damage estimated at ~50K EUR per incident."
        },
        "city": {
            "insight": "Hasselt leads with 44 devices as Belgium's industrial manufacturing hub. Charleroi's 32 devices reflect the Walloon steel and chemical industry cluster.",
            "action": "Establish cross-factory connectivity platform linking Hasselt and Antwerp clusters for unified predictive maintenance analytics.",
            "outcome": "20% improvement in Overall Equipment Effectiveness (OEE) through cross-site production optimization and shared failure patterns."
        },
        "signal_battery": {
            "insight": "Industrial devices show wider signal variance (-50 to -85 dBm) due to metallic factory environments causing electromagnetic interference.",
            "action": "Deploy industrial-grade shielded antennas and signal repeaters optimized for metallic environments on factory floors.",
            "outcome": "30% signal strength improvement in heavy manufacturing areas, reducing data packet loss from 5% to below 0.5%."
        },
    },
    "Transport & Logistics": {
        "device_status": {
            "insight": "92.3% active fleet status is critical for supply chain visibility. The 7.7% non-active devices create blind spots in shipment tracking coverage.",
            "action": "Implement automatic failover to satellite connectivity for fleet devices entering cellular dead zones below -85 dBm.",
            "outcome": "100% shipment tracking coverage across Belgium's entire road network, including Ardennes tunnels and rural last-mile routes."
        },
        "connectivity": {
            "insight": "4G dominance at 43% reflects vehicle-mounted GPS tracker requirements. LTE-M at 33% serves container and trailer sensors needing extended battery life.",
            "action": "Upgrade Zeebrugge port and Mechelen logistics hub fleet to 5G for real-time autonomous warehouse robot coordination.",
            "outcome": "Real-time fleet orchestration enabling 15% improvement in warehouse throughput and 20% faster port container turnaround."
        },
        "daily_trends": {
            "insight": "Strong weekday patterns with Monday-Friday operational peaks. Alert concentration correlates with morning dispatch rushes and evening delivery windows.",
            "action": "Implement predictive capacity planning that reserves bandwidth headroom for known peak shipping days (month-end, holiday logistics).",
            "outcome": "Zero connectivity congestion during peak logistics periods, ensuring 100% tracking during Black Friday and holiday shipping surges."
        },
        "sim_type": {
            "insight": "eSIM at 39% is growing rapidly, driven by cross-border roaming needs for trucks on Belgium-Netherlands-Germany corridor routes.",
            "action": "Deploy BICS global eSIM profiles for all international route vehicles, enabling seamless multi-country connectivity switching.",
            "outcome": "Seamless EU corridor connectivity eliminating roaming gaps, with projected 35% savings on cross-border data costs."
        },
        "hourly": {
            "insight": "Primary operational window 5 AM - 9 PM with peak at 8-10 AM (morning dispatches). Overnight quiet shows only cold-chain monitoring activity.",
            "action": "Implement off-peak batch data synchronization for non-critical telemetry, reserving daytime bandwidth for real-time fleet tracking.",
            "outcome": "30% bandwidth cost savings through intelligent scheduling while maintaining real-time priority for fleet safety alerts."
        },
        "device_types": {
            "insight": "Cold Chain Monitors lead with 23% of fleet, reflecting Belgium's strategic role as EU pharmaceutical and food logistics hub.",
            "action": "Implement guaranteed sub-30-second latency SLA for all cold chain temperature excursion alerts to prevent compliance violations.",
            "outcome": "Prevent an estimated 2M EUR in annual cold chain spoilage losses through real-time temperature intervention capabilities."
        },
        "city": {
            "insight": "Mechelen (46 devices) and Zeebrugge (40) lead as Belgium's primary logistics corridors. Liege's 40 devices reflect the airport cargo hub importance.",
            "action": "Deploy dedicated connectivity micro-cells at Zeebrugge port and Liege Airport cargo zones for indoor precision tracking.",
            "outcome": "Improve indoor tracking accuracy from 10m to 1m in major logistics hubs, enabling automated inventory reconciliation."
        },
        "signal_battery": {
            "insight": "Vehicle-mounted devices show stable signal (-55 to -65 dBm) while portable trailer sensors exhibit wider variance and lower battery levels.",
            "action": "Deploy solar-powered charging stations at major trailer yards and install signal boosters at all loading dock areas.",
            "outcome": "99.9% connectivity uptime for trailer-mounted sensors, eliminating the current 8% tracking gap during yard operations."
        },
    },
    "OEM": {
        "device_status": {
            "insight": "92.1% active rate across a diverse OEM portfolio. The heterogeneous device mix creates varied connectivity requirements per product line.",
            "action": "Implement a device certification program with BICS connectivity profiles optimized and tested per OEM device category.",
            "outcome": "Standardized connectivity quality across all OEM partner devices, reducing integration testing time from 6 weeks to 5 days."
        },
        "connectivity": {
            "insight": "Diverse connectivity mix reflects OEM product variety - 5G for vehicles, LTE-M for smart meters, NB-IoT for environmental sensors across 200+ countries.",
            "action": "Offer multi-RAT BICS SIM supporting automatic network selection based on device location, data needs, and power constraints.",
            "outcome": "Seamless global roaming across 700+ MNO partners for all OEM devices, with single SIM managing all connectivity modes."
        },
        "daily_trends": {
            "insight": "Steady telemetry volume reflects a growing base of OEM device activations. Alert patterns are more uniform than other verticals due to diverse use cases.",
            "action": "Deploy an automated device onboarding API pipeline for OEM partners to self-service provision devices at global scale.",
            "outcome": "10x faster device provisioning, enabling OEM partners to activate 10,000+ devices per day during major product launches."
        },
        "sim_type": {
            "insight": "eSIM leads at 56% - the highest across all industries - reflecting modern OEM designs that prioritize embedded connectivity from the chip level.",
            "action": "Pioneer iSIM integration partnerships with top OEM chipset manufacturers for the smallest possible connectivity form factors.",
            "outcome": "Enable new OEM product categories including medical micro-implants, sub-1cm industrial sensors, and next-gen wearable devices."
        },
        "hourly": {
            "insight": "Business-hours peak (8 AM - 6 PM) from enterprise OEM devices, with a secondary evening consumer spike from connected vehicles and wearables.",
            "action": "Implement dual-profile connectivity management that separates enterprise and consumer OEM traffic for optimal QoS routing.",
            "outcome": "20% latency reduction for enterprise OEM devices during business hours without impacting consumer device experience."
        },
        "device_types": {
            "insight": "Connected Vehicle Modules (22% of fleet) are the largest and fastest-growing segment, driven by EU connected car regulatory mandates.",
            "action": "Develop an automotive-grade connectivity SLA with V2X readiness, positioning BICS as the preferred OEM connectivity partner.",
            "outcome": "Capture 30% of Belgium's connected vehicle connectivity market, representing 500K+ annual module activations by 2027."
        },
        "city": {
            "insight": "Brussels leads with 41 devices driven by OEM partner headquarters proximity. Ghent and Leuven reflect university-linked R&D testing programs.",
            "action": "Launch a pan-Belgian OEM Innovation Lab program with dedicated connectivity sandboxes in each major technology hub city.",
            "outcome": "45% OEM partner ecosystem growth within 18 months, attracting EU-based hardware startups to the BICS connectivity platform."
        },
        "signal_battery": {
            "insight": "Wide signal and battery spread reflects diverse OEM form factors - from vehicle modules (strong, stable) to micro-wearables (variable, constrained).",
            "action": "Create device-type-specific connectivity profiles with adaptive power management optimized per OEM product category.",
            "outcome": "30% average battery life improvement across the entire OEM portfolio through intelligent connectivity duty cycling."
        },
    },
}


def render_ai(rec):
    st.html(f"""
    <div class="ai-box">
        <div class="ai-s ai-i"><p class="ai-l">Insight</p><p class="ai-t">{rec['insight']}</p></div>
        <div class="ai-s ai-a"><p class="ai-l">Recommended Action</p><p class="ai-t">{rec['action']}</p></div>
        <div class="ai-s ai-o"><p class="ai-l">Possible Outcome</p><p class="ai-t">{rec['outcome']}</p></div>
    </div>
    """)


try:
    tab_labels = ["\U0001F33E Agriculture", "\U0001F3E5 Healthcare", "\U0001F3ED Manufacturing", "\U0001F69B Transport", "\U0001F4E1 OEM"]
    tabs = st.tabs(tab_labels)

    for tab, (industry, color) in zip(tabs, INDUSTRIES):
        with tab:
            recs = AI_RECS[industry]

            r = load_kpis(industry).iloc[0]
            k1, k2, k3, k4, k5, k6 = st.columns(6)
            for col, val, label in [
                (k1, f"{int(r['DEVICES']):,}", "Devices"),
                (k2, f"{int(r['READINGS']):,}", "Readings"),
                (k3, f"{int(r['ACTIVE']):,}", "Active"),
                (k4, f"{int(r['ALERTS']):,}", "Alerts"),
                (k5, f"{r['DATA_MB']:,.0f} MB", "Data Volume"),
                (k6, f"{r['AVG_BATTERY']:.0f}%", "Avg Battery"),
            ]:
                col.html(f'<div class="iot-kpi"><div class="iot-kpi-value">{val}</div><div class="iot-kpi-label">{label}</div></div>')

            st.html('<div style="margin-top:0.75rem"></div>')

            c1, c2 = st.columns(2)
            with c1:
                df = load_device_status(industry)
                fig = px.pie(df, names="DEVICE_STATUS", values="CNT", color="DEVICE_STATUS",
                             color_discrete_map=STATUS_COLORS, hole=0.5)
                fig.update_layout(**base_layout(title=ctitle("Device Status Distribution"),
                                               height=340, legend=dict(orientation="h", y=-0.1)))
                st.plotly_chart(fig, use_container_width=True)
                render_ai(recs["device_status"])

            with c2:
                df = load_connectivity(industry)
                fig = px.bar(df, x="CONNECTIVITY_TYPE", y="DEVICES", color="CONNECTIVITY_TYPE",
                             color_discrete_sequence=[color, BICS_COLORS["navy"], BICS_COLORS["gold"],
                                                      BICS_COLORS["green"], "#94a3b8"])
                fig.update_layout(**base_layout(title=ctitle("Connectivity Technology Breakdown"),
                                               height=340, showlegend=False, xaxis_title="", yaxis_title="Devices"))
                st.plotly_chart(fig, use_container_width=True)
                render_ai(recs["connectivity"])

            df = load_daily_trends(industry)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df["DATE"], y=df["READINGS"], name="Readings",
                                     mode="lines+markers", line=dict(color=color, width=2), marker=dict(size=4)))
            fig.add_trace(go.Bar(x=df["DATE"], y=df["ALERTS"], name="Alerts",
                                 marker_color="#EF4444", opacity=0.6, yaxis="y2"))
            fig.update_layout(**base_layout(title=ctitle("Daily Telemetry Volume & Alert Trends"),
                                           height=370, legend=dict(orientation="h", y=-0.15),
                                           margin=dict(l=20, r=60, t=50, b=20),
                                           yaxis=dict(title="Readings"), yaxis2=dict(title="Alerts", side="right", overlaying="y")))
            st.plotly_chart(fig, use_container_width=True)
            render_ai(recs["daily_trends"])

            c3, c4 = st.columns(2)
            with c3:
                df = load_sim(industry)
                fig = px.pie(df, names="SIM_TYPE", values="DEVICES", color="SIM_TYPE",
                             color_discrete_map={"eSIM": color, "Traditional SIM": BICS_COLORS["navy"], "iSIM": BICS_COLORS["gold"]},
                             hole=0.45)
                fig.update_layout(**base_layout(title=ctitle("SIM Technology Distribution"),
                                               height=340, legend=dict(orientation="h", y=-0.1)))
                st.plotly_chart(fig, use_container_width=True)
                render_ai(recs["sim_type"])

            with c4:
                df = load_hourly(industry)
                fig = px.area(df, x="HOUR", y="READINGS", color_discrete_sequence=[color])
                fig.update_layout(**base_layout(title=ctitle("Hourly Traffic Pattern (24h)"),
                                               height=340, xaxis=dict(title="Hour of Day", dtick=3), yaxis_title="Readings"))
                st.plotly_chart(fig, use_container_width=True)
                render_ai(recs["hourly"])

            c5, c6 = st.columns(2)
            with c5:
                df = load_device_types(industry)
                fig = px.bar(df, x="DEVICES", y="DEVICE_TYPE", orientation="h",
                             color="AVG_SIGNAL", color_continuous_scale=["#EF4444", "#F59E0B", "#10B981"],
                             labels={"AVG_SIGNAL": "Signal (dBm)"})
                fig.update_layout(**base_layout(title=ctitle("Device Fleet by Type & Signal Quality"),
                                               height=max(300, len(df) * 50 + 80),
                                               yaxis=dict(autorange="reversed"), xaxis_title="Devices", yaxis_title=""))
                st.plotly_chart(fig, use_container_width=True)
                render_ai(recs["device_types"])

            with c6:
                df = load_cities(industry)
                fig = px.bar(df, x="CITY", y="DEVICES", color="AVG_SIGNAL",
                             color_continuous_scale=["#EF4444", "#F59E0B", "#10B981"],
                             labels={"AVG_SIGNAL": "Signal (dBm)"})
                fig.update_layout(**base_layout(title=ctitle("Deployment by City & Signal Quality"),
                                               height=max(300, len(df) * 50 + 80),
                                               xaxis_title="", yaxis_title="Devices"))
                st.plotly_chart(fig, use_container_width=True)
                render_ai(recs["city"])

            df = load_device_health(industry)
            df["_S"] = df["ALERTS"] + 1
            fig = px.scatter(df, x="AVG_SIGNAL", y="AVG_BATTERY", color="DEVICE_TYPE",
                             size="_S", size_max=20, hover_data=["DEVICE_ID", "CITY", "ALERTS"],
                             color_discrete_sequence=px.colors.qualitative.Set2)
            fig.add_vrect(x0=-100, x1=-75, fillcolor="red", opacity=0.06, line_width=0,
                          annotation_text="Weak Signal Zone", annotation_position="top left",
                          annotation_font_size=10, annotation_font_color="#EF4444")
            fig.add_hrect(y0=0, y1=30, fillcolor="red", opacity=0.06, line_width=0,
                          annotation_text="Low Battery Zone", annotation_position="bottom right",
                          annotation_font_size=10, annotation_font_color="#EF4444")
            fig.update_layout(**base_layout(title=ctitle("Device Health Map: Signal Strength vs Battery Level"),
                                           height=420, xaxis_title="Avg Signal Strength (dBm)",
                                           yaxis_title="Avg Battery Level (%)",
                                           legend=dict(orientation="h", y=-0.2)))
            st.plotly_chart(fig, use_container_width=True)
            render_ai(recs["signal_battery"])

            st.html(f'<h3 style="color:#1E3A5F; margin-top:0.5rem;">Top Alerting Devices</h3>')
            alerts_df = load_top_alerting(industry)
            if not alerts_df.empty:
                st.dataframe(
                    alerts_df.rename(columns={
                        "DEVICE_ID": "Device", "DEVICE_TYPE": "Type", "CITY": "City",
                        "SITE_NAME": "Site", "ALERTS": "Alerts",
                        "AVG_SIGNAL": "Signal (dBm)", "AVG_BATTERY": "Battery (%)"
                    }),
                    use_container_width=True, hide_index=True,
                )
            else:
                st.info("No alerts recorded for this industry.")

except Exception as e:
    st.error(f"Error loading IoT data: {e}")
    st.info("Ensure IoT tables exist in BICS_TELCO.IOT_DATA schema.")
