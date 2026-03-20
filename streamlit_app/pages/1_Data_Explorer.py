import streamlit as st
from snowflake.snowpark.context import get_active_session
from utils.styles import render_common_styles, render_page_header

st.set_page_config(page_title="Data Explorer | BICS", page_icon=":material/search:", layout="wide")

st.logo("logo.png")
render_common_styles()
render_page_header("Data Explorer", "Browse and filter Belgian telco mobility data")

FILTER_PRESETS = {
    "All Data": {},
    "Brussels Peak Hours": {"cities": ["Brussels"], "hour_range": (16, 20)},
    "Antwerp Weekday": {"cities": ["Antwerp"], "hour_range": (8, 18)},
    "Tourist Demographics": {"nationalities": ["French", "Dutch", "German", "Italian"]},
    "Young Adults": {"age_groups": ["18-24", "25-34"]},
    "Flemish Cities": {"cities": ["Antwerp", "Ghent", "Bruges", "Mechelen", "Leuven"]},
}

@st.cache_data(ttl=600)
def get_filter_options():
    session = get_active_session()
    cities = session.sql("SELECT DISTINCT SUBSCRIBER_HOME_CITY FROM BICS_TELCO.MOBILITY_DATA.BICS_TELCO_MOBILITY_DATA ORDER BY 1").to_pandas()
    nationalities = session.sql("SELECT DISTINCT NATIONALITY FROM BICS_TELCO.MOBILITY_DATA.BICS_TELCO_MOBILITY_DATA ORDER BY 1").to_pandas()
    age_groups = session.sql("SELECT DISTINCT AGE_GROUP FROM BICS_TELCO.MOBILITY_DATA.BICS_TELCO_MOBILITY_DATA ORDER BY 1").to_pandas()
    return cities, nationalities, age_groups

@st.cache_data(ttl=300)
def get_filtered_data(cities, nationalities, age_groups, genders, sub_types, hour_range, limit=10000):
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
    
    where_clauses.append(f"HOUR BETWEEN {hour_range[0]} AND {hour_range[1]}")
    
    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
    
    query = f"""
        SELECT * FROM BICS_TELCO.MOBILITY_DATA.BICS_TELCO_MOBILITY_DATA
        WHERE {where_sql}
        LIMIT {limit}
    """
    return session.sql(query).to_pandas()

@st.cache_data(ttl=300)
def get_record_count(cities, nationalities, age_groups, genders, sub_types, hour_range):
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
    
    where_clauses.append(f"HOUR BETWEEN {hour_range[0]} AND {hour_range[1]}")
    
    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
    
    query = f"""
        SELECT COUNT(*) as cnt FROM BICS_TELCO.MOBILITY_DATA.BICS_TELCO_MOBILITY_DATA
        WHERE {where_sql}
    """
    return session.sql(query).to_pandas()['CNT'].iloc[0]

cities_df, nationalities_df, age_groups_df = get_filter_options()

with st.sidebar:
    st.subheader(":material/bookmark: Quick Presets", anchor=False)
    selected_preset = st.selectbox(
        "Load preset",
        options=list(FILTER_PRESETS.keys()),
        index=0,
        help="Select a preset to quickly load common filter combinations"
    )
    
    preset = FILTER_PRESETS[selected_preset]
    
    st.divider()
    st.subheader(":material/filter_list: Custom Filters", anchor=False)
    
    selected_cities = st.multiselect(
        "Cities",
        options=cities_df['SUBSCRIBER_HOME_CITY'].tolist(),
        default=preset.get("cities", [])
    )
    
    selected_nationalities = st.multiselect(
        "Nationalities",
        options=nationalities_df['NATIONALITY'].tolist(),
        default=preset.get("nationalities", [])
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
    
    default_hours = preset.get("hour_range", (0, 23))
    hour_range = st.slider(
        "Hour of day",
        min_value=0,
        max_value=23,
        value=default_hours
    )

record_count = get_record_count(
    selected_cities, selected_nationalities, selected_age_groups,
    selected_genders, selected_sub_types, hour_range
)

col1, col2 = st.columns([3, 1])
with col1:
    st.metric("Matching Records", f"{record_count:,}", border=True)
with col2:
    load_btn = st.button("Load Data", type="primary", icon=":material/download:", use_container_width=True)

if load_btn:
    with st.spinner("Loading data..."):
        df = get_filtered_data(
            selected_cities, selected_nationalities, selected_age_groups,
            selected_genders, selected_sub_types, hour_range
        )
        
        with st.container(border=True):
            st.dataframe(df, use_container_width=True, height=450, hide_index=True)
        
        with st.container(horizontal=True):
            st.metric("Avg Dwell Time", f"{df['AVG_STAYING_DURATION_MIN'].mean():.1f} min", border=True)
            st.metric("Unique Hexagons", f"{df['HEXAGON_ID'].nunique():,}", border=True)
            st.metric("Rows Displayed", f"{len(df):,}", border=True)
else:
    with st.container(border=True):
        st.markdown("""
        ### :material/touch_app: Select filters and click "Load Data"
        
        Use the **Quick Presets** in the sidebar to explore common queries:
        - **Brussels Peak Hours** - Evening traffic in the capital
        - **Tourist Demographics** - Focus on visitor nationalities
        - **Flemish Cities** - Antwerp, Ghent, Bruges, Mechelen, Leuven
        
        Or customize filters and click **Load Data** to explore.
        """)
