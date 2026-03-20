# BICS Roaming & IoT Mobility Dataset

## Overview

This dataset supports **BICS Mobility & IoT Intelligence**, a platform that aggregates anonymized roaming signaling data from BICS's global network of 700+ MNO partners. The data captures international and domestic roaming mobility patterns observed across Belgium through BICS's wholesale carrier infrastructure. BICS is a Proximus Global company headquartered in Brussels, providing global connectivity, IoT, and communications services.

### Use Cases
- **Urban Planning**: Analyze foot traffic and population density across cities
- **Retail & Commercial**: Identify high-traffic areas for site selection
- **Transportation**: Understand commuter patterns and peak travel times
- **Tourism**: Track visitor flows to destinations like Bruges, Ghent, and Brussels
- **Government**: Support smart city initiatives and EU digital strategy planning
- **IoT Analytics**: Monitor connected devices across Agriculture, Healthcare, Manufacturing, Transport, and OEM verticals

### Data Ingestion Context
BICS processes roaming signaling data (anonymized and aggregated) from its global carrier network. This synthetic dataset mimics that ingestion pipeline, split by Belgian region, for demonstration purposes.

## Mobility Data Files

| File | Region | Records | Size |
|------|--------|---------|------|
| `bics_roaming_brussels_capital_jan2026.csv` | Brussels-Capital | 1,415,000 | 92 MB |
| `bics_roaming_flanders_jan2026.csv` | Flanders | 1,415,000 | 92 MB |
| `bics_roaming_wallonia_jan2026.csv` | Wallonia | 1,415,000 | 92 MB |
| **Total** | | **4,245,000** | **276 MB** |

## IoT Data Files

| File | Description | Records |
|------|-------------|---------|
| `bics_iot_devices.csv` | Device registry (5 industries) | ~1,000 |
| `bics_iot_telemetry.csv` | Telemetry readings | ~150,000 |

## Date Range

January 1-31, 2026

## Mobility Schema

| Field | Type | Description |
|-------|------|-------------|
| `hexagon_id` | STRING | Uber H3 geospatial index (resolution 9, ~174m hexagons) |
| `hour` | INT | Hour of day (0-23) |
| `date` | DATE | Observation date (YYYY-MM-DD) |
| `avg_staying_duration_min` | FLOAT | Average time observed in hexagon (minutes) |
| `subscription_type` | STRING | Mobile plan type (Prepaid, Postpaid) |
| `nationality` | STRING | Roamer nationality |
| `gender` | STRING | Gender (Male, Female) |
| `age_group` | STRING | Age bracket (18-24, 25-34, 35-44, 45-54, 55+) |
| `subscriber_home_city` | STRING | Observed home city |

## Data Distributions

### Nationality
| Nationality | Percentage |
|-------------|------------|
| Belgian | 65% |
| French | 5% |
| Dutch | 4% |
| Moroccan | 4% |
| Turkish | 3% |
| Italian | 3% |
| Romanian | 3% |
| Polish | 2% |
| German | 2% |
| Portuguese | 2% |
| Other | 7% |

### Gender
| Gender | Percentage |
|--------|------------|
| Male | 50% |
| Female | 50% |

### Age Group
| Age Group | Percentage |
|-----------|------------|
| 18-24 | 15% |
| 25-34 | 22% |
| 35-44 | 20% |
| 45-54 | 20% |
| 55+ | 23% |

### Subscription Type
| Type | Percentage |
|------|------------|
| Postpaid | 65% |
| Prepaid | 35% |

### Cities
| City | Percentage |
|------|------------|
| Brussels | 28% |
| Antwerp | 16% |
| Ghent | 10% |
| Charleroi | 8% |
| Liege | 8% |
| Bruges | 5% |
| Namur | 4% |
| Leuven | 4% |
| Mons | 3% |
| Mechelen | 3% |
| Hasselt | 3% |
| Kortrijk | 3% |
| Ostend | 3% |
| Arlon | 2% |

### Average Staying Duration
- Min: 5 minutes
- Max: ~480 minutes
- Mean: ~30 minutes
- Distribution: Exponential (realistic for mobility data)

## H3 Geospatial Index

- Resolution: 9
- Hexagon edge length: ~174 meters
- Coverage: Urban areas of listed Belgian cities
- Coordinates are randomly distributed around city centers with Gaussian offset (std=0.04 degrees)

## BICS Global Network Context

| Attribute | Value |
|-----------|-------|
| MNO Partners | 700+ worldwide |
| Country Reach | 200+ countries |
| IoT Industries | Agriculture, Healthcare, Manufacturing, Transport, OEM |
| IoT Connectivity | NB-IoT, LTE-M, 4G, 5G |
| SIM Types | eSIM, Traditional SIM, iSIM |

## Snowflake Setup

### 1. Create Database, Schemas & Warehouse

```sql
CREATE DATABASE IF NOT EXISTS BICS_TELCO;

CREATE SCHEMA IF NOT EXISTS BICS_TELCO.MOBILITY_DATA;
CREATE SCHEMA IF NOT EXISTS BICS_TELCO.IOT_DATA;

CREATE WAREHOUSE IF NOT EXISTS COMPUTE_WH
  WAREHOUSE_SIZE = 'MEDIUM'
  AUTO_SUSPEND = 300
  AUTO_RESUME = TRUE;
```

### 2. Create Stage & File Format

```sql
USE SCHEMA BICS_TELCO.MOBILITY_DATA;

CREATE STAGE IF NOT EXISTS BICS_STREAMLIT_STAGE
  DIRECTORY = (ENABLE = TRUE);

CREATE FILE FORMAT IF NOT EXISTS BICS_CSV_FORMAT
  TYPE = CSV
  SKIP_HEADER = 1
  FIELD_OPTIONALLY_ENCLOSED_BY = '"';
```

### 3. Create Mobility Table & Load Data

```sql
CREATE OR REPLACE TABLE BICS_TELCO.MOBILITY_DATA.BICS_TELCO_MOBILITY_DATA (
    HEXAGON_ID VARCHAR,
    HOUR INTEGER,
    DATE DATE,
    AVG_STAYING_DURATION_MIN FLOAT,
    SUBSCRIPTION_TYPE VARCHAR,
    NATIONALITY VARCHAR,
    GENDER VARCHAR,
    AGE_GROUP VARCHAR,
    SUBSCRIBER_HOME_CITY VARCHAR
);

-- Upload CSVs to stage
PUT file:///path/to/bics_roaming_brussels_capital_jan2026.csv @BICS_STREAMLIT_STAGE/data/ AUTO_COMPRESS=TRUE;
PUT file:///path/to/bics_roaming_flanders_jan2026.csv @BICS_STREAMLIT_STAGE/data/ AUTO_COMPRESS=TRUE;
PUT file:///path/to/bics_roaming_wallonia_jan2026.csv @BICS_STREAMLIT_STAGE/data/ AUTO_COMPRESS=TRUE;

-- Load all region files
COPY INTO BICS_TELCO.MOBILITY_DATA.BICS_TELCO_MOBILITY_DATA
  FROM @BICS_STREAMLIT_STAGE/data/
  FILE_FORMAT = BICS_CSV_FORMAT
  PATTERN = '.*bics_roaming.*[.]csv[.]gz';
```

### 4. Create IoT Tables & Load Data

```sql
CREATE OR REPLACE TABLE BICS_TELCO.IOT_DATA.BICS_IOT_DEVICES (
    DEVICE_ID VARCHAR,
    INDUSTRY VARCHAR,
    DEVICE_TYPE VARCHAR,
    CONNECTIVITY_TYPE VARCHAR,
    SIM_TYPE VARCHAR,
    COUNTRY VARCHAR,
    CITY VARCHAR,
    SITE_NAME VARCHAR,
    LATITUDE FLOAT,
    LONGITUDE FLOAT
);

CREATE OR REPLACE TABLE BICS_TELCO.IOT_DATA.BICS_IOT_TELEMETRY (
    DEVICE_ID VARCHAR,
    INDUSTRY VARCHAR,
    DEVICE_TYPE VARCHAR,
    CONNECTIVITY_TYPE VARCHAR,
    SIM_TYPE VARCHAR,
    COUNTRY VARCHAR,
    CITY VARCHAR,
    SITE_NAME VARCHAR,
    LATITUDE FLOAT,
    LONGITUDE FLOAT,
    TIMESTAMP TIMESTAMP,
    DATE DATE,
    HOUR INTEGER,
    METRIC_NAME VARCHAR,
    METRIC_VALUE FLOAT,
    METRIC_UNIT VARCHAR,
    SIGNAL_STRENGTH_DBM INTEGER,
    DATA_USAGE_KB FLOAT,
    BATTERY_LEVEL_PCT FLOAT,
    DEVICE_STATUS VARCHAR,
    ALERT_FLAG BOOLEAN
);

-- Upload IoT CSVs
PUT file:///path/to/bics_iot_devices.csv @BICS_STREAMLIT_STAGE/data/ AUTO_COMPRESS=TRUE;
PUT file:///path/to/bics_iot_telemetry.csv @BICS_STREAMLIT_STAGE/data/ AUTO_COMPRESS=TRUE;

-- Load device registry
COPY INTO BICS_TELCO.IOT_DATA.BICS_IOT_DEVICES
  FROM @BICS_TELCO.MOBILITY_DATA.BICS_STREAMLIT_STAGE/data/bics_iot_devices
  FILE_FORMAT = BICS_CSV_FORMAT;

-- Load telemetry
COPY INTO BICS_TELCO.IOT_DATA.BICS_IOT_TELEMETRY
  FROM @BICS_TELCO.MOBILITY_DATA.BICS_STREAMLIT_STAGE/data/bics_iot_telemetry
  FILE_FORMAT = BICS_CSV_FORMAT;
```

### 5. Deploy Streamlit App

```sql
-- Upload app files to stage
PUT file:///path/to/streamlit_app/streamlit_app.py @BICS_STREAMLIT_STAGE OVERWRITE=TRUE AUTO_COMPRESS=FALSE;
PUT file:///path/to/streamlit_app/environment.yml @BICS_STREAMLIT_STAGE OVERWRITE=TRUE AUTO_COMPRESS=FALSE;
PUT file:///path/to/streamlit_app/pages/*.py @BICS_STREAMLIT_STAGE/pages/ OVERWRITE=TRUE AUTO_COMPRESS=FALSE;
PUT file:///path/to/streamlit_app/utils/*.py @BICS_STREAMLIT_STAGE/utils/ OVERWRITE=TRUE AUTO_COMPRESS=FALSE;

-- Create Streamlit app
CREATE OR REPLACE STREAMLIT BICS_TELCO.MOBILITY_DATA.BICS_APP
  ROOT_LOCATION = '@BICS_TELCO.MOBILITY_DATA.BICS_STREAMLIT_STAGE'
  MAIN_FILE = 'streamlit_app.py'
  QUERY_WAREHOUSE = 'COMPUTE_WH';

-- Grant access
GRANT USAGE ON STREAMLIT BICS_TELCO.MOBILITY_DATA.BICS_APP TO ROLE <role_name>;
```

## Repo Structure

```
BICS_monetization/
├── README.md                              # This file
├── generate_telco_data.py                 # Mobility data generator (3 regions)
├── generate_iot_data.py                   # IoT data generator (5 industries)
├── create_market_intelligence_doc.py      # Market report generator
├── bics_mobility_semantic_view.yaml       # Cortex Analyst semantic model
├── BICS_Market_Intelligence_Report.docx   # Generated market report
└── streamlit_app/
    ├── streamlit_app.py                   # Main entry point + data product catalog
    ├── environment.yml                    # Snowflake dependencies
    ├── logo.png
    ├── pages/
    │   ├── 0_Market_Intelligence.py       # Market strategy and pricing
    │   ├── 1_Data_Explorer.py             # Data browsing and filtering
    │   ├── 2_Analytics_Dashboard.py       # Mobility charts and insights
    │   ├── 3_Map_Visualization.py         # H3 hexagon maps
    │   ├── 4_Data_Export.py               # Data export/purchase
    │   ├── 5_IoT_Analytics.py             # IoT industry analytics dashboard
    │   └── 6_IoT_Device_Map.py            # IoT device geographic map
    └── utils/
        ├── __init__.py
        └── styles.py                      # Shared BICS styles and components
```
