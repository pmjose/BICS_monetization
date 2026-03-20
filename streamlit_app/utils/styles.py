"""
Shared styles and UI components for BICS Mobility Intelligence Dashboard.
Centralizes CSS and common UI patterns to reduce duplication.
"""
import streamlit as st

BICS_COLORS = {
    "navy": "#1E3A5F",
    "teal": "#0891B2",
    "gold": "#D4AF37",
    "green": "#10B981",
    "purple": "#8B5CF6",
    "slate": "#64748b",
    "light": "#f8fafc",
    "pink": "#EC4899",
    "orange": "#F97316",
    "cyan": "#06B6D4",
    "dark": "#0f172a",
}

SIDEBAR_CSS = """
<style>
    /* SIDEBAR BASE */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 50%, #0f172a 100%) !important;
        border-right: 1px solid rgba(8, 145, 178, 0.2) !important;
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"]::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: radial-gradient(ellipse at top left, rgba(8, 145, 178, 0.08) 0%, transparent 50%),
                    radial-gradient(ellipse at bottom right, rgba(212, 175, 55, 0.05) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }
    [data-testid="stSidebar"] > div:first-child { position: relative; z-index: 1; }
    
    /* LOGO STYLING */
    [data-testid="stSidebar"] [data-testid="stLogo"] {
        max-width: 100% !important;
        width: 100% !important;
        padding: 0.5rem 1rem !important;
    }
    [data-testid="stSidebar"] [data-testid="stLogo"] img {
        max-height: 80px !important;
        width: auto !important;
        height: auto !important;
        border-radius: 12px !important;
        padding: 8px !important;
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.1) !important;
        transition: all 0.3s ease !important;
    }
    [data-testid="stSidebar"] [data-testid="stLogo"] img:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 30px rgba(8, 145, 178, 0.4), 0 0 0 2px rgba(8, 145, 178, 0.3) !important;
    }
    
    /* NAV LINKS */
    [data-testid="stSidebar"] a {
        color: #ffffff !important;
        font-weight: 500 !important;
        padding: 0.75rem 1rem !important;
        border-radius: 10px !important;
        margin: 0.25rem 0.5rem !important;
        transition: all 0.3s ease !important;
        position: relative;
        overflow: hidden;
    }
    [data-testid="stSidebar"] a::before {
        content: '';
        position: absolute;
        left: 0; top: 0;
        height: 100%; width: 0;
        background: linear-gradient(90deg, rgba(8, 145, 178, 0.3), transparent);
        transition: width 0.3s ease;
        border-radius: 10px;
    }
    [data-testid="stSidebar"] a:hover {
        background: linear-gradient(135deg, rgba(8, 145, 178, 0.2) 0%, rgba(30, 58, 95, 0.3) 100%) !important;
        color: #ffffff !important;
        transform: translateX(4px);
    }
    [data-testid="stSidebar"] a:hover::before {
        width: 4px;
        background: linear-gradient(180deg, #0891B2, #D4AF37);
    }
    [data-testid="stSidebar"] a[aria-current="page"] {
        background: linear-gradient(135deg, rgba(8, 145, 178, 0.25) 0%, rgba(30, 58, 95, 0.4) 100%) !important;
        color: #ffffff !important;
        border-left: 3px solid #0891B2 !important;
    }
    
    /* SIDEBAR ELEMENTS */
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown p { color: #cbd5e1 !important; }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 { color: #f1f5f9 !important; font-weight: 600 !important; }
    [data-testid="stSidebar"] hr { border-color: rgba(8, 145, 178, 0.2) !important; margin: 1rem 0 !important; }
    [data-testid="stSidebar"] .stSelectbox > div > div,
    [data-testid="stSidebar"] .stMultiSelect > div > div {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(8, 145, 178, 0.3) !important;
        border-radius: 8px !important;
        color: #e2e8f0 !important;
        transition: all 0.3s ease !important;
    }
    [data-testid="stSidebar"] .stSelectbox > div > div:hover,
    [data-testid="stSidebar"] .stMultiSelect > div > div:hover {
        border-color: #0891B2 !important;
        box-shadow: 0 0 0 2px rgba(8, 145, 178, 0.15) !important;
    }
    [data-testid="stSidebar"] .stCaption { color: #64748b !important; font-size: 0.75rem !important; }
</style>
"""

PAGE_HEADER_CSS = """
<style>
    .page-header {
        background: linear-gradient(135deg, #1E3A5F 0%, #0891B2 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
        position: relative;
        overflow: hidden;
    }
    .page-header::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='M20 20h20v20H20V20zM0 0h20v20H0V0z'/%3E%3C/g%3E%3C/svg%3E");
        pointer-events: none;
    }
    .page-header h1 { 
        margin: 0; 
        font-size: 1.8rem; 
        font-weight: 700;
        position: relative;
        z-index: 1;
    }
    .page-header p { 
        margin: 0.3rem 0 0 0; 
        opacity: 0.9; 
        font-size: 0.95rem;
        position: relative;
        z-index: 1;
    }
</style>
"""

CARD_CSS = """
<style>
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }
    @keyframes pulse-border {
        0%, 100% { border-color: rgba(8, 145, 178, 0.2); }
        50% { border-color: rgba(8, 145, 178, 0.5); }
    }
    
    .bics-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.25rem;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .bics-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 3px;
        background: linear-gradient(90deg, #0891B2, #D4AF37, #10B981);
        background-size: 200% 100%;
        animation: shimmer 3s ease infinite;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    .bics-card:hover::before {
        opacity: 1;
    }
    .bics-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 20px 40px rgba(30, 58, 95, 0.12);
        border-color: #0891B2;
    }
    .bics-card-title {
        color: #1E3A5F;
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }
    .bics-card-desc {
        color: #64748b;
        font-size: 0.85rem;
        line-height: 1.5;
    }
    
    .insight-callout {
        background: linear-gradient(135deg, #fef3c7 0%, #fef9c3 100%);
        border-left: 4px solid #D4AF37;
        border-radius: 0 12px 12px 0;
        padding: 1rem 1.25rem;
        margin: 1rem 0;
    }
    .insight-callout p {
        color: #92400e;
        margin: 0;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    
    .eu-callout {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        border-left: 4px solid #10B981;
        border-radius: 0 12px 12px 0;
        padding: 1rem 1.25rem;
        margin: 1rem 0;
    }
    .eu-callout p {
        color: #065f46;
        margin: 0;
        font-size: 0.9rem;
        line-height: 1.6;
    }
</style>
"""


def render_common_styles():
    """Render shared sidebar and base styles. Call once per page."""
    st.html(SIDEBAR_CSS)
    st.html(PAGE_HEADER_CSS)
    st.html(CARD_CSS)


def render_page_header(title: str, subtitle: str = None):
    """Render a consistent page header with gradient background."""
    subtitle_html = f"<p>{subtitle}</p>" if subtitle else ""
    st.html(f"""
    <div class="page-header">
        <h1>{title}</h1>
        {subtitle_html}
    </div>
    """)


def render_insight_callout(text: str, icon: str = "lightbulb"):
    """Render a gold insight callout box."""
    st.html(f"""
    <div class="insight-callout">
        <p>:{icon}: <strong>Key Insight:</strong> {text}</p>
    </div>
    """)


def render_eu_callout(text: str):
    """Render a green EU/Belgium-specific callout box."""
    st.html(f"""
    <div class="eu-callout">
        <p><strong>Belgium / EU:</strong> {text}</p>
    </div>
    """)


def render_section_header(title: str, icon: str = None):
    """Render a section header with optional icon and divider line."""
    icon_html = f'<span style="margin-right: 0.5rem;">{icon}</span>' if icon else ""
    st.html(f"""
    <div style="display: flex; align-items: center; gap: 0.75rem; margin: 1.5rem 0 1rem 0;">
        <h3 style="color: #1E3A5F; font-size: 1.1rem; font-weight: 600; margin: 0;">
            {icon_html}{title}
        </h3>
        <div style="flex: 1; height: 2px; background: linear-gradient(90deg, #e2e8f0, transparent);"></div>
    </div>
    """)
