import streamlit as st
from utils.styles import render_common_styles, BICS_COLORS

st.set_page_config(
    page_title="BICS - Belgium Mobility Intelligence",
    page_icon=":material/analytics:",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.logo("logo.png")
render_common_styles()

st.html("""
<style>
    .hero-section {
        background: linear-gradient(135deg, #1E3A5F 0%, #0891B2 50%, #1E3A5F 100%);
        background-size: 200% 200%;
        animation: heroGradient 8s ease infinite;
        padding: 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    @keyframes heroGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        pointer-events: none;
    }
    .hero-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        position: relative;
        z-index: 1;
    }
    .hero-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin: 0.5rem 0 1rem 0;
        position: relative;
        z-index: 1;
    }
    .hero-badges {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        position: relative;
        z-index: 1;
    }
    .hero-badge {
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(10px);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        border: 1px solid rgba(255,255,255,0.2);
    }
    .hero-badge.proximus { background: rgba(30, 58, 95, 0.8); }
    .hero-badge.iot { background: rgba(16, 185, 129, 0.8); }
    .hero-badge.roaming { background: rgba(8, 145, 178, 0.8); }
    
    .product-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem;
        height: 100%;
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    .product-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #0891B2, #1E3A5F);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    .product-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 16px 32px rgba(30, 58, 95, 0.12);
        border-color: #0891B2;
    }
    .product-card:hover::before {
        opacity: 1;
    }
    .product-icon {
        font-size: 2rem;
        margin-bottom: 0.75rem;
    }
    .product-title {
        color: #1E3A5F;
        font-weight: 700;
        font-size: 1.05rem;
        margin-bottom: 0.5rem;
    }
    .product-desc {
        color: #64748b;
        font-size: 0.85rem;
        line-height: 1.5;
        margin-bottom: 1rem;
    }
    .product-tags {
        display: flex;
        gap: 0.4rem;
        flex-wrap: wrap;
    }
    .product-tag {
        font-size: 0.7rem;
        padding: 0.2rem 0.6rem;
        border-radius: 10px;
        font-weight: 600;
    }
    .product-tag.published { background: #d1fae5; color: #065f46; }
    .product-tag.draft { background: #fef3c7; color: #92400e; }
    .product-tag.type { background: #e0e7ff; color: #3730a3; }
    
    .spec-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin-top: 1rem;
    }
    .spec-table th {
        background: linear-gradient(135deg, #1E3A5F, #0891B2);
        color: white;
        padding: 0.8rem 1rem;
        text-align: left;
        font-weight: 500;
        font-size: 0.85rem;
    }
    .spec-table th:first-child { border-radius: 8px 0 0 0; }
    .spec-table th:last-child { border-radius: 0 8px 0 0; }
    .spec-table td {
        padding: 0.75rem 1rem;
        border-bottom: 1px solid #e2e8f0;
        font-size: 0.85rem;
        color: #475569;
    }
    .spec-table tr:last-child td:first-child { border-radius: 0 0 0 8px; }
    .spec-table tr:last-child td:last-child { border-radius: 0 0 8px 0; }
    .spec-table tr:hover td { background: #f8fafc; }
    
    .cta-section {
        background: linear-gradient(135deg, #f0fdfa 0%, #e0f2fe 100%);
        border: 2px solid #0891B2;
        border-radius: 16px;
        padding: 1.5rem 2rem;
        text-align: center;
        margin-top: 2rem;
    }
    .cta-section h3 {
        color: #1E3A5F;
        margin: 0 0 0.5rem 0;
        font-size: 1.2rem;
    }
    .cta-section p {
        color: #64748b;
        margin: 0;
        font-size: 0.9rem;
    }
</style>
""")

st.html("""
<div class="hero-section">
    <h1 class="hero-title">BICS Mobility & IoT Intelligence</h1>
    <p class="hero-subtitle">Global Carrier Intelligence Platform — Powered by BICS (Proximus Global)</p>
    <div class="hero-badges">
        <span class="hero-badge proximus">700+ MNO Partners</span>
        <span class="hero-badge roaming">200+ Countries</span>
        <span class="hero-badge iot">5 IoT Industries</span>
        <span class="hero-badge">14 Belgian Cities</span>
        <span class="hero-badge">4.2M+ Roaming Records</span>
        <span class="hero-badge">1,000+ IoT Devices</span>
    </div>
</div>
""")

st.markdown("""
Aggregating anonymized roaming signaling data from BICS's global network of 
700+ MNO partners **and** real-time IoT telemetry across 5 enterprise verticals — enabling powerful location-based analytics and IoT intelligence.
""")

with st.container(horizontal=True):
    st.metric("Mobility Records", "4.2M+", border=True)
    st.metric("IoT Devices", "1,000+", border=True)
    st.metric("IoT Industries", "5", border=True)
    st.metric("MNO Partners", "700+", border=True)
    st.metric("Countries", "200+", border=True)
    st.metric("Data Period", "Jan 2026", border=True)

st.subheader(":material/inventory_2: Data Product Catalog", anchor=False)
st.caption("Aligned with TM Forum GB1086 Data Product Lifecycle Management (DPLM) v1.0")

st.markdown("**Mobility Data Products**")

mobility_offerings = [
    {
        "icon": ":material/store:",
        "title": "Retail Mobility Insights",
        "desc": "Site selection, foot traffic, competitor benchmarking",
        "type": "Consumer-Aligned",
        "status": "Published",
    },
    {
        "icon": ":material/account_balance:",
        "title": "Urban Planning Analytics",
        "desc": "Infrastructure planning, smart city, population density",
        "type": "Consumer-Aligned",
        "status": "Published",
    },
    {
        "icon": ":material/flight:",
        "title": "Tourism Flow Data",
        "desc": "Visitor flows, destination analytics, seasonal patterns",
        "type": "Source-Aligned",
        "status": "Published",
    },
    {
        "icon": ":material/directions_bus:",
        "title": "Transport Patterns",
        "desc": "Commuter patterns, route optimization, peak hours",
        "type": "Knowledge-Aligned",
        "status": "Draft",
    },
]

cols = st.columns(4)
for i, offer in enumerate(mobility_offerings):
    with cols[i]:
        with st.container(border=True):
            st.markdown(f"### {offer['icon']}")
            st.markdown(f"**{offer['title']}**")
            st.caption(offer['desc'])
            st.html(f'''
            <div class="product-tags">
                <span class="product-tag {"published" if offer["status"] == "Published" else "draft"}">{offer["status"]}</span>
                <span class="product-tag type">{offer["type"]}</span>
            </div>
            ''')

st.markdown("**IoT Data Products**")

iot_offerings = [
    {
        "icon": ":material/agriculture:",
        "title": "Agricultural IoT Insights",
        "desc": "Soil monitoring, precision farming, livestock tracking, irrigation analytics",
        "type": "Consumer-Aligned",
        "status": "Published",
    },
    {
        "icon": ":material/local_hospital:",
        "title": "Healthcare IoT Analytics",
        "desc": "Patient monitoring, asset tracking, cold chain, environmental compliance",
        "type": "Consumer-Aligned",
        "status": "Published",
    },
    {
        "icon": ":material/precision_manufacturing:",
        "title": "Industrial IoT Intelligence",
        "desc": "Predictive maintenance, vibration analysis, energy monitoring, OEE",
        "type": "Knowledge-Aligned",
        "status": "Published",
    },
    {
        "icon": ":material/local_shipping:",
        "title": "Fleet & Logistics Analytics",
        "desc": "Fleet GPS tracking, container monitoring, cold chain, fuel optimization",
        "type": "Consumer-Aligned",
        "status": "Published",
    },
    {
        "icon": ":material/developer_board:",
        "title": "Connected Device Management",
        "desc": "OEM device lifecycle, eSIM/iSIM analytics, edge compute monitoring",
        "type": "Source-Aligned",
        "status": "Published",
    },
]

cols = st.columns(5)
for i, offer in enumerate(iot_offerings):
    with cols[i]:
        with st.container(border=True):
            st.markdown(f"### {offer['icon']}")
            st.markdown(f"**{offer['title']}**")
            st.caption(offer['desc'])
            st.html(f'''
            <div class="product-tags">
                <span class="product-tag {"published" if offer["status"] == "Published" else "draft"}">{offer["status"]}</span>
                <span class="product-tag type">{offer["type"]}</span>
            </div>
            ''')

st.subheader(":material/description: Data Product Specification", anchor=False)
st.caption("Following DATSIS principles: Discoverable, Addressable, Trustworthy, Self-describing, Interoperable, Secure")

st.html("""
<table class="spec-table">
    <thead>
        <tr>
            <th style="width: 30%;">Attribute</th>
            <th>Details</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Domain Owner</strong></td>
            <td>BICS Mobility Analytics Team</td>
        </tr>
        <tr>
            <td><strong>Data Contract</strong></td>
            <td>SLA: 99.5% uptime | Freshness: Hourly refresh | Quality: >98% completeness</td>
        </tr>
        <tr>
            <td><strong>Access Patterns</strong></td>
            <td>SQL (Snowflake), REST API, Streamlit Dashboard</td>
        </tr>
        <tr>
            <td><strong>Lineage (Mobility)</strong></td>
            <td>BICS global roaming signaling (700+ MNO partners) &rarr; Anonymization &rarr; Aggregation &rarr; H3 Hexagons</td>
        </tr>
        <tr>
            <td><strong>Lineage (IoT)</strong></td>
            <td>1,000+ IoT devices (NB-IoT, LTE-M, 4G, 5G) &rarr; eSIM/iSIM/Traditional SIM &rarr; BICS IoT Platform &rarr; Telemetry Aggregation</td>
        </tr>
        <tr>
            <td><strong>IoT Industries</strong></td>
            <td>Agriculture &bull; Healthcare &bull; Industrial Manufacturing &bull; Transport &amp; Logistics &bull; OEM</td>
        </tr>
        <tr>
            <td><strong>Version</strong></td>
            <td>v2.0.0 (Jan 2026) | Lifecycle: Published</td>
        </tr>
    </tbody>
</table>
""")

with st.expander(":material/info: Data Product Types (TM Forum DPLM)"):
    st.markdown("""
    | Type | Description |
    |------|-------------|
    | **Source-Aligned** | Raw data with minimal transformation, preserves fidelity to source systems |
    | **Consumer-Aligned** | Optimized for specific use cases, aggregated and enriched for direct consumption |
    | **Knowledge-Aligned** | Semantic models and knowledge graphs for AI/ML reasoning |
    | **Standard-Aligned** | Conforms to TM Forum SID/ODA standards for cross-operator interoperability |
    """)

st.html("""
<div class="cta-section">
    <h3>:material/rocket_launch: Ready to Explore?</h3>
    <p>Navigate using the sidebar to explore data, view analytics, visualize maps, or export data packages.</p>
</div>
""")

with st.sidebar:
    st.caption("Roaming data: BICS global carrier network (700+ MNO partners, 200+ countries). IoT data: 5 industry verticals via BICS IoT connectivity platform. All data anonymized and aggregated.")
