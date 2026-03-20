------------------------------------------------------------------------
-- BICS Mobility & IoT Intelligence Platform — Full DDL
-- Run this script once to create all Snowflake objects from scratch.
-- Source: https://github.com/pmjose/BICS_monetization
------------------------------------------------------------------------

------------------------------------------------------------------------
-- 1. DATABASE & SCHEMAS
------------------------------------------------------------------------
CREATE DATABASE IF NOT EXISTS BICS_TELCO
    COMMENT = 'BICS Mobility & IoT Intelligence Platform — roaming signaling data and IoT telemetry';

CREATE SCHEMA IF NOT EXISTS BICS_TELCO.MOBILITY_DATA
    COMMENT = 'Roaming mobility data from BICS global carrier network (700+ MNO partners)';

CREATE SCHEMA IF NOT EXISTS BICS_TELCO.IOT_DATA
    COMMENT = 'IoT device registry and telemetry across 5 enterprise verticals';

------------------------------------------------------------------------
-- 2. WAREHOUSE
------------------------------------------------------------------------
CREATE WAREHOUSE IF NOT EXISTS COMPUTE_WH
    WAREHOUSE_SIZE      = 'MEDIUM'
    AUTO_SUSPEND        = 300
    AUTO_RESUME         = TRUE
    INITIALLY_SUSPENDED = TRUE
    COMMENT             = 'General-purpose warehouse for BICS analytics and Streamlit app';

USE WAREHOUSE COMPUTE_WH;

------------------------------------------------------------------------
-- 3. GIT REPOSITORY INTEGRATION
------------------------------------------------------------------------
CREATE OR REPLACE API INTEGRATION BICS_GITHUB_INTEGRATION
    API_PROVIDER       = git_https_api
    API_ALLOWED_PREFIXES = ('https://github.com/pmjose/')
    ENABLED            = TRUE
    COMMENT            = 'GitHub integration for BICS_monetization repo';

CREATE OR REPLACE GIT REPOSITORY BICS_TELCO.MOBILITY_DATA.BICS_REPO
    API_INTEGRATION = BICS_GITHUB_INTEGRATION
    ORIGIN          = 'https://github.com/pmjose/BICS_monetization.git';

ALTER GIT REPOSITORY BICS_TELCO.MOBILITY_DATA.BICS_REPO FETCH;

-- Verify repo contents
LS @BICS_TELCO.MOBILITY_DATA.BICS_REPO/branches/main/;

------------------------------------------------------------------------
-- 4. FILE FORMAT
------------------------------------------------------------------------
CREATE FILE FORMAT IF NOT EXISTS BICS_TELCO.MOBILITY_DATA.BICS_CSV_FORMAT
    TYPE                         = CSV
    SKIP_HEADER                  = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    NULL_IF                      = ('', 'NULL', 'None')
    COMMENT                      = 'Standard CSV format for BICS data loads';

------------------------------------------------------------------------
-- 5. INTERNAL STAGE (for Streamlit app files)
------------------------------------------------------------------------
CREATE STAGE IF NOT EXISTS BICS_TELCO.MOBILITY_DATA.BICS_STREAMLIT_STAGE
    DIRECTORY   = (ENABLE = TRUE)
    FILE_FORMAT = BICS_TELCO.MOBILITY_DATA.BICS_CSV_FORMAT
    COMMENT     = 'Stage for Streamlit app files';

------------------------------------------------------------------------
-- 6. MOBILITY TABLE
------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS BICS_TELCO.MOBILITY_DATA.BICS_TELCO_MOBILITY_DATA (
    HEXAGON_ID               VARCHAR   NOT NULL  COMMENT 'Uber H3 geospatial index (resolution 9, ~174 m hexagons)',
    HOUR                     INTEGER   NOT NULL  COMMENT 'Hour of day (0-23)',
    DATE                     DATE      NOT NULL  COMMENT 'Observation date',
    AVG_STAYING_DURATION_MIN FLOAT     NOT NULL  COMMENT 'Average dwell time in hexagon (minutes)',
    SUBSCRIPTION_TYPE        VARCHAR   NOT NULL  COMMENT 'Prepaid or Postpaid',
    NATIONALITY              VARCHAR   NOT NULL  COMMENT 'Roamer nationality',
    GENDER                   VARCHAR   NOT NULL  COMMENT 'Male or Female',
    AGE_GROUP                VARCHAR   NOT NULL  COMMENT 'Age bracket (18-24, 25-34, 35-44, 45-54, 55+)',
    SUBSCRIBER_HOME_CITY     VARCHAR   NOT NULL  COMMENT 'Observed home city'
)
COMMENT = 'Anonymised roaming signaling data from BICS global network — 4.2 M+ records, Jan 2026';

------------------------------------------------------------------------
-- 7. IOT DEVICE REGISTRY TABLE
------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS BICS_TELCO.IOT_DATA.BICS_IOT_DEVICES (
    DEVICE_ID         VARCHAR NOT NULL  COMMENT 'Unique device identifier (BICS-XXX-00001)',
    INDUSTRY          VARCHAR NOT NULL  COMMENT 'Agriculture | Healthcare | Industrial Manufacturing | Transport & Logistics | OEM',
    DEVICE_TYPE       VARCHAR NOT NULL  COMMENT 'Sensor / tracker type',
    CONNECTIVITY_TYPE VARCHAR NOT NULL  COMMENT 'NB-IoT | LTE-M | 4G | 5G',
    SIM_TYPE          VARCHAR NOT NULL  COMMENT 'eSIM | Traditional SIM | iSIM',
    COUNTRY           VARCHAR NOT NULL  COMMENT 'Deployment country',
    CITY              VARCHAR NOT NULL  COMMENT 'Deployment city',
    SITE_NAME         VARCHAR NOT NULL  COMMENT 'Deployment site name',
    LATITUDE          FLOAT   NOT NULL  COMMENT 'Device latitude',
    LONGITUDE         FLOAT   NOT NULL  COMMENT 'Device longitude'
)
COMMENT = 'IoT device registry — ~1,000 devices across 5 BICS enterprise verticals';

------------------------------------------------------------------------
-- 8. IOT TELEMETRY TABLE
------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS BICS_TELCO.IOT_DATA.BICS_IOT_TELEMETRY (
    DEVICE_ID           VARCHAR   NOT NULL  COMMENT 'Foreign key to BICS_IOT_DEVICES',
    INDUSTRY            VARCHAR   NOT NULL  COMMENT 'Industry vertical',
    DEVICE_TYPE         VARCHAR   NOT NULL  COMMENT 'Sensor / tracker type',
    CONNECTIVITY_TYPE   VARCHAR   NOT NULL  COMMENT 'NB-IoT | LTE-M | 4G | 5G',
    SIM_TYPE            VARCHAR   NOT NULL  COMMENT 'eSIM | Traditional SIM | iSIM',
    COUNTRY             VARCHAR   NOT NULL  COMMENT 'Deployment country',
    CITY                VARCHAR   NOT NULL  COMMENT 'Deployment city',
    SITE_NAME           VARCHAR   NOT NULL  COMMENT 'Deployment site name',
    LATITUDE            FLOAT     NOT NULL  COMMENT 'Reading latitude',
    LONGITUDE           FLOAT     NOT NULL  COMMENT 'Reading longitude',
    TIMESTAMP           TIMESTAMP NOT NULL  COMMENT 'Telemetry reading timestamp',
    DATE                DATE      NOT NULL  COMMENT 'Reading date',
    HOUR                INTEGER   NOT NULL  COMMENT 'Reading hour (0-23)',
    METRIC_NAME         VARCHAR   NOT NULL  COMMENT 'Metric being reported',
    METRIC_VALUE        FLOAT     NOT NULL  COMMENT 'Metric value',
    METRIC_UNIT         VARCHAR   NOT NULL  COMMENT 'Unit of measurement',
    SIGNAL_STRENGTH_DBM INTEGER   NOT NULL  COMMENT 'Cellular signal strength (dBm)',
    DATA_USAGE_KB       FLOAT     NOT NULL  COMMENT 'Data transmitted (KB)',
    BATTERY_LEVEL_PCT   FLOAT              COMMENT 'Battery level (%) — NULL for mains-powered devices',
    DEVICE_STATUS       VARCHAR   NOT NULL  COMMENT 'active | warning | critical | offline',
    ALERT_FLAG          BOOLEAN   NOT NULL  COMMENT 'TRUE when anomaly detected'
)
COMMENT = 'IoT telemetry readings — ~150,000 records, Jan 2026';

------------------------------------------------------------------------
-- 9. LOAD DATA FROM GITHUB REPO
------------------------------------------------------------------------
-- Mobility data (3 region files)
COPY INTO BICS_TELCO.MOBILITY_DATA.BICS_TELCO_MOBILITY_DATA
    FROM @BICS_TELCO.MOBILITY_DATA.BICS_REPO/branches/main/
    FILE_FORMAT = BICS_TELCO.MOBILITY_DATA.BICS_CSV_FORMAT
    PATTERN     = '.*bics_roaming.*[.]csv'
    ON_ERROR    = ABORT_STATEMENT;

-- IoT device registry
COPY INTO BICS_TELCO.IOT_DATA.BICS_IOT_DEVICES
    FROM @BICS_TELCO.MOBILITY_DATA.BICS_REPO/branches/main/bics_iot_devices.csv
    FILE_FORMAT = BICS_TELCO.MOBILITY_DATA.BICS_CSV_FORMAT
    ON_ERROR    = ABORT_STATEMENT;

-- IoT telemetry
COPY INTO BICS_TELCO.IOT_DATA.BICS_IOT_TELEMETRY
    FROM @BICS_TELCO.MOBILITY_DATA.BICS_REPO/branches/main/bics_iot_telemetry.csv
    FILE_FORMAT = BICS_TELCO.MOBILITY_DATA.BICS_CSV_FORMAT
    ON_ERROR    = ABORT_STATEMENT;

------------------------------------------------------------------------
-- 10. DEPLOY STREAMLIT APP (copy from git repo to Streamlit stage)
------------------------------------------------------------------------
COPY FILES
    INTO @BICS_TELCO.MOBILITY_DATA.BICS_STREAMLIT_STAGE/
    FROM @BICS_TELCO.MOBILITY_DATA.BICS_REPO/branches/main/streamlit_app/streamlit_app.py;

COPY FILES
    INTO @BICS_TELCO.MOBILITY_DATA.BICS_STREAMLIT_STAGE/
    FROM @BICS_TELCO.MOBILITY_DATA.BICS_REPO/branches/main/streamlit_app/environment.yml;

COPY FILES
    INTO @BICS_TELCO.MOBILITY_DATA.BICS_STREAMLIT_STAGE/
    FROM @BICS_TELCO.MOBILITY_DATA.BICS_REPO/branches/main/streamlit_app/logo.jpg;

COPY FILES
    INTO @BICS_TELCO.MOBILITY_DATA.BICS_STREAMLIT_STAGE/pages/
    FROM @BICS_TELCO.MOBILITY_DATA.BICS_REPO/branches/main/streamlit_app/pages/
    PATTERN = '.*[.]py';

COPY FILES
    INTO @BICS_TELCO.MOBILITY_DATA.BICS_STREAMLIT_STAGE/utils/
    FROM @BICS_TELCO.MOBILITY_DATA.BICS_REPO/branches/main/streamlit_app/utils/
    PATTERN = '.*[.]py';

CREATE OR REPLACE STREAMLIT BICS_TELCO.MOBILITY_DATA.BICS_APP
    ROOT_LOCATION   = '@BICS_TELCO.MOBILITY_DATA.BICS_STREAMLIT_STAGE'
    MAIN_FILE       = 'streamlit_app.py'
    QUERY_WAREHOUSE = 'COMPUTE_WH'
    COMMENT         = 'BICS Mobility & IoT Intelligence Platform';

------------------------------------------------------------------------
-- 11. GRANTS (adjust role names to your environment)
------------------------------------------------------------------------
GRANT USAGE  ON DATABASE  BICS_TELCO                                    TO ROLE PUBLIC;
GRANT USAGE  ON SCHEMA    BICS_TELCO.MOBILITY_DATA                      TO ROLE PUBLIC;
GRANT USAGE  ON SCHEMA    BICS_TELCO.IOT_DATA                           TO ROLE PUBLIC;
GRANT SELECT ON TABLE     BICS_TELCO.MOBILITY_DATA.BICS_TELCO_MOBILITY_DATA TO ROLE PUBLIC;
GRANT SELECT ON TABLE     BICS_TELCO.IOT_DATA.BICS_IOT_DEVICES              TO ROLE PUBLIC;
GRANT SELECT ON TABLE     BICS_TELCO.IOT_DATA.BICS_IOT_TELEMETRY            TO ROLE PUBLIC;
GRANT USAGE  ON WAREHOUSE COMPUTE_WH                                    TO ROLE PUBLIC;
GRANT USAGE  ON STREAMLIT BICS_TELCO.MOBILITY_DATA.BICS_APP             TO ROLE PUBLIC;

------------------------------------------------------------------------
-- 12. VERIFICATION
------------------------------------------------------------------------
SELECT 'MOBILITY_DATA' AS dataset, COUNT(*) AS row_count FROM BICS_TELCO.MOBILITY_DATA.BICS_TELCO_MOBILITY_DATA
UNION ALL
SELECT 'IOT_DEVICES',              COUNT(*)               FROM BICS_TELCO.IOT_DATA.BICS_IOT_DEVICES
UNION ALL
SELECT 'IOT_TELEMETRY',            COUNT(*)               FROM BICS_TELCO.IOT_DATA.BICS_IOT_TELEMETRY;
