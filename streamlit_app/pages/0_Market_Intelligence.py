import streamlit as st
import altair as alt
import pandas as pd

st.set_page_config(page_title="Market Intelligence | BICS", page_icon="logo.png", layout="wide")

st.logo("logo.png")

BICS_BLUE = "#1E3A5F"
BICS_TEAL = "#0891B2"
BICS_GOLD = "#D4AF37"
BICS_GREEN = "#10B981"
BICS_PURPLE = "#8B5CF6"

st.html("""
<style>
    /* =========================================
       SIDEBAR STYLING
       ========================================= */
    @keyframes sidebarFadeIn {
        from { opacity: 0; transform: translateX(-10px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes glowPulse {
        0%, 100% { box-shadow: 0 4px 15px rgba(8, 145, 178, 0.2); }
        50% { box-shadow: 0 4px 25px rgba(8, 145, 178, 0.4); }
    }
    @keyframes navItemSlide {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
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
    [data-testid="stSidebar"] [data-testid="stLogo"] { animation: sidebarFadeIn 0.5s ease-out; }
    [data-testid="stSidebar"] [data-testid="stLogo"] img {
        border-radius: 12px !important;
        padding: 8px !important;
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.1) !important;
        transition: all 0.3s ease !important;
        animation: glowPulse 3s ease-in-out infinite;
    }
    [data-testid="stSidebar"] [data-testid="stLogo"] img:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 30px rgba(8, 145, 178, 0.4), 0 0 0 2px rgba(8, 145, 178, 0.3) !important;
    }
    [data-testid="stSidebar"] a {
        color: #ffffff !important;
        font-weight: 500 !important;
        padding: 0.75rem 1rem !important;
        border-radius: 10px !important;
        margin: 0.25rem 0.5rem !important;
        transition: all 0.3s ease !important;
        position: relative;
        overflow: hidden;
        animation: navItemSlide 0.4s ease-out backwards;
    }
    [data-testid="stSidebar"] a:nth-child(1) { animation-delay: 0.1s; }
    [data-testid="stSidebar"] a:nth-child(2) { animation-delay: 0.15s; }
    [data-testid="stSidebar"] a:nth-child(3) { animation-delay: 0.2s; }
    [data-testid="stSidebar"] a:nth-child(4) { animation-delay: 0.25s; }
    [data-testid="stSidebar"] a:nth-child(5) { animation-delay: 0.3s; }
    [data-testid="stSidebar"] a:nth-child(6) { animation-delay: 0.35s; }
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
    
    /* =========================================
       ANIMATIONS - PROFESSIONAL EDITION
       ========================================= */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes countUp {
        from { opacity: 0; transform: scale(0.5); }
        to { opacity: 1; transform: scale(1); }
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 20px rgba(8, 145, 178, 0.3); }
        50% { box-shadow: 0 0 40px rgba(8, 145, 178, 0.6); }
    }
    @keyframes borderGlow {
        0%, 100% { border-color: rgba(8, 145, 178, 0.3); }
        50% { border-color: rgba(8, 145, 178, 0.8); }
    }
    @keyframes scaleIn {
        from { opacity: 0; transform: scale(0.8); }
        to { opacity: 1; transform: scale(1); }
    }
    @keyframes rotateIn {
        from { opacity: 0; transform: rotate(-10deg) scale(0.9); }
        to { opacity: 1; transform: rotate(0) scale(1); }
    }
    @keyframes typewriter {
        from { width: 0; }
        to { width: 100%; }
    }
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0; }
    }
    @keyframes ripple {
        0% { transform: scale(0.8); opacity: 1; }
        100% { transform: scale(2.4); opacity: 0; }
    }
    @keyframes morphGradient {
        0% { background-position: 0% 50%; filter: hue-rotate(0deg); }
        50% { background-position: 100% 50%; filter: hue-rotate(15deg); }
        100% { background-position: 0% 50%; filter: hue-rotate(0deg); }
    }
    @keyframes particleFloat {
        0%, 100% { transform: translateY(0) rotate(0deg); opacity: 0.6; }
        25% { transform: translateY(-20px) rotate(90deg); opacity: 1; }
        50% { transform: translateY(-40px) rotate(180deg); opacity: 0.6; }
        75% { transform: translateY(-20px) rotate(270deg); opacity: 1; }
    }
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    @keyframes breathe {
        0%, 100% { transform: scale(1); opacity: 0.8; }
        50% { transform: scale(1.02); opacity: 1; }
    }
    
    .page-header {
        background: linear-gradient(135deg, #1E3A5F 0%, #0891B2 50%, #1E3A5F 100%);
        background-size: 200% 200%;
        animation: morphGradient 8s ease infinite, fadeInUp 0.8s ease-out;
        padding: 2.5rem 3rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
        position: relative;
        overflow: hidden;
        box-shadow: 0 15px 50px rgba(30, 58, 95, 0.3);
    }
    .page-header::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='M20 20h20v20H20V20zM0 0h20v20H0V0z'/%3E%3C/g%3E%3C/svg%3E");
    }
    .page-header::after {
        content: '';
        position: absolute;
        top: -50%; right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(212, 175, 55, 0.1) 0%, transparent 50%);
        animation: float 6s ease-in-out infinite;
    }
    .page-header h1 { 
        margin: 0; 
        font-size: 2.4rem; 
        font-weight: 800; 
        position: relative; 
        z-index: 1;
        text-shadow: 0 2px 20px rgba(0, 0, 0, 0.3);
        animation: slideIn 0.6s ease-out 0.2s backwards;
    }
    .page-header p { 
        margin: 0.75rem 0 0 0; 
        opacity: 0.95; 
        font-size: 1.1rem; 
        position: relative; 
        z-index: 1;
        animation: slideIn 0.6s ease-out 0.4s backwards;
    }
    
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin: 1.5rem 0 1rem 0;
        animation: slideIn 0.5s ease-out;
    }
    .section-header h3 {
        color: #1E3A5F;
        font-size: 1.15rem;
        font-weight: 700;
        margin: 0;
    }
    .section-line {
        flex: 1;
        height: 2px;
        background: linear-gradient(90deg, #e2e8f0, transparent);
    }
    
    .intro-card {
        background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.75rem;
        margin-bottom: 1rem;
        animation: fadeInUp 0.6s ease-out;
        transition: all 0.3s ease;
    }
    .intro-card:hover {
        box-shadow: 0 10px 40px rgba(30, 58, 95, 0.1);
        transform: translateY(-2px);
    }
    
    .questions-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        margin-top: 1.5rem;
    }
    @media (max-width: 768px) {
        .questions-grid { grid-template-columns: 1fr; }
    }
    .question-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e2e8f0;
        border-radius: 20px;
        padding: 1.75rem;
        animation: fadeInUp 0.7s ease-out backwards;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }
    .question-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 5px;
        height: 100%;
        background: linear-gradient(180deg, #0891B2, #1E3A5F);
        border-radius: 5px 0 0 5px;
        transition: width 0.4s ease, opacity 0.4s ease;
        opacity: 0.7;
    }
    .question-card::after {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(135deg, rgba(8, 145, 178, 0) 0%, rgba(8, 145, 178, 0.05) 100%);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    .question-card:hover {
        transform: translateY(-8px) translateX(8px);
        box-shadow: 0 20px 40px rgba(30, 58, 95, 0.15);
        border-color: #0891B2;
    }
    .question-card:hover::before {
        width: 8px;
        opacity: 1;
    }
    .question-card:hover::after {
        opacity: 1;
    }
    .question-card .q-icon {
        font-size: 1.75rem;
        margin-bottom: 1rem;
        display: inline-block;
        animation: float 3s ease-in-out infinite;
        position: relative;
        z-index: 1;
    }
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-6px); }
    }
    .question-card .q-title {
        color: #1E3A5F;
        font-weight: 700;
        font-size: 1.05rem;
        margin: 0 0 0.6rem 0;
        line-height: 1.4;
        position: relative;
        z-index: 1;
    }
    .question-card .q-desc {
        color: #64748b;
        font-size: 0.9rem;
        margin: 0;
        line-height: 1.7;
        position: relative;
        z-index: 1;
    }
    .question-card .q-arrow {
        position: absolute;
        bottom: 1.25rem;
        right: 1.25rem;
        color: #0891B2;
        font-size: 1.5rem;
        opacity: 0;
        transform: translateX(-15px);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .question-card:hover .q-arrow {
        opacity: 1;
        transform: translateX(0);
    }
    
    .stat-highlight {
        background: linear-gradient(135deg, #1E3A5F 0%, #0891B2 100%);
        border-radius: 20px;
        padding: 1.75rem 2rem;
        color: white;
        text-align: center;
        animation: scaleIn 0.6s ease-out backwards, glow 3s ease-in-out infinite;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    .stat-highlight::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
        background-size: 200% 200%;
        animation: shimmer 3s ease-in-out infinite;
    }
    .stat-highlight:hover {
        transform: scale(1.05) translateY(-5px);
        box-shadow: 0 20px 50px rgba(30, 58, 95, 0.4);
    }
    .stat-highlight .value {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        position: relative;
        z-index: 1;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        animation: countUp 1s ease-out backwards;
    }
    .stat-highlight .label {
        font-size: 0.9rem;
        opacity: 0.95;
        margin-top: 0.4rem;
        position: relative;
        z-index: 1;
    }
    
    .shift-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 20px;
        padding: 1.75rem;
        height: 100%;
        animation: fadeInUp 0.7s ease-out backwards;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    .shift-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, #1E3A5F, #0891B2, #D4AF37);
        background-size: 200% 100%;
        animation: shimmer 3s ease-in-out infinite;
    }
    .shift-card::after {
        content: '';
        position: absolute;
        bottom: 0; left: 0; right: 0; top: 0;
        background: radial-gradient(circle at bottom right, rgba(8, 145, 178, 0.05) 0%, transparent 50%);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    .shift-card:hover {
        border-color: #0891B2;
        box-shadow: 0 15px 40px rgba(30, 58, 95, 0.15);
        transform: translateY(-6px);
    }
    .shift-card:hover::after {
        opacity: 1;
    }
    .shift-number {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #1E3A5F, #0891B2);
        color: white;
        border-radius: 50%;
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 1rem;
        animation: scaleIn 0.5s ease-out backwards, pulse 2s ease-in-out infinite;
        box-shadow: 0 4px 15px rgba(8, 145, 178, 0.3);
    }
    .shift-title {
        color: #1E3A5F;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 0.75rem;
        position: relative;
        z-index: 1;
    }
    .shift-desc {
        color: #64748b;
        font-size: 0.9rem;
        line-height: 1.7;
        position: relative;
        z-index: 1;
    }
    .shift-example {
        background: linear-gradient(135deg, #f8fafc 0%, #f0f9ff 100%);
        border-radius: 12px;
        padding: 1rem;
        margin-top: 1rem;
        font-size: 0.85rem;
        color: #64748b;
        border-left: 4px solid #D4AF37;
        position: relative;
        z-index: 1;
        transition: all 0.3s ease;
    }
    .shift-card:hover .shift-example {
        background: linear-gradient(135deg, #fef9c3 0%, #fef3c7 100%);
    }
    
    .buyer-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.25rem;
        animation: fadeInUp 0.5s ease-out backwards;
        transition: all 0.3s ease;
    }
    .buyer-card:hover {
        border-color: #0891B2;
        box-shadow: 0 8px 25px rgba(30, 58, 95, 0.1);
    }
    .buyer-icon {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .buyer-title {
        color: #1E3A5F;
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 0.3rem;
    }
    .buyer-uses {
        color: #64748b;
        font-size: 0.8rem;
        line-height: 1.5;
    }
    
    .pricing-model {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: left;
        transition: all 0.3s ease;
        animation: fadeInUp 0.6s ease-out backwards;
        height: 100%;
    }
    .pricing-model:hover {
        border-color: #0891B2;
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(30, 58, 95, 0.12);
    }
    .pricing-model.recommended {
        border-color: #0891B2;
        background: linear-gradient(180deg, #f0fdfa 0%, #ffffff 100%);
    }
    .pricing-icon {
        font-size: 1.8rem;
        margin-bottom: 0.75rem;
    }
    .pricing-name {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1E3A5F;
        margin-bottom: 0.5rem;
    }
    .pricing-desc {
        color: #64748b;
        font-size: 0.85rem;
        line-height: 1.5;
        margin-bottom: 1rem;
    }
    .pricing-details {
        background: #f8fafc;
        border-radius: 8px;
        padding: 0.75rem;
        font-size: 0.8rem;
        color: #64748b;
    }
    .pricing-tag {
        display: inline-block;
        background: #0891B2;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
    }
    
    .distribution-option {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem;
        animation: fadeInUp 0.6s ease-out backwards;
        transition: all 0.3s ease;
        height: 100%;
    }
    .distribution-option:hover {
        border-color: #0891B2;
        box-shadow: 0 10px 30px rgba(30, 58, 95, 0.1);
        transform: translateY(-3px);
    }
    .distribution-icon {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #1E3A5F, #0891B2);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    .distribution-title {
        font-size: 1rem;
        font-weight: 700;
        color: #1E3A5F;
        margin-bottom: 0.5rem;
    }
    .distribution-desc {
        color: #64748b;
        font-size: 0.85rem;
        line-height: 1.6;
    }
    .distribution-tag {
        display: inline-block;
        background: #f0fdfa;
        color: #0891B2;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: 1rem;
    }
    .distribution-tag.warning {
        background: #fef3c7;
        color: #92400e;
    }
    
    .key-insight {
        background: linear-gradient(135deg, #fef3c7 0%, #fef9c3 100%);
        border-left: 5px solid #D4AF37;
        border-radius: 0 16px 16px 0;
        padding: 1.25rem 1.5rem;
        margin: 1.5rem 0;
        animation: slideInRight 0.6s ease-out;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    .key-insight::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(90deg, rgba(212, 175, 55, 0.1) 0%, transparent 50%);
        animation: shimmer 5s ease-in-out infinite;
    }
    .key-insight:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 25px rgba(212, 175, 55, 0.2);
    }
    .key-insight p {
        color: #92400e;
        margin: 0;
        font-size: 0.95rem;
        line-height: 1.6;
        position: relative;
        z-index: 1;
    }
    
    .eu-highlight {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        border-left: 5px solid #10B981;
        border-radius: 0 16px 16px 0;
        padding: 1.25rem 1.5rem;
        margin: 1.5rem 0;
        animation: slideInRight 0.6s ease-out;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    .eu-highlight::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(90deg, rgba(16, 185, 129, 0.1) 0%, transparent 50%);
    }
    .eu-highlight:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.2);
    }
    .eu-highlight p {
        color: #065f46;
        margin: 0;
        font-size: 0.95rem;
        line-height: 1.6;
        position: relative;
        z-index: 1;
    }
    
    .source-ref {
        color: #94a3b8;
        font-size: 0.75rem;
        font-style: italic;
        margin-top: 0.5rem;
    }
    
    .position-box {
        background: linear-gradient(135deg, #1E3A5F 0%, #0891B2 100%);
        background-size: 200% 200%;
        animation: morphGradient 6s ease infinite, scaleIn 0.6s ease-out;
        border-radius: 16px;
        padding: 1.5rem 1.75rem;
        color: white;
        margin-top: 1.5rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(30, 58, 95, 0.3);
    }
    .position-box::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
        background-size: 200% 200%;
        animation: shimmer 4s ease-in-out infinite;
    }
    .position-box p {
        margin: 0;
        font-size: 0.95rem;
        line-height: 1.7;
        position: relative;
        z-index: 1;
    }
    .position-box strong {
        color: #D4AF37;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
    }
</style>
""")

st.html("""
<div class="page-header">
    <h1>Market Intelligence</h1>
    <p>Understanding the telco data monetization landscape</p>
</div>
""")

tab_intro, tab_trends, tab_demand, tab_pricing, tab_distribution, tab_references = st.tabs([
    "📋 Intro",
    "📈 Data Product Trends",
    "🎯 Market Demand",
    "💰 Pricing Models",
    "🌐 Data Distribution",
    "📚 References"
])

# =============================================================================
# TAB 1: INTRO
# =============================================================================
with tab_intro:
    st.html("""
    <div class="section-header">
        <h3>📌 About This Dashboard</h3>
        <div class="section-line"></div>
    </div>
    
    <div style="text-align: right; margin-top: 1rem; padding-right: 0.5rem;">
        <span style="color: #64748b; font-size: 0.8rem;">📄 Source: <a href="https://www.tmforum.org/resources/guidebook/gb1086-data-product-lifecycle-management-dplm-establishing-an-operational-model-for-telco-data-v1-0-0/" target="_blank" style="color: #0891B2; text-decoration: none;">TM Forum GB1086 DPLM v1.0.0</a></span>
    </div>
    """)
    
    st.html("""
    <p style="color: #64748b; font-size: 1rem; line-height: 1.7; margin-bottom: 0.5rem;">
        This Market Intelligence dashboard addresses <strong style="color: #1E3A5F;">key strategic questions from BICS</strong> 
        about telco data monetization. Each tab provides research, market data, and actionable insights.
    </p>
    
    <div class="questions-grid">
        <div class="question-card" style="animation-delay: 0.1s;">
            <div class="q-icon">📈</div>
            <p class="q-title">What is the telco data product trend?</p>
            <p class="q-desc">Three major shifts: from raw data to privacy-safe insights, from one-off deals to marketplaces, and AI-native use on governed products.</p>
            <span class="q-arrow">→</span>
        </div>
        <div class="question-card" style="animation-delay: 0.2s;">
            <div class="q-icon">🎯</div>
            <p class="q-title">What is the market demand for telco data products?</p>
            <p class="q-desc">Multi-billion dollar market with strong demand from public sector, retail, transport, financial services, and advertising verticals.</p>
            <span class="q-arrow">→</span>
        </div>
        <div class="question-card" style="animation-delay: 0.3s;">
            <div class="q-icon">💰</div>
            <p class="q-title">Is there a reference pricing model?</p>
            <p class="q-desc">A pricing toolbox: subscription/recurring licenses, usage-based/API-metered, flat licenses, freemium tiers, and outcome/revenue-share models.</p>
            <span class="q-arrow">→</span>
        </div>
        <div class="question-card" style="animation-delay: 0.4s;">
            <div class="q-icon">🌐</div>
            <p class="q-title">How to expose data to consumers without a Snowflake account?</p>
            <p class="q-desc">Multiple options: Reader accounts, "Powered-by BICS" portals, REST APIs, Clean Rooms, and file exports—all with Snowflake as the governed backend.</p>
            <span class="q-arrow">→</span>
        </div>
    </div>
    """)
    
    st.html("""
    <div class="section-header">
        <h3>🇪🇺 Belgium & EU Context: Digital Strategy & Data Governance</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.html("""
        <div class="intro-card">
            <h4 style="color: #1E3A5F; margin-top: 0;">EU Digital Strategy & Belgian Data Landscape</h4>
            <p style="color: #64748b; line-height: 1.7; margin-bottom: 1rem;">
                The European Commission's Digital Strategy drives Europe's data agenda. Belgium, as host to EU institutions,
                is at the forefront of data governance and digital transformation:
            </p>
            <ul style="color: #64748b; line-height: 1.8; margin: 0; padding-left: 1.25rem;">
                <li><strong>GDPR (2018)</strong> — World's most comprehensive data protection framework</li>
                <li><strong>EU Data Act (2024)</strong> — Fair access to and use of industrial and IoT data</li>
                <li><strong>EU AI Act (2025)</strong> — Risk-based framework for trustworthy AI deployment</li>
            </ul>
            <p class="source-ref">Source: ec.europa.eu, digital-strategy.ec.europa.eu</p>
        </div>
        """)
        
        st.html("""
        <div class="eu-highlight">
            <p>🇪🇺 <strong>EU Digital Decade 2030:</strong> The EU targets 75% of enterprises using cloud/AI by 2030,
            with <strong>20M+ ICT specialists</strong> across Europe. Belgium's Proximus Group (BICS parent) is
            a key enabler of cross-border digital infrastructure, connecting 700+ operators worldwide.</p>
        </div>
        """)
    
    with col2:
        st.html("""
        <div class="stat-highlight" style="margin-bottom: 1rem;">
            <p class="value">#1 GDPR</p>
            <p class="label">Data Protection Standard</p>
        </div>
        """)
        st.html("""
        <div class="stat-highlight" style="background: linear-gradient(135deg, #0891B2 0%, #10B981 100%); margin-bottom: 1rem;">
            <p class="value">700+</p>
            <p class="label">Operators Connected (BICS)</p>
        </div>
        """)
        st.html("""
        <div class="stat-highlight" style="background: linear-gradient(135deg, #D4AF37 0%, #F59E0B 100%);">
            <p class="value">27 EU</p>
            <p class="label">Member State Markets</p>
        </div>
        """)
    
    st.html("""
    <div class="section-header">
        <h3>🏗️ Belgian & EU Digital Initiatives</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    col1, col2, col3, col4 = st.columns(4)
    
    giga_projects = [
        {"icon": "🌆", "name": "Smart Brussels", "desc": "Capital region digital transformation with mobility-as-a-service"},
        {"icon": "🏙️", "name": "Port of Antwerp", "desc": "Europe's 2nd largest port, IoT-driven logistics and 5G innovation hub"},
        {"icon": "🏭", "name": "Flanders AI", "desc": "AI Research Program with industry partnerships across Flemish region"},
        {"icon": "🚄", "name": "EU Quarter", "desc": "Brussels European institutions district requiring visitor flow analytics"}
    ]
    
    for col, proj in zip([col1, col2, col3, col4], giga_projects):
        with col:
            with st.container(border=True):
                st.markdown(f"### {proj['icon']}")
                st.markdown(f"**{proj['name']}**")
                st.caption(proj['desc'])
    
    st.caption("Source: smartcity.brussels, portofantwerp.com, flandersai.be")
    
    st.html("""
    <div class="section-header">
        <h3>🇧🇪 Belgian Initiatives for BICS Data Products</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("**🏖️ Tourism & Cultural Heritage**")
            st.markdown("""
            - 🇧🇪 **Visit Flanders** — Tourism board requiring visitor flow & seasonal analytics
            - 🇧🇪 **Bruges Historic Center** — UNESCO site needing crowd density management
            - 🇧🇪 **Wallonia Tourism** — Regional tourism requiring origin-destination analytics
            - 🇧🇪 **Belgian Coast** — Seasonal tourism requiring capacity planning
            - 🇧🇪 **Ardennes Region** — Nature tourism requiring visitor flow analytics
            """)
            st.caption("Source: visitflanders.com, walloniabelgiumtourism.co.uk")
        
        with st.container(border=True):
            st.markdown("**🎭 Events & Festivals**")
            st.markdown("""
            - 🇧🇪 **Tomorrowland** — World's largest EDM festival requiring crowd analytics
            - 🇧🇪 **Gentse Feesten** — 10-day city festival needing real-time density management
            - 🇧🇪 **Belgian Grand Prix** — Spa-Francorchamps F1 requiring visitor flow planning
            - 🇧🇪 **Carnival of Binche** — UNESCO heritage event crowd management
            """)
            st.caption("Source: tomorrowland.com, gentsefeesten.be")
    
    with col2:
        with st.container(border=True):
            st.markdown("**🏘️ Urban & Real Estate**")
            st.markdown("""
            - 🇧🇪 **Antwerp Smart Zone** — Urban innovation district requiring mobility analytics
            - 🇧🇪 **Brussels Canal District** — Urban renewal requiring footfall & retail analytics
            - 🇧🇪 **Ghent Living Lab** — Smart city pilot needing visitor analytics
            - 🇧🇪 **Liege Guillemins Quarter** — Transit hub development requiring flow insights
            - 🇧🇪 **Green Deal Belgium** — Environmental planning with mobility correlation
            """)
            st.caption("Source: smartcity.brussels, antwerpen.be")
        
        with st.container(border=True):
            st.markdown("**🎢 Entertainment & Sports**")
            st.markdown("""
            - 🇧🇪 **Belgian Pro League** — Football stadiums requiring matchday analytics
            - 🇧🇪 **Walibi Belgium** — Theme park requiring visitor flow & experience analytics
            - 🇧🇪 **Brussels Expo/Heizel** — Exhibition center needing event crowd management
            - 🇧🇪 **Flanders Classics** — Cycling events requiring route & spectator analytics
            """)
            st.caption("Source: proleague.be, walibibelgium.be")
    
    st.html("""
    <div class="section-header">
        <h3>🔐 Data & AI Governance Initiatives</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container(border=True):
            st.markdown("**🏛️ EU Data Governance**")
            st.markdown("""
            European Data Strategy frameworks:
            - EU Data Governance Act
            - European Data Spaces
            - Open Data Directive
            - EU AI Ethics Guidelines
            """)
            st.caption("Source: ec.europa.eu")
    
    with col2:
        with st.container(border=True):
            st.markdown("**📜 GDPR Compliance**")
            st.markdown("""
            General Data Protection Regulation:
            - Consent management
            - Cross-border transfer (adequacy)
            - Data subject rights (Art. 15-22)
            - Privacy-by-design (Art. 25)
            """)
            st.caption("Source: gdpr.eu")
    
    with col3:
        with st.container(border=True):
            st.markdown("**🤖 Belgian AI & Innovation**")
            st.markdown("""
            Belgian AI ecosystem:
            - imec (nanotech/AI research)
            - Flanders AI Research Program
            - Proximus Ada (AI platform)
            - EuroHPC (Lumi supercomputer)
            """)
            st.caption("Source: imec.be, flandersai.be")
    
    st.html("""
    <div class="eu-highlight">
        <p>🇧🇪 <strong>BICS Opportunity:</strong> All flagged initiatives (🇧🇪) have <strong>explicit data requirements</strong> 
        that align with BICS's mobility, footfall, and network analytics capabilities. The combination of 
        EU digital transformation + GDPR governance frameworks + cross-border data flows creates a unique opportunity 
        for <strong>privacy-compliant telco data products</strong> at scale across 27 EU markets.</p>
    </div>
    """)
    
    st.markdown("---")
    st.markdown("**📚 Belgian & EU Initiative References:**")
    st.markdown("""
    - [EU Digital Strategy](https://digital-strategy.ec.europa.eu/en)
    - [EU Data Act](https://digital-strategy.ec.europa.eu/en/policies/data-act)
    - [GDPR Official Text](https://gdpr.eu/)
    - [Smart Brussels](https://smartcity.brussels/)
    - [Proximus Group](https://www.proximus.com/)
    - [BICS](https://www.bics.com/)
    - [imec Research](https://www.imec-int.com/)
    - [Flanders AI](https://flandersai.be/)
    """)

# =============================================================================
# TAB 2: TELCO DATA PRODUCT TRENDS
# =============================================================================
with tab_trends:
    st.html("""
    <div class="section-header">
        <h3>📦 What is a Data Product?</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    st.html("""
    <style>
        .dp-hero-section {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        @media (max-width: 900px) {
            .dp-hero-section { grid-template-columns: 1fr; }
        }
        
        .definition-card {
            background: #ffffff;
            border-radius: 20px;
            padding: 0;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(30, 58, 95, 0.08);
            border: 1px solid #e2e8f0;
            transition: all 0.3s ease;
        }
        .definition-card:hover {
            box-shadow: 0 12px 40px rgba(30, 58, 95, 0.12);
            transform: translateY(-4px);
        }
        .definition-card-header {
            background: linear-gradient(135deg, #0891B2 0%, #0e7490 100%);
            padding: 1rem 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        .definition-card-header .icon-wrapper {
            width: 36px;
            height: 36px;
            background: rgba(255,255,255,0.2);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .definition-card-header .icon-wrapper img {
            width: 22px;
            height: 22px;
        }
        .definition-card-header h4 {
            color: white;
            font-size: 1rem;
            font-weight: 600;
            margin: 0;
            letter-spacing: -0.01em;
        }
        .definition-card-body {
            padding: 1.5rem;
        }
        .definition-card-body p {
            color: #334155;
            font-size: 0.925rem;
            line-height: 1.75;
            margin: 0 0 1rem 0;
        }
        .definition-card-body p:last-of-type {
            margin-bottom: 0;
        }
        .definition-card-body strong {
            color: #1E3A5F;
            font-weight: 600;
        }
        .definition-card-footer {
            padding: 1rem 1.5rem;
            background: #f8fafc;
            border-top: 1px solid #e2e8f0;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .definition-card-footer .source-icon {
            color: #64748b;
            font-size: 0.85rem;
        }
        .definition-card-footer a {
            color: #0891B2;
            font-size: 0.8rem;
            text-decoration: none;
            font-weight: 500;
        }
        .definition-card-footer a:hover {
            text-decoration: underline;
        }
        
        .telco-card {
            background: #ffffff;
            border-radius: 20px;
            padding: 0;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(30, 58, 95, 0.08);
            border: 1px solid #e2e8f0;
            transition: all 0.3s ease;
        }
        .telco-card:hover {
            box-shadow: 0 12px 40px rgba(30, 58, 95, 0.12);
            transform: translateY(-4px);
        }
        .telco-card-header {
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            padding: 1rem 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        .telco-card-header .icon-wrapper {
            width: 36px;
            height: 36px;
            background: rgba(255,255,255,0.2);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1rem;
        }
        .telco-card-header h4 {
            color: white;
            font-size: 1rem;
            font-weight: 600;
            margin: 0;
            letter-spacing: -0.01em;
        }
        .telco-card-body {
            padding: 1.25rem 1.5rem;
        }
        .telco-item {
            display: flex;
            gap: 0.75rem;
            padding: 0.875rem 0;
            border-bottom: 1px solid #f1f5f9;
        }
        .telco-item:last-child {
            border-bottom: none;
            padding-bottom: 0;
        }
        .telco-item:first-child {
            padding-top: 0;
        }
        .telco-item .not-label {
            flex-shrink: 0;
            background: #fef2f2;
            color: #dc2626;
            font-size: 0.7rem;
            font-weight: 700;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            text-transform: uppercase;
            letter-spacing: 0.02em;
            height: fit-content;
            margin-top: 2px;
        }
        .telco-item .content {
            flex: 1;
        }
        .telco-item .what {
            color: #64748b;
            font-size: 0.85rem;
            margin-bottom: 0.25rem;
        }
        .telco-item .instead {
            color: #1E3A5F;
            font-size: 0.875rem;
            line-height: 1.5;
        }
        .telco-item .instead .highlight {
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            padding: 0.15rem 0.5rem;
            border-radius: 4px;
            font-weight: 600;
            color: #92400e;
        }
        
        .pillars-section {
            margin-top: 1.5rem;
        }
        .pillars-header {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 1rem;
        }
        .pillars-header h5 {
            color: #1E3A5F;
            font-size: 0.95rem;
            font-weight: 600;
            margin: 0;
        }
        .pillars-header .divider {
            flex: 1;
            height: 1px;
            background: linear-gradient(90deg, #e2e8f0, transparent);
        }
        .pillars-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1rem;
        }
        @media (max-width: 900px) {
            .pillars-grid { grid-template-columns: repeat(2, 1fr); }
        }
        .pillar-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 1.25rem;
            text-align: center;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        .pillar-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #1E3A5F, #0891B2);
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        .pillar-card:hover {
            transform: translateY(-6px);
            box-shadow: 0 12px 30px rgba(30, 58, 95, 0.12);
            border-color: #0891B2;
        }
        .pillar-card:hover::before {
            opacity: 1;
        }
        .pillar-card .icon {
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            margin: 0 auto 0.875rem auto;
        }
        .pillar-card .title {
            color: #1E3A5F;
            font-weight: 700;
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
        }
        .pillar-card .desc {
            color: #64748b;
            font-size: 0.8rem;
            line-height: 1.5;
        }
    </style>
    """)
    
    st.html("""
    <div class="dp-hero-section">
        <div class="definition-card">
            <div class="definition-card-header">
                <div class="icon-wrapper">❄️</div>
                <h4>Snowflake's Definition</h4>
            </div>
            <div class="definition-card-body">
                <p>A <strong>Data Product</strong> is a curated, governed, and reusable collection of data assets 
                designed to deliver specific value to a defined set of consumers.</p>
                <p>Unlike raw data exports, a data product is <strong>self-describing</strong> (metadata, documentation, quality metrics), 
                <strong>access-controlled</strong> (built-in governance and privacy), and 
                <strong>consumption-ready</strong> (optimized for specific use cases).</p>
                <p>Data products treat data as a <strong>product with a lifecycle</strong> — 
                versioned, maintained, monitored, and improved based on consumer feedback.</p>
            </div>
            <div class="definition-card-footer">
                <span class="source-icon">📚</span>
                <a href="https://www.snowflake.com/guides/what-is-a-data-product/" target="_blank">snowflake.com/guides/what-is-a-data-product</a>
            </div>
        </div>
        
        <div class="telco-card">
            <div class="telco-card-header">
                <div class="icon-wrapper">📡</div>
                <h4>What This Means in the Telco World</h4>
            </div>
            <div class="telco-card-body">
                <div class="telco-item">
                    <span class="not-label">Not</span>
                    <div class="content">
                        <div class="what">Raw CDRs or network logs</div>
                        <div class="instead">Instead → <span class="highlight">aggregated, anonymized insights</span> (mobility, footfall, dwell times)</div>
                    </div>
                </div>
                <div class="telco-item">
                    <span class="not-label">Not</span>
                    <div class="content">
                        <div class="what">One-off data dumps</div>
                        <div class="instead">Instead → <span class="highlight">continuously refreshed feeds</span> with SLAs & quality monitoring</div>
                    </div>
                </div>
                <div class="telco-item">
                    <span class="not-label">Not</span>
                    <div class="content">
                        <div class="what">"Take it or leave it"</div>
                        <div class="instead">Instead → <span class="highlight">tiered products</span> by geography, granularity, history depth</div>
                    </div>
                </div>
                <div class="telco-item">
                    <span class="not-label">Not</span>
                    <div class="content">
                        <div class="what">Uncontrolled sharing</div>
                        <div class="instead">Instead → <span class="highlight">privacy-safe delivery</span> via clean rooms & differential privacy</div>
                    </div>
                </div>
                <div class="telco-item">
                    <span class="not-label">Not</span>
                    <div class="content">
                        <div class="what">Just data</div>
                        <div class="instead">Instead → <span class="highlight">data + AI models + APIs</span> as a service</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="pillars-section">
        <div class="pillars-header">
            <h5>Core Pillars of a Data Product</h5>
            <div class="divider"></div>
        </div>
        <div class="pillars-grid">
            <div class="pillar-card">
                <div class="icon">📊</div>
                <div class="title">Curated Data</div>
                <div class="desc">Aggregated, cleaned, and validated — not raw network events</div>
            </div>
            <div class="pillar-card">
                <div class="icon">🔒</div>
                <div class="title">Built-in Governance</div>
                <div class="desc">Access policies, audit trails, and privacy controls embedded</div>
            </div>
            <div class="pillar-card">
                <div class="icon">📖</div>
                <div class="title">Self-Documenting</div>
                <div class="desc">Metadata, schemas, lineage, and quality metrics included</div>
            </div>
            <div class="pillar-card">
                <div class="icon">🎯</div>
                <div class="title">Use-Case Ready</div>
                <div class="desc">Optimized for specific outcomes (retail, transport, government)</div>
            </div>
        </div>
    </div>
    """)
    
    st.markdown("---")
    
    st.html("""
    <div class="section-header">
        <h3>🔄 Three Big Shifts in Telco Data Products</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.html("""
        <div class="shift-card" style="animation-delay: 0.1s;">
            <div class="shift-number">1</div>
            <div class="shift-title">From Raw Data to Privacy-Safe Insight Products</div>
            <div class="shift-desc">
                Operators are moving away from selling raw CDR/location feeds toward curated, anonymized 
                insight products: mobility & footfall, network quality, IoT/5G telemetry, fraud/risk signals, 
                customer intent, and more.
            </div>
            <div class="shift-example">
                <strong>Example:</strong> "Digital nervous system" products for cities—real-time density, 
                surge prediction, and recommended actions for transport, energy, and public safety packaged 
                as data products, not raw network logs.
            </div>
        </div>
        """)
    
    with col2:
        st.html("""
        <div class="shift-card" style="animation-delay: 0.2s;">
            <div class="shift-number">2</div>
            <div class="shift-title">From One-Off Deals to Marketplaces & Platforms</div>
            <div class="shift-desc">
                Telcos increasingly publish their data products through data marketplaces and clean rooms, 
                so partners (cities, retailers, banks, advertisers) can subscribe to governed feeds and run 
                their own analytics without ever seeing raw subscriber identifiers.
            </div>
            <div class="shift-example">
                <strong>Key principle:</strong> "This is not about selling raw telco data, it's about a 
                trusted collaboration platform for insights."
            </div>
        </div>
        """)
    
    with col3:
        st.html("""
        <div class="shift-card" style="animation-delay: 0.3s;">
            <div class="shift-number">3</div>
            <div class="shift-title">AI-Native / Agentic Use on Governed Products</div>
            <div class="shift-desc">
                The next wave is AI/agent-assist on top of these data products: call-center intent detection, 
                agent assist, network ops copilots—all using the same governed products with masking and 
                row-level policies.
            </div>
            <div class="shift-example">
                <strong>The pattern:</strong> Build reusable, policy-attached telco data products once; 
                reuse them across dashboards, AI, and partner use cases.
            </div>
        </div>
        """)
    
    st.html("""
    <div class="position-box">
        <p><strong>BICS Opportunity:</strong> "Build a catalog of governed telco data products 
        (mobility, network, CX, IoT) that power AI and analytics across any industry—retail, finance, 
        healthcare, smart cities, and enterprise partnerships."</p>
    </div>
    """)
    
    st.html("""
    <div class="section-header">
        <h3>📊 Data Product Categories</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    products_data = pd.DataFrame({
        'Category': ['Mobility & Footfall', 'Audience Segments', 'Network Quality', 'Fraud & Risk Signals', 'IoT / 5G Telemetry', 'Customer Intent'],
        'Maturity': [95, 85, 80, 75, 70, 65],
        'Privacy': ['Aggregated', 'Cohort-based', 'Aggregated', 'Scored', 'Device-level', 'Inferred'],
        'Icon': ['📍', '👥', '📶', '🛡️', '📡', '🎯']
    })
    
    st.html("""
    <style>
        .product-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin: 1rem 0;
        }
        @media (max-width: 768px) {
            .product-grid { grid-template-columns: repeat(2, 1fr); }
        }
        .product-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 1.25rem;
            position: relative;
            overflow: hidden;
            animation: fadeInUp 0.5s ease-out backwards;
            transition: all 0.3s ease;
        }
        .product-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 30px rgba(30, 58, 95, 0.12);
            border-color: #0891B2;
        }
        .product-card .card-icon {
            font-size: 1.8rem;
            margin-bottom: 0.5rem;
        }
        .product-card .card-name {
            color: #1E3A5F;
            font-weight: 700;
            font-size: 0.95rem;
            margin-bottom: 0.75rem;
        }
        .product-card .card-privacy {
            display: inline-block;
            background: #f0fdfa;
            color: #0891B2;
            padding: 0.2rem 0.6rem;
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: 600;
            margin-bottom: 0.75rem;
        }
        .product-card .progress-bar {
            background: #e2e8f0;
            border-radius: 6px;
            height: 8px;
            overflow: hidden;
        }
        .product-card .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #1E3A5F, #0891B2);
            border-radius: 6px;
            transition: width 1s ease-out;
        }
        .product-card .maturity-label {
            display: flex;
            justify-content: space-between;
            margin-top: 0.4rem;
            font-size: 0.75rem;
            color: #64748b;
        }
    </style>
    
    <div class="product-grid">
        <div class="product-card" style="animation-delay: 0.1s;">
            <div class="card-icon">📍</div>
            <div class="card-name">Mobility & Footfall</div>
            <div class="card-privacy">Aggregated</div>
            <div class="progress-bar"><div class="progress-fill" style="width: 95%;"></div></div>
            <div class="maturity-label"><span>Maturity</span><span>95%</span></div>
        </div>
        <div class="product-card" style="animation-delay: 0.15s;">
            <div class="card-icon">👥</div>
            <div class="card-name">Audience Segments</div>
            <div class="card-privacy">Cohort-based</div>
            <div class="progress-bar"><div class="progress-fill" style="width: 85%;"></div></div>
            <div class="maturity-label"><span>Maturity</span><span>85%</span></div>
        </div>
        <div class="product-card" style="animation-delay: 0.2s;">
            <div class="card-icon">📶</div>
            <div class="card-name">Network Quality</div>
            <div class="card-privacy">Aggregated</div>
            <div class="progress-bar"><div class="progress-fill" style="width: 80%;"></div></div>
            <div class="maturity-label"><span>Maturity</span><span>80%</span></div>
        </div>
        <div class="product-card" style="animation-delay: 0.25s;">
            <div class="card-icon">🛡️</div>
            <div class="card-name">Fraud & Risk Signals</div>
            <div class="card-privacy">Scored</div>
            <div class="progress-bar"><div class="progress-fill" style="width: 75%;"></div></div>
            <div class="maturity-label"><span>Maturity</span><span>75%</span></div>
        </div>
        <div class="product-card" style="animation-delay: 0.3s;">
            <div class="card-icon">📡</div>
            <div class="card-name">IoT / 5G Telemetry</div>
            <div class="card-privacy">Device-level</div>
            <div class="progress-bar"><div class="progress-fill" style="width: 70%;"></div></div>
            <div class="maturity-label"><span>Maturity</span><span>70%</span></div>
        </div>
        <div class="product-card" style="animation-delay: 0.35s;">
            <div class="card-icon">🎯</div>
            <div class="card-name">Customer Intent</div>
            <div class="card-privacy">Inferred</div>
            <div class="progress-bar"><div class="progress-fill" style="width: 65%;"></div></div>
            <div class="maturity-label"><span>Maturity</span><span>65%</span></div>
        </div>
    </div>
    """)
    
    st.html("""
    <div class="section-header">
        <h3>🇪🇺 EU Alignment</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    st.html("""
    <div class="eu-highlight">
        <p>🇪🇺 <strong>EU Opportunity:</strong> The EU Data Spaces initiative explicitly
        targets cross-border data sharing for smart cities and mobility. BICS's mobility, network, and 
        CX data products directly align with EU needs for real-time density analytics, urban 
        planning, and cross-border analytics.</p>
    </div>
    """)
    
    # TM Forum Section
    st.html("""
    <div class="section-header">
        <h3>📚 TM Forum Industry Guidance</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    st.markdown("""
    **TM Forum**, the global industry association for digital business, provides comprehensive guidance 
    on telco data monetization through its Open Digital Framework and research publications.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("**📘 IG1138: External Data Monetization Guide**")
            st.markdown("""
            TM Forum's flagship guide for CSP data monetization covers:
            
            - **Regulations & Compliance** — Privacy requirements by jurisdiction
            - **Privacy Techniques** — Anonymization, aggregation, differential privacy
            - **10 Monetization Use Cases** across Health, Transportation, Finance/Fraud, 
              Advertising, Site Planning, and Tourism
            - **Revenue Conversion** — Moving from data assets to commercial products
            """)
            st.caption("Source: TM Forum IG1138 R15.5.1")
        
        with st.container(border=True):
            st.markdown("**🔄 ODA Monetization Engine**")
            st.markdown("""
            TM Forum's Open Digital Architecture (ODA) provides a standards-based platform to:
            
            - **Unify fragmented data** across legacy and modern systems
            - **Apply governance & automation** frameworks consistently
            - **Convert data assets** into revenue-generating services
            - **Enable secure data movement** via TM Forum-certified APIs 
              (TMF620, TMF622, TMF638-642)
            """)
            st.caption("Source: TM Forum ODA Catalyst, 2024")
    
    with col2:
        with st.container(border=True):
            st.markdown("**🏪 Digital Marketplace Model**")
            st.markdown("""
            TM Forum research highlights **digital marketplaces** as the primary channel 
            for data monetization:
            
            - **Self-service discovery** — Partners find and subscribe to data products
            - **Micro-segmentation** — Target specific demographics geographically
            - **5G data explosion** — Mobile data usage projected to reach 56GB/smartphone by 2029
            - **IoT scale** — 55.7 billion IoT devices estimated by 2025
            """)
            st.caption("Source: TM Forum Inform, 'How telcos can monetize data through digital marketplaces'")
        
        with st.container(border=True):
            st.markdown("**⚠️ The Monetization Gap**")
            st.markdown("""
            TM Forum research identifies a critical challenge:
            
            > *"While CSPs possess vast data assets and have invested heavily in big data platforms, 
            most haven't achieved tangible ROI."*
            
            **Key barriers:** Legacy IT silos, fragmented data, lack of governance, 
            and inability to package data as consumable products.
            
            **Solution:** Move from static data collection to **dynamic intelligence exchange** 
            using governed, API-accessible data products.
            """)
            st.caption("Source: TM Forum IG1138")
    
    st.html("""
    <div class="key-insight">
        <p>💡 <strong>TM Forum Recommendation:</strong> CSPs should pursue <strong>external data monetization</strong> 
        (selling insights to third parties) alongside internal use cases to significantly increase revenue. 
        The shift is from being <strong>data custodians</strong> to <strong>digital service orchestrators</strong>.</p>
    </div>
    """)
    
    # TM Forum Use Cases
    st.html("""
    <div class="section-header">
        <h3>🎯 TM Forum Use Case Framework</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    tmf_use_cases = pd.DataFrame({
        'Vertical': ['🏥 Health', '🚗 Transportation', '🏦 Finance/Fraud', '📣 Advertising', '📍 Site Planning', '✈️ Tourism'],
        'Data Products': [
            'Population health patterns, mobility for outbreak tracking',
            'Traffic flow, commuter patterns, route optimization',
            'Fraud detection signals, credit risk scoring, geo-behavior',
            'Audience segments, campaign measurement, attribution',
            'Footfall analytics, catchment analysis, location scoring',
            'Visitor flows, origin-destination, seasonal patterns'
        ],
        'Privacy Model': ['Aggregated', 'Aggregated', 'Scored/Anonymized', 'Cohort-based', 'Aggregated', 'Aggregated']
    })
    
    with st.container(border=True):
        st.dataframe(
            tmf_use_cases,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Vertical": st.column_config.TextColumn("Industry Vertical", width="medium"),
                "Data Products": st.column_config.TextColumn("Example Data Products", width="large"),
                "Privacy Model": st.column_config.TextColumn("Privacy Model", width="medium")
            }
        )
    
    st.caption("Source: TM Forum IG1138 — Introductory Guide to External Data Monetization")
    
    # GSMA Section
    st.html("""
    <div class="section-header">
        <h3>🌐 GSMA Data Monetization Insights</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    st.markdown("""
    **GSMA Intelligence**, the research arm of the global mobile industry association representing 
    operators worldwide, provides critical market intelligence on telco data monetization opportunities.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("**📊 B2B Market Opportunity**")
            st.markdown("""
            GSMA identifies a **$400B addressable market** for B2B services beyond connectivity:
            
            - 🇪🇺 **Enterprise Digital Transformation:** 10% of operator revenue (2024-2030) 
            - 🇪🇺 **IoT Connections:** 26 billion globally by 2025
            - 🇪🇺 **AI Monetization:** 74% of operators testing generative AI
            - **Open Gateway:** 74% of operators committed to API exposure
            """)
            st.caption("Source: GSMA Mobile Economy 2025")
        
        with st.container(border=True):
            st.markdown("**🔑 Open Gateway Initiative**")
            st.markdown("""
            GSMA's Open Gateway enables telcos to monetize network capabilities via APIs:
            
            - 🇪🇺 **Number Verify** — SIM-based authentication *(itsme/eIDAS integration)*
            - 🇪🇺 **Device Location** — Verified geolocation *(Smart city/event management)*
            - 🇪🇺 **SIM Swap** — Fraud prevention signals *(Banking/fintech security)*
            - 🇪🇺 **Network Quality** — QoS on demand *(Enterprise 5G services)*
            """)
            st.caption("Reference: GSMA Open Gateway")
    
    with col2:
        with st.container(border=True):
            st.markdown("**🚀 2025 Monetization Themes**")
            st.markdown("""
            Key GSMA research themes for operator monetization:
            
            1. 🇪🇺 **Data-as-a-Service** — Packaging telco signals for enterprise *(BICS core)*
            2. 🇪🇺 **AI/ML Integration** — Intelligent network monetization *(EU AI Act alignment)*
            3. 🇪🇺 **B2B2X Models** — Platform plays beyond connectivity *(EU Digital Market demand)*
            4. 🇪🇺 **Privacy-First Analytics** — Compliant data products *(GDPR compliance)*
            """)
            st.caption("Source: GSMA Intelligence Research Themes")
        
        with st.container(border=True):
            st.markdown("**📈 Revenue Diversification Imperative**")
            st.markdown("""
            GSMA emphasizes the shift from pure connectivity revenue:
            
            - **Legacy:** Voice + Data subscriptions declining
            - 🇪🇺 **Growth:** B2B digital services, IoT, enterprise solutions
            - 🇪🇺 **Future:** Network APIs, AI services, data products
            
            Operators must become **digital service providers** not just connectivity pipes.
            """)
            st.caption("Source: GSMA Operator Strategies Report")
    
    st.html("""
    <div class="key-insight">
        <p>💡 <strong>GSMA Key Finding:</strong> The <strong>$400B B2B services opportunity</strong> represents 
        telcos' best path to revenue growth beyond saturating connectivity markets. Operators with mature 
        <strong>data product strategies</strong> and <strong>API monetization</strong> capabilities will 
        capture disproportionate value in this transition.</p>
    </div>
    """)
    
    st.html("""
    <div class="eu-highlight">
        <p>🇪🇺 <strong>EU Feature Alignment:</strong> Nearly all GSMA monetization themes are <strong>highly relevant</strong> 
        for Belgium and the EU. Key drivers: EU Digital Decade transformation mandates, Smart City projects 
        requiring real-time analytics, EU AI Act compliance, GDPR privacy requirements, and the 
        Proximus Group's push toward B2B enterprise services. BICS is positioned to deliver on all flagged (🇪🇺) use cases.</p>
    </div>
    """)
    
    st.markdown("---")
    st.markdown("**📚 GSMA Reference Materials:**")
    st.markdown("""
    - [GSMA: The Mobile Economy 2025](https://www.gsma.com/solutions-and-impact/connectivity-for-good/mobile-economy/wp-content/uploads/2025/02/030325-The-Mobile-Economy-2025.pdf)
    - [GSMA: Operator Strategies for Monetization](https://telecomlead.com/telecom-services/gsma-on-operator-strategies-for-monetization-and-customer-experience-119176)
    - [GSMA Open Gateway](https://www.gsma.com/solutions-and-impact/gsma-open-gateway/)
    - [GSMA Intelligence](https://www.gsmaintelligence.com/)
    """)

# =============================================================================
# TAB 3: MARKET DEMAND
# =============================================================================
with tab_demand:
    st.html("""
    <div class="section-header">
        <h3>📊 Market Size & Growth</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    st.html("""
    <style>
        @keyframes numberPop {
            0% { transform: scale(0.3) rotateY(-90deg); opacity: 0; }
            50% { transform: scale(1.1) rotateY(10deg); }
            100% { transform: scale(1) rotateY(0); opacity: 1; }
        }
        @keyframes slideUp {
            from { transform: translateY(40px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        @keyframes shimmer {
            0% { background-position: -200% 0; }
            100% { background-position: 200% 0; }
        }
        @keyframes borderPulse {
            0%, 100% { border-color: rgba(255,255,255,0.2); }
            50% { border-color: rgba(255,255,255,0.5); }
        }
        .market-stats-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1.5rem;
            margin-bottom: 1.5rem;
        }
        @media (max-width: 768px) {
            .market-stats-grid { grid-template-columns: 1fr; }
        }
        .market-stat-card {
            border-radius: 24px;
            padding: 2rem 1.75rem;
            text-align: center;
            position: relative;
            overflow: hidden;
            animation: slideUp 0.8s ease-out backwards;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
        }
        .market-stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            background-size: 200% 100%;
            animation: shimmer 4s ease-in-out infinite;
        }
        .market-stat-card::after {
            content: '';
            position: absolute;
            top: -50%; left: -50%;
            width: 200%; height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 40%);
            opacity: 0;
            transition: opacity 0.4s ease;
        }
        .market-stat-card:hover::after {
            opacity: 1;
        }
        .market-stat-card:hover {
            transform: translateY(-10px) scale(1.03);
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
        }
        .market-stat-card.blue {
            background: linear-gradient(135deg, #1E3A5F 0%, #0891B2 100%);
            box-shadow: 0 10px 30px rgba(30, 58, 95, 0.4);
        }
        .market-stat-card.teal {
            background: linear-gradient(135deg, #0891B2 0%, #10B981 100%);
            box-shadow: 0 10px 30px rgba(8, 145, 178, 0.4);
        }
        .market-stat-card.gold {
            background: linear-gradient(135deg, #D4AF37 0%, #F59E0B 100%);
            box-shadow: 0 10px 30px rgba(212, 175, 55, 0.4);
        }
        .market-stat-card .stat-value {
            font-size: 3.2rem;
            font-weight: 800;
            color: white;
            margin: 0;
            position: relative;
            z-index: 1;
            animation: numberPop 1s ease-out backwards;
            text-shadow: 0 4px 20px rgba(0,0,0,0.3);
            letter-spacing: -1px;
        }
        .market-stat-card .stat-label {
            font-size: 1rem;
            color: rgba(255,255,255,0.95);
            margin-top: 0.75rem;
            position: relative;
            z-index: 1;
            font-weight: 500;
        }
        .market-stat-card .stat-source {
            font-size: 0.75rem;
            color: rgba(255,255,255,0.7);
            margin-top: 1rem;
            position: relative;
            z-index: 1;
            font-style: italic;
            padding-top: 0.75rem;
            border-top: 1px solid rgba(255,255,255,0.2);
        }
    </style>
    
    <div class="market-stats-grid">
        <div class="market-stat-card blue" style="animation-delay: 0.1s;">
            <p class="stat-value" style="animation-delay: 0.3s;">~$5.3B</p>
            <p class="stat-label">Global Market 2024</p>
            <p class="stat-source">Precedence Research, 2024</p>
        </div>
        <div class="market-stat-card teal" style="animation-delay: 0.25s;">
            <p class="stat-value" style="animation-delay: 0.45s;">$14.9B</p>
            <p class="stat-label">Projected by 2029</p>
            <p class="stat-source">Market Research Future</p>
        </div>
        <div class="market-stat-card gold" style="animation-delay: 0.4s;">
            <p class="stat-value" style="animation-delay: 0.6s;">~24%</p>
            <p class="stat-label">CAGR Growth Rate</p>
            <p class="stat-source">Industry Consensus</p>
        </div>
    </div>
    """)
    
    st.html("""
    <div class="key-insight">
        <p>💡 <strong>Message:</strong> "This is now a multi-billion-dollar, high-growth segment, not an experiment."</p>
    </div>
    """)
    
    # Market growth chart
    market_data = pd.DataFrame({
        'Year': [2024, 2025, 2026, 2027, 2028, 2029],
        'Market Size ($B)': [5.3, 6.6, 8.2, 10.2, 12.5, 14.9],
        'Type': ['Actual'] + ['Projected'] * 5
    })
    
    st.html("""
    <style>
        @keyframes chartReveal {
            from { 
                clip-path: inset(0 100% 0 0);
                opacity: 0.5;
            }
            to { 
                clip-path: inset(0 0 0 0);
                opacity: 1;
            }
        }
        @keyframes pulseGlow {
            0%, 100% { box-shadow: 0 4px 20px rgba(8, 145, 178, 0.1); }
            50% { box-shadow: 0 4px 30px rgba(8, 145, 178, 0.25); }
        }
        .chart-container {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
            animation: fadeInUp 0.6s ease-out, pulseGlow 3s ease-in-out infinite;
            position: relative;
            overflow: hidden;
        }
        .chart-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #1E3A5F, #0891B2, #D4AF37);
            border-radius: 16px 16px 0 0;
        }
        .chart-title {
            font-size: 1.1rem;
            font-weight: 700;
            color: #1E3A5F;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .chart-title-icon {
            width: 32px;
            height: 32px;
            background: linear-gradient(135deg, #0891B2, #1E3A5F);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1rem;
        }
        .chart-subtitle {
            font-size: 0.85rem;
            color: #64748b;
            margin-bottom: 1rem;
        }
        .chart-wrapper {
            animation: chartReveal 1.5s ease-out 0.3s backwards;
        }
        .chart-sources {
            margin-top: 1rem;
            padding-top: 0.75rem;
            border-top: 1px solid #e2e8f0;
            font-size: 0.75rem;
            color: #94a3b8;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        .chart-sources::before {
            content: '📊';
        }
        .growth-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
            background: linear-gradient(135deg, #10B981, #34D399);
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            margin-left: auto;
            animation: pulse 2s ease-in-out infinite;
        }
    </style>
    <div class="chart-container">
        <div style="display: flex; align-items: center;">
            <div class="chart-title">
                <div class="chart-title-icon">📈</div>
                Global Telco Data Monetization Market Trajectory
            </div>
            <span class="growth-badge">↑ ~24% CAGR</span>
        </div>
        <div class="chart-subtitle">Projected growth from $5.3B (2024) to $14.9B (2029)</div>
    </div>
    """)
    
    market_chart = alt.Chart(market_data).mark_area(
        line={'color': '#DC2626', 'strokeWidth': 3},
        color=alt.Gradient(
            gradient='linear',
            stops=[
                alt.GradientStop(color='rgba(220, 38, 38, 0.4)', offset=0),
                alt.GradientStop(color='rgba(220, 38, 38, 0.05)', offset=1)
            ],
            x1=1, x2=1, y1=1, y2=0
        )
    ).encode(
        x=alt.X('Year:O', axis=alt.Axis(title='Year', labelAngle=0)),
        y=alt.Y('Market Size ($B):Q', axis=alt.Axis(title='Market Size ($ Billion)', grid=True, gridOpacity=0.3)),
        tooltip=[
            alt.Tooltip('Year:O', title='Year'),
            alt.Tooltip('Market Size ($B):Q', title='Market Size', format='$,.1f')
        ]
    ).properties(height=300)
    
    points = alt.Chart(market_data).mark_circle(size=100, color='#DC2626').encode(
        x='Year:O',
        y='Market Size ($B):Q'
    )
    
    st.altair_chart(market_chart + points, use_container_width=True)
    
    st.html("""
    <div class="chart-sources">
        📊 Sources: Precedence Research, Market Research Future, Mordor Intelligence — Telecom Data Monetization Market Reports 2024
    </div>
    """)
    
    st.html("""
    <div class="section-header">
        <h3>🎯 Who is Buying What?</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    st.html("""
    <style>
        .use-case-container {
            margin: 1.5rem 0;
        }
        .industry-section {
            margin-bottom: 2rem;
            animation: fadeInUp 0.6s ease-out backwards;
        }
        .industry-header {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 1rem;
            padding-bottom: 0.75rem;
            border-bottom: 2px solid #e2e8f0;
        }
        .industry-icon {
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, #1E3A5F, #0891B2);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
        }
        .industry-name {
            font-size: 1.1rem;
            font-weight: 700;
            color: #1E3A5F;
            margin: 0;
        }
        .industry-tag {
            background: #f0fdfa;
            color: #0891B2;
            padding: 0.2rem 0.6rem;
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: 600;
            margin-left: auto;
        }
        .industry-tag.hot {
            background: #fef3c7;
            color: #d97706;
        }
        .use-cases-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 0.75rem;
        }
        .use-case-chip {
            background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 0.875rem 1rem;
            display: flex;
            align-items: flex-start;
            gap: 0.6rem;
            transition: all 0.3s ease;
            animation: fadeInUp 0.4s ease-out backwards;
        }
        .use-case-chip:hover {
            border-color: #0891B2;
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(30, 58, 95, 0.1);
        }
        .use-case-chip .chip-icon {
            font-size: 1.2rem;
            flex-shrink: 0;
        }
        .use-case-chip .chip-content {
            flex: 1;
        }
        .use-case-chip .chip-title {
            font-weight: 600;
            font-size: 0.85rem;
            color: #1E3A5F;
            margin-bottom: 0.2rem;
        }
        .use-case-chip .chip-desc {
            font-size: 0.75rem;
            color: #64748b;
            line-height: 1.4;
        }
    </style>
    
    <div class="use-case-container">
        <!-- Government & Smart Cities -->
        <div class="industry-section" style="animation-delay: 0.1s;">
            <div class="industry-header">
                <div class="industry-icon">🏛️</div>
                <h4 class="industry-name">Government & Smart Cities</h4>
                <span class="industry-tag hot">High Priority for EU</span>
            </div>
            <div class="use-cases-grid">
                <div class="use-case-chip" style="animation-delay: 0.15s;">
                    <span class="chip-icon">📊</span>
                    <div class="chip-content">
                        <div class="chip-title">🇪🇺 Population Analytics</div>
                        <div class="chip-desc">Real-time density, demographic distribution</div>
                    </div>
                </div>
                <div class="use-case-chip" style="animation-delay: 0.2s;">
                    <span class="chip-icon">🚨</span>
                    <div class="chip-content">
                        <div class="chip-title">🇪🇺 Emergency Response</div>
                        <div class="chip-desc">Crowd surge prediction, evacuation planning</div>
                    </div>
                </div>
                <div class="use-case-chip" style="animation-delay: 0.25s;">
                    <span class="chip-icon">🏗️</span>
                    <div class="chip-content">
                        <div class="chip-title">🇪🇺 Infrastructure Planning</div>
                        <div class="chip-desc">Transport routes, utility demand forecasting</div>
                    </div>
                </div>
                <div class="use-case-chip" style="animation-delay: 0.3s;">
                    <span class="chip-icon">🎉</span>
                    <div class="chip-content">
                        <div class="chip-title">🇪🇺 Event Management</div>
                        <div class="chip-desc">Crowd flow, capacity optimization</div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Retail & Real Estate -->
        <div class="industry-section" style="animation-delay: 0.2s;">
            <div class="industry-header">
                <div class="industry-icon">🏪</div>
                <h4 class="industry-name">Retail & Real Estate</h4>
                <span class="industry-tag">High Demand</span>
            </div>
            <div class="use-cases-grid">
                <div class="use-case-chip" style="animation-delay: 0.25s;">
                    <span class="chip-icon">📍</span>
                    <div class="chip-content">
                        <div class="chip-title">🇪🇺 Site Selection</div>
                        <div class="chip-desc">Optimal store/branch locations</div>
                    </div>
                </div>
                <div class="use-case-chip" style="animation-delay: 0.3s;">
                    <span class="chip-icon">👣</span>
                    <div class="chip-content">
                        <div class="chip-title">🇪🇺 Foot Traffic Analysis</div>
                        <div class="chip-desc">Hourly/daily visitor patterns</div>
                    </div>
                </div>
                <div class="use-case-chip" style="animation-delay: 0.35s;">
                    <span class="chip-icon">🎯</span>
                    <div class="chip-content">
                        <div class="chip-title">Catchment Analysis</div>
                        <div class="chip-desc">Trade area, customer origin</div>
                    </div>
                </div>
                <div class="use-case-chip" style="animation-delay: 0.4s;">
                    <span class="chip-icon">⚔️</span>
                    <div class="chip-content">
                        <div class="chip-title">Competitive Intel</div>
                        <div class="chip-desc">Competitor foot traffic benchmarking</div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Tourism & Hospitality -->
        <div class="industry-section" style="animation-delay: 0.3s;">
            <div class="industry-header">
                <div class="industry-icon">✈️</div>
                <h4 class="industry-name">Tourism & Hospitality</h4>
                <span class="industry-tag hot">Growing Fast</span>
            </div>
            <div class="use-cases-grid">
                <div class="use-case-chip" style="animation-delay: 0.35s;">
                    <span class="chip-icon">🗺️</span>
                    <div class="chip-content">
                        <div class="chip-title">🇪🇺 Visitor Flow Mapping</div>
                        <div class="chip-desc">Tourist routes, attraction popularity</div>
                    </div>
                </div>
                <div class="use-case-chip" style="animation-delay: 0.4s;">
                    <span class="chip-icon">🌍</span>
                    <div class="chip-content">
                        <div class="chip-title">🇪🇺 Origin-Destination</div>
                        <div class="chip-desc">Where visitors come from</div>
                    </div>
                </div>
                <div class="use-case-chip" style="animation-delay: 0.45s;">
                    <span class="chip-icon">📅</span>
                    <div class="chip-content">
                        <div class="chip-title">🇪🇺 Seasonal Patterns</div>
                        <div class="chip-desc">Peak periods, trend forecasting</div>
                    </div>
                </div>
                <div class="use-case-chip" style="animation-delay: 0.5s;">
                    <span class="chip-icon">⏱️</span>
                    <div class="chip-content">
                        <div class="chip-title">Dwell Time Hotspots</div>
                        <div class="chip-desc">High-engagement areas</div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Transport & Logistics -->
        <div class="industry-section" style="animation-delay: 0.4s;">
            <div class="industry-header">
                <div class="industry-icon">🚌</div>
                <h4 class="industry-name">Transport & Logistics</h4>
                <span class="industry-tag">Steady Demand</span>
            </div>
            <div class="use-cases-grid">
                <div class="use-case-chip" style="animation-delay: 0.45s;">
                    <span class="chip-icon">🛤️</span>
                    <div class="chip-content">
                        <div class="chip-title">🇪🇺 Route Optimization</div>
                        <div class="chip-desc">Delivery efficiency, traffic patterns</div>
                    </div>
                </div>
                <div class="use-case-chip" style="animation-delay: 0.5s;">
                    <span class="chip-icon">🚇</span>
                    <div class="chip-content">
                        <div class="chip-title">🇪🇺 Commuter Analysis</div>
                        <div class="chip-desc">Peak hours, corridor demand</div>
                    </div>
                </div>
                <div class="use-case-chip" style="animation-delay: 0.55s;">
                    <span class="chip-icon">✈️</span>
                    <div class="chip-content">
                        <div class="chip-title">🇪🇺 Hub Capacity</div>
                        <div class="chip-desc">Airport/station planning</div>
                    </div>
                </div>
                <div class="use-case-chip" style="animation-delay: 0.6s;">
                    <span class="chip-icon">📦</span>
                    <div class="chip-content">
                        <div class="chip-title">Last-Mile Insights</div>
                        <div class="chip-desc">Delivery zone optimization</div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Financial Services -->
        <div class="industry-section" style="animation-delay: 0.5s;">
            <div class="industry-header">
                <div class="industry-icon">🏦</div>
                <h4 class="industry-name">Financial Services & Insurance</h4>
                <span class="industry-tag">Emerging</span>
            </div>
            <div class="use-cases-grid">
                <div class="use-case-chip" style="animation-delay: 0.55s;">
                    <span class="chip-icon">🛡️</span>
                    <div class="chip-content">
                        <div class="chip-title">Fraud Detection</div>
                        <div class="chip-desc">Location-based anomaly signals</div>
                    </div>
                </div>
                <div class="use-case-chip" style="animation-delay: 0.6s;">
                    <span class="chip-icon">📋</span>
                    <div class="chip-content">
                        <div class="chip-title">Risk Scoring</div>
                        <div class="chip-desc">Geo-behavior for underwriting</div>
                    </div>
                </div>
                <div class="use-case-chip" style="animation-delay: 0.65s;">
                    <span class="chip-icon">🏧</span>
                    <div class="chip-content">
                        <div class="chip-title">Branch Network</div>
                        <div class="chip-desc">ATM/branch placement optimization</div>
                    </div>
                </div>
                <div class="use-case-chip" style="animation-delay: 0.7s;">
                    <span class="chip-icon">💳</span>
                    <div class="chip-content">
                        <div class="chip-title">Credit Signals</div>
                        <div class="chip-desc">Alternative data for thin-file customers</div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Advertising & Media -->
        <div class="industry-section" style="animation-delay: 0.6s;">
            <div class="industry-header">
                <div class="industry-icon">📣</div>
                <h4 class="industry-name">Advertising & Media</h4>
                <span class="industry-tag">Privacy-First</span>
            </div>
            <div class="use-cases-grid">
                <div class="use-case-chip" style="animation-delay: 0.65s;">
                    <span class="chip-icon">👥</span>
                    <div class="chip-content">
                        <div class="chip-title">Audience Segments</div>
                        <div class="chip-desc">Privacy-safe cohorts for targeting</div>
                    </div>
                </div>
                <div class="use-case-chip" style="animation-delay: 0.7s;">
                    <span class="chip-icon">📺</span>
                    <div class="chip-content">
                        <div class="chip-title">OOH Measurement</div>
                        <div class="chip-desc">Billboard/screen exposure analytics</div>
                    </div>
                </div>
                <div class="use-case-chip" style="animation-delay: 0.75s;">
                    <span class="chip-icon">📈</span>
                    <div class="chip-content">
                        <div class="chip-title">Attribution</div>
                        <div class="chip-desc">Ad exposure to store visit</div>
                    </div>
                </div>
                <div class="use-case-chip" style="animation-delay: 0.8s;">
                    <span class="chip-icon">🎯</span>
                    <div class="chip-content">
                        <div class="chip-title">Campaign Measurement</div>
                        <div class="chip-desc">Reach, frequency, uplift</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """)
    
    st.html("""
    <div class="section-header">
        <h3>📱 How They Prefer to Consume</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    st.html("""
    <div class="intro-card">
        <p style="color: #64748b; line-height: 1.7; margin: 0;">
            TM Forum and market research show telcos moving to <strong>digital marketplaces and platforms</strong> 
            where enterprises can self-service discover, subscribe, and integrate telco data products rather 
            than bespoke one-offs. The shift is from custom integrations to standardized, governed data products 
            with clear APIs and SLAs.
        </p>
    </div>
    """)
    
    st.html("""
    <div class="position-box">
        <p><strong>For BICS:</strong> "We see strong demand from governments, banks, and retailers for exactly 
        the kinds of mobility, network and identity-adjacent signals BICS already has—as long as we deliver 
        them as <strong>governed products, not raw feeds</strong>."</p>
    </div>
    """)

# =============================================================================
# TAB 4: PRICING MODELS
# =============================================================================
with tab_pricing:
    st.html("""
    <div class="section-header">
        <h3>🧰 The Pricing Toolbox</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    st.markdown("""
    There's no single global tariff sheet, but there are clear patterns. Here's the pricing toolbox 
    telcos use for data products:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.html("""
        <div class="pricing-model recommended" style="animation-delay: 0.1s; margin-bottom: 1rem;">
            <div class="pricing-tag">MOST COMMON</div>
            <div class="pricing-icon">🔄</div>
            <div class="pricing-name">Subscription / Recurring Licenses</div>
            <div class="pricing-desc">
                Monthly/annual subscription per data product + geography + freshness 
                (e.g., Brussels daily mobility insights, Belgium-wide weekly, EU regional).
            </div>
            <div class="pricing-details">
                Often tiered by volume, history window, SLA, and number of users/use-cases. 
                Core revenue stream for real-time and historical insight feeds.
            </div>
        </div>
        """)
        
        st.html("""
        <div class="pricing-model" style="animation-delay: 0.3s; margin-bottom: 1rem;">
            <div class="pricing-icon">📁</div>
            <div class="pricing-name">Flat Licenses for Static/Historical Data</div>
            <div class="pricing-desc">
                One-off or annual license for historic archives (e.g., 3 years of aggregated mobility).
            </div>
            <div class="pricing-details">
                Often used for consulting, strategy projects, and model training. Lower recurring 
                revenue but good for market entry.
            </div>
        </div>
        """)
        
        st.html("""
        <div class="pricing-model" style="animation-delay: 0.5s;">
            <div class="pricing-icon">🎯</div>
            <div class="pricing-name">Outcome / Revenue-Share Models</div>
            <div class="pricing-desc">
                For advertising, insurance, or retail uplift, some telcos use rev-share or 
                success-based fees with partners.
            </div>
            <div class="pricing-details">
                Especially for "Powered-by-[Telco]" white-label platforms and APIs. Aligns 
                incentives but requires strong measurement.
            </div>
        </div>
        """)
    
    with col2:
        st.html("""
        <div class="pricing-model recommended" style="animation-delay: 0.2s; margin-bottom: 1rem;">
            <div class="pricing-tag">SCALABLE</div>
            <div class="pricing-icon">📊</div>
            <div class="pricing-name">Usage-Based / API-Metered</div>
            <div class="pricing-desc">
                Pay-per-API call, per 1k queries, or per 1k records scored (for prediction services).
            </div>
            <div class="pricing-details">
                Market studies highlight license fee, pay-per-use, and subscription as the main 
                commercial models. Great for developer adoption and variable workloads.
            </div>
        </div>
        """)
        
        st.html("""
        <div class="pricing-model" style="animation-delay: 0.4s;">
            <div class="pricing-icon">🎁</div>
            <div class="pricing-name">Freemium / Trial Tiers via Marketplaces</div>
            <div class="pricing-desc">
                Provide sample/low-granularity datasets for free; charge for higher resolution, 
                more history, or custom segments.
            </div>
            <div class="pricing-details">
                Trials, paid POCs, and usage-based experiments are standard practice for data 
                products. Reduces friction for new customers.
            </div>
        </div>
        """)
    
    st.html("""
    <div class="section-header">
        <h3>💡 Pricing Recommendation for BICS</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    st.html("""
    <div class="position-box">
        <p><strong>Recommended approach:</strong> "Globally we see subscription for core data products, 
        usage-based for APIs and predictions, and rev-share where we co-create services with partners. 
        We'd recommend starting simple (<strong>tiered subscription + usage-based API</strong>) and then 
        adding outcome-based pricing where we have strong partners like banks or ad platforms."</p>
    </div>
    """)
    
    st.html("""
    <div class="section-header">
        <h3>📋 Pricing Dimensions</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    st.html("""
    <style>
        .dimensions-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1rem;
            margin: 1rem 0;
        }
        @media (max-width: 900px) {
            .dimensions-grid { grid-template-columns: repeat(2, 1fr); }
        }
        @media (max-width: 500px) {
            .dimensions-grid { grid-template-columns: 1fr; }
        }
        .dimension-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 1.5rem;
            position: relative;
            overflow: hidden;
            animation: fadeInUp 0.5s ease-out backwards;
            transition: all 0.3s ease;
        }
        .dimension-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 30px rgba(30, 58, 95, 0.12);
            border-color: #0891B2;
        }
        .dimension-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            border-radius: 16px 16px 0 0;
        }
        .dimension-card.geo::before { background: linear-gradient(90deg, #1E3A5F, #0891B2); }
        .dimension-card.fresh::before { background: linear-gradient(90deg, #10B981, #34D399); }
        .dimension-card.volume::before { background: linear-gradient(90deg, #8B5CF6, #A78BFA); }
        .dimension-card.history::before { background: linear-gradient(90deg, #D4AF37, #F59E0B); }
        
        .dimension-header {
            display: flex;
            align-items: center;
            gap: 0.6rem;
            margin-bottom: 1rem;
        }
        .dimension-icon {
            width: 40px;
            height: 40px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.3rem;
        }
        .dimension-card.geo .dimension-icon { background: linear-gradient(135deg, #1E3A5F, #0891B2); }
        .dimension-card.fresh .dimension-icon { background: linear-gradient(135deg, #10B981, #34D399); }
        .dimension-card.volume .dimension-icon { background: linear-gradient(135deg, #8B5CF6, #A78BFA); }
        .dimension-card.history .dimension-icon { background: linear-gradient(135deg, #D4AF37, #F59E0B); }
        
        .dimension-name {
            font-weight: 700;
            font-size: 1rem;
            color: #1E3A5F;
        }
        .dimension-items {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }
        .dimension-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 0.75rem;
            background: #f8fafc;
            border-radius: 8px;
            font-size: 0.85rem;
            color: #475569;
            transition: all 0.2s ease;
        }
        .dimension-item:hover {
            background: #f0fdfa;
            color: #0891B2;
            transform: translateX(4px);
        }
        .dimension-item .item-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            flex-shrink: 0;
        }
        .dimension-card.geo .item-dot { background: #0891B2; }
        .dimension-card.fresh .item-dot { background: #10B981; }
        .dimension-card.volume .item-dot { background: #8B5CF6; }
        .dimension-card.history .item-dot { background: #D4AF37; }
    </style>
    
    <div class="dimensions-grid">
        <div class="dimension-card geo" style="animation-delay: 0.1s;">
            <div class="dimension-header">
                <div class="dimension-icon">🌍</div>
                <span class="dimension-name">Geography</span>
            </div>
            <div class="dimension-items">
                <div class="dimension-item"><span class="item-dot"></span>City-level</div>
                <div class="dimension-item"><span class="item-dot"></span>National (Belgium)</div>
                <div class="dimension-item"><span class="item-dot"></span>Regional (EU)</div>
                <div class="dimension-item"><span class="item-dot"></span>Custom zones</div>
            </div>
        </div>
        <div class="dimension-card fresh" style="animation-delay: 0.2s;">
            <div class="dimension-header">
                <div class="dimension-icon">⚡</div>
                <span class="dimension-name">Freshness</span>
            </div>
            <div class="dimension-items">
                <div class="dimension-item"><span class="item-dot"></span>Real-time</div>
                <div class="dimension-item"><span class="item-dot"></span>Hourly</div>
                <div class="dimension-item"><span class="item-dot"></span>Daily</div>
                <div class="dimension-item"><span class="item-dot"></span>Weekly / Monthly</div>
            </div>
        </div>
        <div class="dimension-card volume" style="animation-delay: 0.3s;">
            <div class="dimension-header">
                <div class="dimension-icon">📊</div>
                <span class="dimension-name">Volume</span>
            </div>
            <div class="dimension-items">
                <div class="dimension-item"><span class="item-dot"></span>Record count</div>
                <div class="dimension-item"><span class="item-dot"></span>Query limits</div>
                <div class="dimension-item"><span class="item-dot"></span>API calls/month</div>
                <div class="dimension-item"><span class="item-dot"></span>User seats</div>
            </div>
        </div>
        <div class="dimension-card history" style="animation-delay: 0.4s;">
            <div class="dimension-header">
                <div class="dimension-icon">📅</div>
                <span class="dimension-name">History</span>
            </div>
            <div class="dimension-items">
                <div class="dimension-item"><span class="item-dot"></span>30 days rolling</div>
                <div class="dimension-item"><span class="item-dot"></span>1 year archive</div>
                <div class="dimension-item"><span class="item-dot"></span>3+ years deep</div>
                <div class="dimension-item"><span class="item-dot"></span>Custom range</div>
            </div>
        </div>
    </div>
    """)
    
    st.markdown("---")
    st.markdown("##### Understanding Each Pricing Dimension")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("**🌍 Geography — Coverage Scope**")
            st.markdown("""
            Defines the spatial boundaries of the data product. Pricing typically increases with broader coverage:
            
            | Tier | Description | Use Case |
            |------|-------------|----------|
            | **City-level** | Single city (e.g., Brussels only) | Local retailers, municipal planning |
            | **National** | Full Belgium coverage | National brands, government ministries |
            | **Regional** | EU or Benelux region | Multi-country operators, regional banks |
            | **Custom zones** | POI-specific or geofenced areas | Mall operators, event venues, industrial zones |
            
            *Premium: Custom geofences around specific assets (e.g., Port of Antwerp, EU Quarter)*
            """)
        
        with st.container(border=True):
            st.markdown("**📊 Volume — Consumption Metrics**")
            st.markdown("""
            Controls how much data consumers can access. Common billing models:
            
            | Metric | Description | Typical Pricing |
            |--------|-------------|-----------------|
            | **Record count** | Number of rows/records delivered | Per 1M records |
            | **Query limits** | Max queries per period | Per 1K queries |
            | **API calls/month** | REST/GraphQL endpoint hits | Tiered brackets |
            | **User seats** | Named users with access | Per seat/month |
            
            *Enterprise: Unlimited queries with fair-use policy + dedicated compute*
            """)
    
    with col2:
        with st.container(border=True):
            st.markdown("**⚡ Freshness — Data Latency**")
            st.markdown("""
            How recent the data is when delivered. Lower latency = higher cost:
            
            | Tier | Latency | Premium | Use Case |
            |------|---------|---------|----------|
            | **Real-time** | < 5 min | 3-5x base | Emergency response, live events |
            | **Hourly** | 1-2 hours | 2x base | Dynamic pricing, traffic ops |
            | **Daily** | 24 hours | Base price | Retail analytics, reporting |
            | **Weekly/Monthly** | 7-30 days | 0.5x base | Trend analysis, research |
            
            *Note: Real-time requires streaming infrastructure (Kafka/Kinesis) vs. batch*
            """)
        
        with st.container(border=True):
            st.markdown("**📅 History — Temporal Depth**")
            st.markdown("""
            How far back historical data extends. Deeper history enables trend analysis:
            
            | Tier | Retention | Use Case |
            |------|-----------|----------|
            | **30 days rolling** | Recent window only | Operational dashboards |
            | **1 year archive** | Full year lookback | YoY comparisons, seasonality |
            | **3+ years deep** | Multi-year archive | Long-term planning, ML training |
            | **Custom range** | Specific periods | Event analysis, audits |
            
            *Storage costs increase with history depth; consider tiered storage (hot/cold)*
            """)
    
    st.info("""
    💡 **Pricing Strategy Tip**: Most data products use a **matrix pricing model** combining 2-3 dimensions. 
    For example: *"National coverage + Daily freshness + 1 year history"* as a standard tier, 
    with upcharges for real-time access or regional expansion.
    """)

# =============================================================================
# TAB 5: DATA DISTRIBUTION
# =============================================================================
with tab_distribution:
    st.html("""
    <div class="section-header">
        <h3>🌐 Reaching Consumers Without a Snowflake Account</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    st.markdown("""
    All options use **Snowflake as BICS's platform** but abstract it from the end consumer. 
    Here's the menu of distribution options with the specific Snowflake features that enable each:
    """)
    
    # Option 1: Reader Accounts
    with st.container(border=True):
        col_icon, col_content = st.columns([1, 11])
        with col_icon:
            st.html("""<div class="distribution-icon">👤</div>""")
        with col_content:
            st.markdown("### Reader-Style Access")
            st.markdown("""
            BICS hosts the data in Snowflake and provisions governed, read-only endpoints for 
            agencies or enterprises. The consumer doesn't need their own Snowflake contract; 
            BICS controls the account, roles, policies, and pays for compute.
            """)
        
        st.html("""<div class="distribution-tag">Best for: Government entities who want dashboards/SQL</div>""")
        
        st.markdown("**Snowflake Features:**")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            - **Reader Accounts** — Managed accounts BICS creates for consumers; no separate Snowflake contract needed
            - **Resource Monitors** — Set compute budgets per consumer to control costs
            - **Network Policies** — Restrict access by IP range for security
            """)
        with col2:
            st.markdown("""
            - **Role-Based Access Control (RBAC)** — Fine-grained permissions per user/group
            - **Object Tagging** — Classify data sensitivity for governance
            - **Query History & Access History** — Full audit trail of who accessed what
            """)
    
    # Option 2: Streamlit Apps / Portals
    with st.container(border=True):
        col_icon, col_content = st.columns([1, 11])
        with col_icon:
            st.html("""<div class="distribution-icon">📱</div>""")
        with col_content:
            st.markdown("### \"Powered-by BICS\" Applications & Portals")
            st.markdown("""
            Build web or mobile apps (e.g., city operations dashboard, tourism insights portal, 
            government analytics cockpit) where Snowflake is the backend and the user only sees 
            BICS's UI. For Belgium, this could be a "BICS Data Exchange Portal" with SSO.
            """)
        
        st.html("""<div class="distribution-tag">Best for: Business users and ministries</div>""")
        
        st.markdown("**Snowflake Features:**")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            - **Streamlit in Snowflake** — Build and host Python apps directly in Snowflake; no external infra needed
            - **Snowflake Native Apps** — Package apps + data as installable products consumers run in their account
            - **Snowsight Dashboards** — No-code dashboards with filters, charts, and sharing
            """)
        with col2:
            st.markdown("""
            - **OAuth / SAML SSO** — Integrate with ministry identity providers (Azure AD, Okta, etc.)
            - **Row Access Policies** — Each ministry sees only their entitled data automatically
            - **Secure Views** — Expose curated datasets without revealing underlying tables
            """)
    
    # Option 3: APIs
    with st.container(border=True):
        col_icon, col_content = st.columns([1, 11])
        with col_icon:
            st.html("""<div class="distribution-icon">🔌</div>""")
        with col_content:
            st.markdown("### APIs and Services on Top of Snowflake")
            st.markdown("""
            Expose REST/GraphQL APIs for queries like "give me today's footfall by district" or 
            "score this list of locations", implemented via services that query Snowflake. 
            API usage (pay-per-call) is a core revenue stream.
            """)
        
        st.html("""<div class="distribution-tag">Best for: Developers and system integrations</div>""")
        
        st.markdown("**Snowflake Features:**")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            - **Snowflake REST API** — Native SQL API for programmatic access with OAuth/key-pair auth
            - **Snowpark Container Services** — Deploy custom API containers (FastAPI, Flask) inside Snowflake
            - **External Functions** — Call external ML models or services from SQL
            """)
        with col2:
            st.markdown("""
            - **Snowflake Connector for Python/Java/.NET** — Native drivers for any backend
            - **Usage Metering** — Track API calls per consumer for billing
            - **Warehouse Auto-Suspend/Resume** — Pay only when queries run
            """)
    
    # Option 4: Clean Rooms
    with st.container(border=True):
        col_icon, col_content = st.columns([1, 11])
        with col_icon:
            st.html("""<div class="distribution-icon">🔒</div>""")
        with col_content:
            st.markdown("### Clean Rooms for Joint Analysis")
            st.markdown("""
            Use Snowflake Clean Rooms so government agencies can run approved queries that join 
            their data with BICS's, without ever exchanging raw PII. Access can be via their 
            tools or a simple front-end; governed products with row/masking policies attached.
            """)
        
        st.html("""<div class="distribution-tag">Best for: Privacy-sensitive joint analytics</div>""")
        
        st.markdown("**Snowflake Features:**")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            - **Snowflake Data Clean Rooms** — Pre-built templates for secure overlap analysis, attribution, lookalikes
            - **Secure Data Sharing** — Share live data without copying; consumer queries BICS's tables in-place
            - **Differential Privacy** — Add statistical noise to prevent re-identification
            """)
        with col2:
            st.markdown("""
            - **Dynamic Data Masking** — Mask PII columns based on consumer role (e.g., show city but hide exact lat/lon)
            - **Aggregation Policies** — Enforce minimum group sizes (e.g., no results with <100 people)
            - **Projection Policies** — Control which columns each consumer can select
            """)
    
    # Option 5: File Exports
    with st.container(border=True):
        col_icon, col_content = st.columns([1, 11])
        with col_icon:
            st.html("""<div class="distribution-icon">📁</div>""")
        with col_content:
            st.markdown("### Files / Object-Store Exports")
            st.markdown("""
            If a specific agency can only consume files (CSV/Parquet in S3/Blob), BICS can 
            schedule governed exports from Snowflake. This is the least powerful option 
            (no live data, harder to govern/audit).
            """)
        
        st.html("""<div class="distribution-tag warning">Fallback option — limited governance</div>""")
        
        st.markdown("**Snowflake Features:**")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            - **COPY INTO (Unload)** — Export query results to S3, Azure Blob, or GCS in CSV/Parquet/JSON
            - **Tasks & Streams** — Schedule automated exports on data changes or time intervals
            - **External Stages** — Managed connection to cloud storage with encryption
            """)
        with col2:
            st.markdown("""
            - **Storage Integration** — Secure, credential-free access to cloud buckets
            - **Data Retention Policies** — Auto-delete old exports after N days
            - **File Format Options** — Compression (gzip, snappy), partitioning, headers
            """)
    
    st.html("""
    <div class="section-header">
        <h3>📋 Distribution Method Comparison</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    comparison_data = pd.DataFrame({
        'Method': ['Reader Accounts', 'Streamlit / Native Apps', 'REST APIs', 'Clean Rooms', 'File Exports'],
        'Snowflake Feature': ['Reader Accounts + RBAC', 'Streamlit in Snowflake', 'Snowpark Container Services', 'Data Clean Rooms', 'COPY INTO + Tasks'],
        'Consumer Needs': ['Browser only', 'Browser + SSO', 'Developer skills', 'Analyst skills', 'File handling'],
        'Live Data': ['✓', '✓', '✓', '✓', '✗'],
        'Governance': ['High', 'High', 'High', 'Very High', 'Low'],
        'Best For': ['Govt dashboards', 'Ministry portals', 'System integration', 'Joint analytics', 'Legacy systems']
    })
    
    with st.container(border=True):
        st.dataframe(
            comparison_data,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Method": st.column_config.TextColumn("Distribution Method", width="medium"),
                "Snowflake Feature": st.column_config.TextColumn("Key Snowflake Feature", width="large"),
                "Consumer Needs": st.column_config.TextColumn("Consumer Needs"),
                "Live Data": st.column_config.TextColumn("Live"),
                "Governance": st.column_config.TextColumn("Governance"),
                "Best For": st.column_config.TextColumn("Best For", width="medium")
            }
        )
    
    st.html("""
    <div class="section-header">
        <h3>🏗️ Snowflake Governance Stack</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    st.markdown("These governance features apply across **all** distribution methods:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container(border=True):
            st.markdown("**🔐 Access Control**")
            st.caption("• Role-Based Access Control (RBAC)")
            st.caption("• Row Access Policies")
            st.caption("• Column-Level Security")
            st.caption("• Network Policies (IP allowlists)")
            st.caption("• Multi-Factor Authentication")
    
    with col2:
        with st.container(border=True):
            st.markdown("**🛡️ Data Protection**")
            st.caption("• Dynamic Data Masking")
            st.caption("• Aggregation Policies")
            st.caption("• Projection Policies")
            st.caption("• Secure Views")
            st.caption("• End-to-End Encryption")
    
    with col3:
        with st.container(border=True):
            st.markdown("**📊 Audit & Compliance**")
            st.caption("• Query History (90 days)")
            st.caption("• Access History")
            st.caption("• Object Tagging & Classification")
            st.caption("• Data Lineage (Horizon)")
            st.caption("• SOC 2 / ISO 27001 / GDPR")
    
    st.html("""
    <div class="key-insight">
        <p>💡 <strong>Recommendation:</strong> For maximum reach, combine <strong>Streamlit Apps</strong> 
        (for government self-service), <strong>Snowpark Container Services APIs</strong> (for developer integrations), and 
        <strong>Clean Rooms</strong> (for privacy-sensitive joint analytics with ministries). 
        This covers 90%+ of potential Belgian and EU customer segments while maintaining full data governance.</p>
    </div>
    """)
    
    st.html("""
    <div class="position-box">
        <p><strong>For Belgian/EU Government:</strong> Position as a "BICS Data Exchange Portal" built with 
        <strong>Streamlit in Snowflake</strong>, integrated with ministry SSO via <strong>SAML/OAuth</strong>, 
        where each ministry only sees entitled data via <strong>Row Access Policies</strong>. 
        Snowflake stays invisible; BICS delivers governed insights through a trusted, branded experience.</p>
    </div>
    """)

# =============================================================================
# TAB 6: REFERENCES
# =============================================================================
with tab_references:
    st.html("""
    <div class="section-header">
        <h3>📚 Industry References & Case Studies</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    st.markdown("""
    Below are examples of how telcos and satellite operators are monetizing their data through 
    marketplace datasets. These serve as reference models for BICS's data product strategy.
    """)
    
    st.html("""
    <style>
        .featured-card {
            background: linear-gradient(135deg, #1E3A5F 0%, #0891B2 100%);
            border-radius: 20px;
            padding: 2rem;
            margin: 1.5rem 0;
            color: white;
            position: relative;
            overflow: hidden;
            animation: fadeInUp 0.6s ease-out;
            box-shadow: 0 10px 40px rgba(30, 58, 95, 0.3);
        }
        .featured-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
            pointer-events: none;
        }
        .featured-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            background: linear-gradient(135deg, #D4AF37, #F59E0B);
            color: #1E3A5F;
            padding: 0.4rem 1rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 700;
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .featured-card h4 {
            color: white;
            margin: 0 0 0.75rem 0;
            font-size: 1.4rem;
            font-weight: 700;
            position: relative;
            z-index: 1;
        }
        .featured-card p {
            color: rgba(255, 255, 255, 0.9);
            margin: 0;
            line-height: 1.7;
            position: relative;
            z-index: 1;
        }
        .featured-card ul {
            color: rgba(255, 255, 255, 0.9);
            margin-top: 1rem;
            line-height: 1.9;
            position: relative;
            z-index: 1;
        }
        .featured-card li strong {
            color: #D4AF37;
        }
        .featured-stats {
            display: flex;
            gap: 1.5rem;
            margin-top: 1.5rem;
            flex-wrap: wrap;
            position: relative;
            z-index: 1;
        }
        .featured-stat {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            padding: 1rem 1.5rem;
            border-radius: 12px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .featured-stat-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: #D4AF37;
        }
        .featured-stat-label {
            font-size: 0.8rem;
            color: rgba(255, 255, 255, 0.8);
            margin-top: 0.25rem;
        }
        .featured-link {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: white;
            color: #1E3A5F;
            padding: 0.75rem 1.5rem;
            border-radius: 10px;
            font-weight: 600;
            text-decoration: none;
            margin-top: 1.5rem;
            transition: all 0.3s ease;
            position: relative;
            z-index: 1;
        }
        .featured-link:hover {
            background: #D4AF37;
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        .reference-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
            animation: fadeInUp 0.6s ease-out;
        }
        .reference-card h4 {
            color: #1E3A5F;
            margin: 0 0 0.5rem 0;
            font-size: 1.1rem;
        }
        .reference-card p {
            color: #64748b;
            margin: 0;
            line-height: 1.6;
        }
        .reference-image-container {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 1rem;
            margin: 1.5rem 0;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            animation: fadeInUp 0.6s ease-out 0.2s backwards;
        }
        .reference-caption {
            text-align: center;
            color: #64748b;
            font-size: 0.85rem;
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid #e2e8f0;
        }
    </style>
    """)
    
    # FEATURED: BT Active Intelligence
    st.html("""
    <div class="featured-card">
        <div class="featured-badge">⭐ Featured Reference</div>
        <h4>🇬🇧 BT Active Intelligence - Snowflake Marketplace</h4>
        <p>
            <strong>BT Active Intelligence</strong> (UK) is a leading example of how a major telco monetizes 
            mobility data through the Snowflake Marketplace. They offer 4 distinct data products serving 
            transportation, geospatial, and media sectors — directly relevant to BICS's strategy.
        </p>
        <div class="featured-stats">
            <div class="featured-stat">
                <div class="featured-stat-value">24M</div>
                <div class="featured-stat-label">Mobile Devices</div>
            </div>
            <div class="featured-stat">
                <div class="featured-stat-value">25B</div>
                <div class="featured-stat-label">Daily Events</div>
            </div>
            <div class="featured-stat">
                <div class="featured-stat-value">1/3</div>
                <div class="featured-stat-label">UK Adult Population</div>
            </div>
            <div class="featured-stat">
                <div class="featured-stat-value">4</div>
                <div class="featured-stat-label">Data Products</div>
            </div>
        </div>
        <ul>
            <li><strong>Road Insights:</strong> Traffic flow and speed along specific road networks</li>
            <li><strong>Location Insights:</strong> Footfall data to optimize business strategies</li>
            <li><strong>On Demand Journeys:</strong> Origin-destination insights at LSOA level</li>
            <li><strong>Audience Insights:</strong> Geo personas for campaign planning</li>
        </ul>
        <a href="https://business.bt.com/iot/active-intelligence/" target="_blank" class="featured-link">
            🔗 Visit BT Active Intelligence
        </a>
        <a href="https://app.snowflake.com/marketplace/providers/GZ2FRZE33RP/BT%20Active%20Intelligence?search=BT" target="_blank" class="featured-link" style="margin-left: 10px;">
            🏪 Visit Marketplace
        </a>
    </div>
    """)
    
    # Note: Images from local files not supported in Streamlit in Snowflake
    # Reference: bt_active_intelligence_reference.png
    
    st.html("""
    <div class="reference-caption">
        <strong>Source:</strong> BT Active Intelligence on Snowflake Marketplace — 
        <a href="https://business.bt.com/iot/active-intelligence/" target="_blank" style="color: #0891B2;">business.bt.com/iot/active-intelligence</a>
    </div>
    """)
    
    st.html("""
    <div class="key-insight">
        <p>💡 <strong>Why BT Matters for BICS:</strong> BT's "Active Intelligence" is the closest 
        comparable to BICS's vision — a major telco selling <strong>anonymized mobility insights</strong> 
        through a marketplace with "Free to try" options. Their product catalog (Road, Location, Journeys, 
        Audience) maps directly to what BICS can offer Belgian government and enterprise clients.</p>
    </div>
    """)
    
    st.divider()
    
    st.html("""
    <div class="section-header">
        <h3>📊 Additional Industry Case Studies</h3>
        <div class="section-line"></div>
    </div>
    """)
    
    st.html("""
    <div class="reference-card">
        <h4>🌐 Telia & OneWeb - Snowflake Marketplace Case Study</h4>
        <p>
            This reference from Snowflake showcases how <strong>Telia</strong> (Nordic telco) and 
            <strong>OneWeb/Eutelsat</strong> (satellite operator) are using the Snowflake Marketplace 
            to distribute crowd insights and satellite operations data to partners. Key takeaways:
        </p>
        <ul style="color: #64748b; margin-top: 0.75rem; line-height: 1.8;">
            <li><strong>Telia:</strong> Mobile crowd insights for real estate planning & retail optimization</li>
            <li><strong>Revenue Model:</strong> Free sample datasets → Platform access → Enhanced data at cost</li>
            <li><strong>OneWeb:</strong> Satellite fleet data for coverage analysis & outage prevention</li>
            <li><strong>Partner Strategy:</strong> Free sharing with mutual benefit, leading to new contracts</li>
        </ul>
    </div>
    """)
    
    # Note: Images from local files not supported in Streamlit in Snowflake
    # Reference: telia_oneweb_reference.png
    
    st.html("""
    <div class="reference-caption">
        <strong>Source:</strong> Snowflake Inc. © 2025 — Telia & OneWeb Marketplace Datasets for Crowd Insights & Partner Operations
    </div>
    """)
    
    st.html("""
    <div class="key-insight">
        <p>💡 <strong>Relevance to BICS:</strong> Telia's approach of offering mobile crowd insights 
        for real estate and retail planning directly parallels BICS's mobility data product strategy. 
        The "free sample → platform → premium" revenue model is a proven pattern that BICS can adapt 
        for the Belgian and EU market, especially for government and giga-project clients.</p>
    </div>
    """)
    
    st.divider()
    
    # T-Mobile Reference
    st.html("""
    <div class="reference-card">
        <h4>📱 T-Mobile: Magenta Advertising Platform</h4>
        <p>
            T-Mobile's <strong>Magenta Advertising Platform</strong> demonstrates how telcos can monetize 
            subscriber data for advertising while generating significant new revenue streams.
        </p>
        <ul style="color: #64748b; margin-top: 0.75rem; line-height: 1.8;">
            <li><strong>Scale:</strong> 240M subscribers reach for targeted advertising</li>
            <li><strong>Revenue:</strong> $80M in new organic advertising revenue</li>
            <li><strong>ROI:</strong> 40X realized return on $2M Snowflake investment</li>
            <li><strong>Capabilities:</strong> Campaign planning, prediction, self-service reporting</li>
            <li><strong>Evolution:</strong> From insights → reporting → secure sharing → advanced AI</li>
        </ul>
    </div>
    """)
    
    # Note: Images from local files not supported in Streamlit in Snowflake
    # Reference: tmobile_magenta_reference.png
    
    st.html("""
    <div class="reference-caption">
        <strong>Source:</strong> Snowflake Inc. © 2025 — T-Mobile Magenta Advertising Platform powered by Snowflake & Pushspring
    </div>
    """)
    
    st.divider()
    
    # AT&T/DirecTV Reference
    st.html("""
    <div class="reference-card">
        <h4>📺 AT&T/DirecTV: Secure Data Monetization with Clean Rooms</h4>
        <p>
            AT&T and DirecTV showcase how <strong>Data Clean Rooms</strong> enable secure data monetization 
            for advertising across live and VoD content while maintaining privacy compliance.
        </p>
        <ul style="color: #64748b; margin-top: 0.75rem; line-height: 1.8;">
            <li><strong>Focus:</strong> Advanced streaming solutions & insight-based advertising</li>
            <li><strong>Capabilities:</strong> Contextual & targeted audience advertising, subscriber insights</li>
            <li><strong>Clean Rooms:</strong> Secure data sharing with guaranteed incremental reach</li>
            <li><strong>Results:</strong> +86% brand awareness, +51% ad awareness for auto campaigns</li>
            <li><strong>Revenue Model:</strong> Fee-based targeted ads, live events, VoD, digital signage</li>
        </ul>
    </div>
    """)
    
    # Note: Images from local files not supported in Streamlit in Snowflake
    # Reference: att_directv_reference.png
    
    st.html("""
    <div class="reference-caption">
        <strong>Source:</strong> Snowflake Inc. © 2025 — AT&T/DirecTV Secure Data Monetization with Data Clean Rooms
    </div>
    """)
    
    st.divider()
    
    # AT&T + CARTO Reference
    st.html("""
    <div class="reference-card">
        <h4>🗺️ AT&T + CARTO: Geospatial Data & App Innovation</h4>
        <p>
            AT&T's partnership with <strong>CARTO</strong> demonstrates how telcos can combine event analytics 
            with geospatial enrichment to create high-value data products for multiple industries.
        </p>
        <ul style="color: #64748b; margin-top: 0.75rem; line-height: 1.8;">
            <li><strong>AT&T Data Patterns:</strong> Event insights, subscriber insights, geospatial enrichment</li>
            <li><strong>CARTO Use Cases:</strong> Marketing, fraud detection, IoT density planning</li>
            <li><strong>Applications:</strong> Disaster impact modeling, digital twin enrichment</li>
            <li><strong>Visualization:</strong> Advanced geospatial dashboards and heatmaps</li>
        </ul>
    </div>
    """)
    
    # Note: Images from local files not supported in Streamlit in Snowflake
    # Reference: att_carto_reference.png
    
    st.html("""
    <div class="reference-caption">
        <strong>Source:</strong> Snowflake Inc. © 2023 — AT&T & CARTO Geospatial Data Innovation
    </div>
    """)
    
    st.divider()
    
    # NTT Docomo Reference
    st.html("""
    <div class="reference-card">
        <h4>🇯🇵 NTT Docomo & aiQ: AI-Powered Data Products</h4>
        <p>
            Japan's <strong>NTT Docomo</strong> partnered with <strong>aiQ</strong> to create AI-powered 
            data products serving operators and enterprise companies with geolocation and consumer insights.
        </p>
        <ul style="color: #64748b; margin-top: 0.75rem; line-height: 1.8;">
            <li><strong>Scale:</strong> 80M+ mobile phones covered across Japan</li>
            <li><strong>Geolocation Products:</strong> Tokyo Stock Exchange company foot traffic analysis</li>
            <li><strong>REIT Analytics:</strong> Real estate location insights for 79+ Japanese REITs</li>
            <li><strong>Consumer Data:</strong> 50K+ monthly respondents tracking purchases across retailers</li>
            <li><strong>Revenue Model:</strong> Datasets at cost + free sample datasets available</li>
        </ul>
    </div>
    """)
    
    # Note: Images from local files not supported in Streamlit in Snowflake
    # Reference: ntt_docomo_reference.png
    
    st.html("""
    <div class="reference-caption">
        <strong>Source:</strong> Snowflake Inc. © 2025 — NTT Docomo & aiQ AI-Powered Data Collaboration
    </div>
    """)
    
    st.html("""
    <div class="key-insight" style="margin-top: 2rem;">
        <p>💡 <strong>Key Takeaway for BICS:</strong> These global telco examples demonstrate proven patterns: 
        <strong>T-Mobile</strong> shows advertising monetization at scale, <strong>AT&T</strong> proves clean rooms 
        enable privacy-safe partnerships, <strong>CARTO</strong> illustrates geospatial value creation, and 
        <strong>NTT Docomo</strong> validates the AI + mobility data combination. BICS can adapt these models 
        for the Belgian and EU market, particularly for smart city initiatives and IoT industry verticals.</p>
    </div>
    """)
