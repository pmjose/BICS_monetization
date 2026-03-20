import streamlit as st
from snowflake.snowpark.context import get_active_session
from utils.styles import render_common_styles, render_page_header

st.set_page_config(page_title="Data Export | BICS", page_icon=":material/download:", layout="wide")

st.logo("logo.png")
render_common_styles()
render_page_header("Data Export", "Select and download mobility data packages")

EXPORT_PRESETS = {
    "Custom Selection": {},
    "Quick: Brussels Full": {"cities": ["Brussels"]},
    "Quick: Flemish Cities": {"cities": ["Antwerp", "Ghent", "Bruges", "Mechelen", "Leuven"]},
    "Quick: Tourist Demographics": {"nationalities": ["French", "Dutch", "German", "Italian"]},
}

@st.cache_data(ttl=600)
def get_filter_options():
    session = get_active_session()
    cities = session.sql("SELECT DISTINCT SUBSCRIBER_HOME_CITY FROM BICS_TELCO.MOBILITY_DATA.BICS_TELCO_MOBILITY_DATA ORDER BY 1").to_pandas()
    nationalities = session.sql("SELECT DISTINCT NATIONALITY FROM BICS_TELCO.MOBILITY_DATA.BICS_TELCO_MOBILITY_DATA ORDER BY 1").to_pandas()
    age_groups = session.sql("SELECT DISTINCT AGE_GROUP FROM BICS_TELCO.MOBILITY_DATA.BICS_TELCO_MOBILITY_DATA ORDER BY 1").to_pandas()
    dates = session.sql("SELECT MIN(DATE) as MIN_DATE, MAX(DATE) as MAX_DATE FROM BICS_TELCO.MOBILITY_DATA.BICS_TELCO_MOBILITY_DATA").to_pandas()
    return cities, nationalities, age_groups, dates

@st.cache_data(ttl=300)
def get_record_count(cities, nationalities, age_groups, genders, sub_types, date_range):
    session = get_active_session()
    
    where_clauses = []
    if cities:
        city_list = "','".join(cities)
        where_clauses.append(f"SUBSCRIBER_HOME_CITY IN ('{city_list}')")
    if nationalities:
        nat_list = "','".join(nationalities)
        where_clauses.append(f"NATIONALITY IN ('{nat_list}')")
    if age_groups:
        age_list = "','".join(age_groups)
        where_clauses.append(f"AGE_GROUP IN ('{age_list}')")
    if genders:
        gender_list = "','".join(genders)
        where_clauses.append(f"GENDER IN ('{gender_list}')")
    if sub_types:
        sub_list = "','".join(sub_types)
        where_clauses.append(f"SUBSCRIPTION_TYPE IN ('{sub_list}')")
    if date_range:
        where_clauses.append(f"DATE BETWEEN '{date_range[0]}' AND '{date_range[1]}'")
    
    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
    
    query = f"""
        SELECT COUNT(*) as cnt FROM BICS_TELCO.MOBILITY_DATA.BICS_TELCO_MOBILITY_DATA
        WHERE {where_sql}
    """
    return session.sql(query).to_pandas()['CNT'].iloc[0]

@st.cache_data(ttl=300)
def get_sample_data(cities, nationalities, age_groups, genders, sub_types, date_range, limit=100):
    session = get_active_session()
    
    where_clauses = []
    if cities:
        city_list = "','".join(cities)
        where_clauses.append(f"SUBSCRIBER_HOME_CITY IN ('{city_list}')")
    if nationalities:
        nat_list = "','".join(nationalities)
        where_clauses.append(f"NATIONALITY IN ('{nat_list}')")
    if age_groups:
        age_list = "','".join(age_groups)
        where_clauses.append(f"AGE_GROUP IN ('{age_list}')")
    if genders:
        gender_list = "','".join(genders)
        where_clauses.append(f"GENDER IN ('{gender_list}')")
    if sub_types:
        sub_list = "','".join(sub_types)
        where_clauses.append(f"SUBSCRIPTION_TYPE IN ('{sub_list}')")
    if date_range:
        where_clauses.append(f"DATE BETWEEN '{date_range[0]}' AND '{date_range[1]}'")
    
    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
    
    query = f"""
        SELECT * FROM BICS_TELCO.MOBILITY_DATA.BICS_TELCO_MOBILITY_DATA
        WHERE {where_sql}
        LIMIT {limit}
    """
    return session.sql(query).to_pandas()

@st.cache_data(ttl=60, show_spinner=False)
def get_export_data(cities, nationalities, age_groups, genders, sub_types, date_range, limit=100000):
    session = get_active_session()
    
    where_clauses = []
    if cities:
        city_list = "','".join(cities)
        where_clauses.append(f"SUBSCRIBER_HOME_CITY IN ('{city_list}')")
    if nationalities:
        nat_list = "','".join(nationalities)
        where_clauses.append(f"NATIONALITY IN ('{nat_list}')")
    if age_groups:
        age_list = "','".join(age_groups)
        where_clauses.append(f"AGE_GROUP IN ('{age_list}')")
    if genders:
        gender_list = "','".join(genders)
        where_clauses.append(f"GENDER IN ('{gender_list}')")
    if sub_types:
        sub_list = "','".join(sub_types)
        where_clauses.append(f"SUBSCRIPTION_TYPE IN ('{sub_list}')")
    if date_range:
        where_clauses.append(f"DATE BETWEEN '{date_range[0]}' AND '{date_range[1]}'")
    
    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
    
    query = f"""
        SELECT * FROM BICS_TELCO.MOBILITY_DATA.BICS_TELCO_MOBILITY_DATA
        WHERE {where_sql}
        LIMIT {limit}
    """
    return session.sql(query).to_pandas()

cities_df, nationalities_df, age_groups_df, dates_df = get_filter_options()
min_date = dates_df['MIN_DATE'].iloc[0]
max_date = dates_df['MAX_DATE'].iloc[0]

with st.sidebar:
    st.subheader(":material/bookmark: Quick Presets", anchor=False)
    selected_preset = st.selectbox(
        "Load preset",
        options=list(EXPORT_PRESETS.keys()),
        index=0,
        help="Quick filter presets for common exports"
    )
    preset = EXPORT_PRESETS[selected_preset]

st.subheader(":material/tune: Configure Data Package", anchor=False)

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("**:material/location_on: Geographic & Temporal**")
        
        selected_cities = st.multiselect(
            "Cities",
            options=cities_df['SUBSCRIBER_HOME_CITY'].tolist(),
            default=preset.get("cities", []),
            help="Leave empty for all cities"
        )
        
        date_range = st.date_input(
            "Date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

with col2:
    with st.container(border=True):
        st.markdown("**:material/person: Demographic Filters**")
        
        selected_nationalities = st.multiselect(
            "Nationalities",
            options=nationalities_df['NATIONALITY'].tolist(),
            default=preset.get("nationalities", []),
            help="Leave empty for all nationalities"
        )
        
        selected_age_groups = st.multiselect(
            "Age groups",
            options=age_groups_df['AGE_GROUP'].tolist(),
            default=preset.get("age_groups", [])
        )
        
        selected_genders = st.multiselect(
            "Gender",
            options=["Male", "Female"],
            default=preset.get("genders", [])
        )
        
        selected_sub_types = st.multiselect(
            "Subscription type",
            options=["Prepaid", "Postpaid"],
            default=preset.get("sub_types", [])
        )

record_count = get_record_count(
    selected_cities, selected_nationalities, selected_age_groups,
    selected_genders, selected_sub_types, date_range
)

def estimate_file_size(row_count, cols=15, avg_bytes_per_cell=12):
    return (row_count * cols * avg_bytes_per_cell) / (1024 * 1024)

st.subheader(":material/summarize: Data Package Summary", anchor=False)

cities_label = ", ".join(selected_cities) if selected_cities else "All Cities"
with st.container(horizontal=True):
    st.metric("Total Records", f"{record_count:,}", border=True)
    st.metric("Coverage", cities_label[:25] + "..." if len(cities_label) > 25 else cities_label, border=True)
    st.metric("Date Range", f"{date_range[0]} to {date_range[1]}", border=True)

st.subheader(":material/preview: Sample Preview", anchor=False)
with st.container(border=True):
    sample_df = get_sample_data(
        selected_cities, selected_nationalities, selected_age_groups,
        selected_genders, selected_sub_types, date_range
    )
    st.dataframe(sample_df, use_container_width=True, height=220, hide_index=True)
    st.caption("Showing first 100 records as preview")

st.subheader(":material/file_download: Export Data", anchor=False)

with st.container(border=True):
    terms_accepted = st.checkbox(
        "I agree to the data usage terms",
        help="This data is for analytical purposes only. Redistribution or resale is prohibited."
    )

    if terms_accepted:
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            export_limit = st.selectbox(
                "Export limit",
                options=[10000, 50000, 100000],
                index=0,
                help="Maximum records per export"
            )
        with col2:
            actual_export = min(export_limit, record_count)
            est_size = estimate_file_size(actual_export)
            st.metric("Est. File Size", f"~{est_size:.1f} MB")
        
        with col3:
            if st.button("Prepare Export", type="primary", icon=":material/download:", use_container_width=True):
                progress_bar = st.progress(0, text="Initializing export...")
                
                progress_bar.progress(10, text="Querying data from Snowflake...")
                export_df = get_export_data(
                    selected_cities, selected_nationalities, selected_age_groups,
                    selected_genders, selected_sub_types, date_range, limit=export_limit
                )
                
                progress_bar.progress(60, text="Converting to CSV format...")
                csv_data = export_df.to_csv(index=False)
                
                progress_bar.progress(90, text="Preparing download...")
                actual_size = len(csv_data.encode('utf-8')) / (1024 * 1024)
                
                progress_bar.progress(100, text="Export ready!")
                
                st.download_button(
                    label=f":material/download: Download CSV ({len(export_df):,} records, {actual_size:.1f} MB)",
                    data=csv_data,
                    file_name="bics_mobility_export.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
                st.success(f"Export ready! {len(export_df):,} records ({actual_size:.1f} MB) prepared.", icon=":material/check_circle:")
    else:
        st.caption(":material/info: Please accept the data usage terms to proceed with export.")

st.html("""
<div style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border: 2px solid #0891B2; border-radius: 12px; padding: 1.5rem; text-align: center; margin-top: 1.5rem;">
    <h3 style="color: #1E3A5F; margin: 0 0 0.5rem 0;">:material/business: Need Full Dataset Access?</h3>
    <p style="color: #64748b; margin: 0;">For enterprise data sharing with unlimited records and real-time access,<br/>
    contact our sales team to set up a Snowflake Data Share or Marketplace listing.</p>
</div>
""")
