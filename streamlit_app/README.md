# BICS - Global Carrier Intelligence Platform

A Streamlit in Snowflake app for monetizing BICS roaming signaling data and IoT connectivity analytics.

## Features

### Mobility Intelligence
- **Data Explorer**: Browse and filter 4.2M+ mobility records
- **Analytics Dashboard**: Sellable insights (traffic trends, demographics, dwell time)
- **Map Visualization**: PyDeck H3 hexagon visualization of foot traffic
- **Data Export**: Self-service data package downloads

### IoT Industry Analytics
- **IoT Analytics Dashboard**: KPIs, device status, telemetry trends, connectivity & SIM breakdown across 5 industries
- **IoT Device Map**: Geographic PyDeck visualization of 1,000+ IoT devices across Belgium, filterable by industry and status

## Data Sources

### Mobility Data
- **Table**: `BICS_TELCO.MOBILITY_DATA.BICS_TELCO_MOBILITY_DATA`
- **Records**: 4,245,000
- **Sources**: BICS global roaming signaling (700+ MNO partners, 200+ countries)
- **Period**: January 2026

### IoT Data
- **Device Registry**: `BICS_TELCO.IOT_DATA.BICS_IOT_DEVICES` (~1,000 devices)
- **Telemetry**: `BICS_TELCO.IOT_DATA.BICS_IOT_TELEMETRY` (~150,000 readings)
- **Industries**: Agriculture, Healthcare, Industrial Manufacturing, Transport & Logistics, OEM
- **Connectivity**: NB-IoT, LTE-M, 4G, 5G
- **SIM Types**: eSIM (50%), Traditional SIM (35%), iSIM (15%)
- **Period**: January 2026

#### IoT Industry Details

| Industry | Devices | Device Types | Key Sites |
|----------|---------|-------------|-----------|
| Agriculture | 180 | Soil Sensor, Weather Station, GPS Tractor, Irrigation, Greenhouse, Livestock | West Flanders, Limburg, Wallonia |
| Healthcare | 200 | Patient Monitor, Asset Tag, Cold Chain, Infusion Pump, Environmental | UZ Brussel, UZA, UZ Ghent, UZ Leuven |
| Industrial Manufacturing | 200 | Vibration Sensor, Pressure Gauge, Power Meter, CNC Monitor, Conveyor | Port of Antwerp, Charleroi, Ghent |
| Transport & Logistics | 220 | Fleet GPS, Container Sensor, Cold Chain, Fuel Sensor, Trailer, Drone | Port of Antwerp, Brussels Airport, Liege Airport |
| OEM | 200 | Smart Meter, Connected Vehicle, Gateway, Wearable, Smart Display, Edge | Brussels, Antwerp, Ghent, imec Leuven |

## Deployment to Snowflake

### 1. Create Database, Schemas & Stage

```sql
CREATE DATABASE IF NOT EXISTS BICS_TELCO;
CREATE SCHEMA IF NOT EXISTS BICS_TELCO.MOBILITY_DATA;
CREATE SCHEMA IF NOT EXISTS BICS_TELCO.IOT_DATA;

CREATE STAGE IF NOT EXISTS BICS_TELCO.MOBILITY_DATA.BICS_STREAMLIT_STAGE
  DIRECTORY = (ENABLE = TRUE);
```

### 2. Load IoT Data

```sql
-- Create tables
CREATE OR REPLACE TABLE BICS_TELCO.IOT_DATA.BICS_IOT_DEVICES (
    DEVICE_ID VARCHAR, INDUSTRY VARCHAR, DEVICE_TYPE VARCHAR,
    CONNECTIVITY_TYPE VARCHAR, SIM_TYPE VARCHAR, COUNTRY VARCHAR,
    CITY VARCHAR, SITE_NAME VARCHAR, LATITUDE FLOAT, LONGITUDE FLOAT
);

CREATE OR REPLACE TABLE BICS_TELCO.IOT_DATA.BICS_IOT_TELEMETRY (
    DEVICE_ID VARCHAR, INDUSTRY VARCHAR, DEVICE_TYPE VARCHAR,
    CONNECTIVITY_TYPE VARCHAR, SIM_TYPE VARCHAR, COUNTRY VARCHAR,
    CITY VARCHAR, SITE_NAME VARCHAR, LATITUDE FLOAT, LONGITUDE FLOAT,
    TIMESTAMP TIMESTAMP, DATE DATE, HOUR INT,
    METRIC_NAME VARCHAR, METRIC_VALUE FLOAT, METRIC_UNIT VARCHAR,
    SIGNAL_STRENGTH_DBM INT, DATA_USAGE_KB FLOAT, BATTERY_LEVEL_PCT FLOAT,
    DEVICE_STATUS VARCHAR, ALERT_FLAG BOOLEAN
);

-- Load from CSVs (after PUT to stage)
```

### 3. Upload Files

```sql
PUT file:///path/to/streamlit_app/streamlit_app.py @BICS_TELCO.MOBILITY_DATA.BICS_STREAMLIT_STAGE OVERWRITE=TRUE AUTO_COMPRESS=FALSE;
PUT file:///path/to/streamlit_app/environment.yml @BICS_TELCO.MOBILITY_DATA.BICS_STREAMLIT_STAGE OVERWRITE=TRUE AUTO_COMPRESS=FALSE;
PUT file:///path/to/streamlit_app/pages/*.py @BICS_TELCO.MOBILITY_DATA.BICS_STREAMLIT_STAGE/pages/ OVERWRITE=TRUE AUTO_COMPRESS=FALSE;
```

### 4. Create Streamlit App

```sql
CREATE OR REPLACE STREAMLIT BICS_TELCO.MOBILITY_DATA.BICS_APP
  ROOT_LOCATION = '@BICS_TELCO.MOBILITY_DATA.BICS_STREAMLIT_STAGE'
  MAIN_FILE = 'streamlit_app.py'
  QUERY_WAREHOUSE = 'COMPUTE_WH';
```

### 5. Grant Access

```sql
GRANT USAGE ON STREAMLIT BICS_TELCO.MOBILITY_DATA.BICS_APP TO ROLE <role_name>;
```

## File Structure

```
streamlit_app/
├── streamlit_app.py              # Main entry point + data product catalog
├── pages/
│   ├── 0_Market_Intelligence.py  # Market strategy and pricing
│   ├── 1_Data_Explorer.py        # Data browsing and filtering
│   ├── 2_Analytics_Dashboard.py  # Mobility charts and insights
│   ├── 3_Map_Visualization.py    # H3 hexagon maps
│   ├── 4_Data_Export.py          # Data export/purchase
│   ├── 5_IoT_Analytics.py        # IoT industry analytics dashboard
│   └── 6_IoT_Device_Map.py       # IoT device geographic map
├── utils/
│   ├── __init__.py
│   └── styles.py                 # Shared BICS styles and components
├── environment.yml               # Snowflake dependencies
└── logo.jpg
```

## Target Users

- **Retail & Commercial**: Site selection, foot traffic analysis
- **Government & Urban Planning**: Infrastructure, smart city initiatives
- **Tourism & Hospitality**: Visitor flows, destination analytics
- **Transportation**: Commuter patterns, route optimization
- **Agriculture**: Precision farming, crop monitoring, livestock management
- **Healthcare**: Patient monitoring, hospital asset utilization, cold chain
- **Manufacturing**: Predictive maintenance, energy optimization, OEE
- **Logistics**: Fleet management, container tracking, supply chain visibility
- **OEM**: Connected device lifecycle, embedded connectivity analytics
