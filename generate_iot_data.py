import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(2026)

INDUSTRIES = {
    "Agriculture": {
        "device_types": {
            "Soil Moisture Sensor": {"metrics": [("soil_moisture", "%", 20, 80), ("soil_temperature", "C", -2, 35), ("soil_ph", "pH", 5.5, 7.5)], "interval_min": 30, "battery": True},
            "Weather Station": {"metrics": [("air_temperature", "C", -5, 38), ("humidity", "%", 30, 95), ("wind_speed", "km/h", 0, 80), ("rainfall", "mm", 0, 25)], "interval_min": 15, "battery": False},
            "GPS Tractor Tracker": {"metrics": [("speed", "km/h", 0, 40), ("fuel_level", "%", 10, 100), ("engine_hours", "h", 0, 12)], "interval_min": 5, "battery": False},
            "Irrigation Controller": {"metrics": [("flow_rate", "L/min", 0, 500), ("pressure", "bar", 1, 6), ("valve_status", "bool", 0, 1)], "interval_min": 15, "battery": False},
            "Greenhouse Climate Sensor": {"metrics": [("temperature", "C", 15, 40), ("humidity", "%", 40, 95), ("co2_level", "ppm", 300, 2000), ("light_intensity", "lux", 0, 80000)], "interval_min": 10, "battery": True},
            "Livestock Tracker": {"metrics": [("body_temperature", "C", 37, 41), ("activity_level", "steps/h", 0, 500), ("heart_rate", "bpm", 40, 120)], "interval_min": 30, "battery": True},
        },
        "locations": [
            {"city": "Bruges", "lat": 51.21, "lon": 3.22, "site": "West Flanders Farmlands"},
            {"city": "Kortrijk", "lat": 50.83, "lon": 3.27, "site": "Leie Valley Agriculture"},
            {"city": "Hasselt", "lat": 50.93, "lon": 5.34, "site": "Limburg Orchards"},
            {"city": "Arlon", "lat": 49.68, "lon": 5.82, "site": "Luxembourg Province Dairy"},
            {"city": "Namur", "lat": 50.47, "lon": 4.87, "site": "Wallonia Grain Belt"},
            {"city": "Leuven", "lat": 50.88, "lon": 4.70, "site": "Brabant Research Farm"},
        ],
        "connectivity_weights": {"NB-IoT": 0.45, "LTE-M": 0.35, "4G": 0.15, "5G": 0.05},
        "device_count": 180,
    },
    "Healthcare": {
        "device_types": {
            "Patient Monitor": {"metrics": [("heart_rate", "bpm", 50, 120), ("spo2", "%", 88, 100), ("blood_pressure_sys", "mmHg", 90, 180), ("respiration_rate", "breaths/min", 10, 30)], "interval_min": 1, "battery": True},
            "Asset Tracking Tag": {"metrics": [("rssi", "dBm", -90, -30), ("battery_voltage", "V", 2.5, 3.3)], "interval_min": 60, "battery": True},
            "Cold Chain Sensor": {"metrics": [("temperature", "C", -80, 8), ("humidity", "%", 20, 60), ("door_open", "bool", 0, 1)], "interval_min": 5, "battery": True},
            "Infusion Pump Monitor": {"metrics": [("flow_rate", "mL/h", 0, 1000), ("volume_infused", "mL", 0, 2000), ("occlusion_pressure", "mmHg", 0, 800)], "interval_min": 5, "battery": False},
            "Environmental Monitor": {"metrics": [("room_temperature", "C", 18, 26), ("humidity", "%", 30, 60), ("air_quality_index", "AQI", 0, 150)], "interval_min": 15, "battery": False},
        },
        "locations": [
            {"city": "Brussels", "lat": 50.85, "lon": 4.35, "site": "UZ Brussel Hospital"},
            {"city": "Brussels", "lat": 50.84, "lon": 4.39, "site": "Saint-Luc University Hospital"},
            {"city": "Antwerp", "lat": 51.22, "lon": 4.41, "site": "UZA Antwerp"},
            {"city": "Ghent", "lat": 51.05, "lon": 3.73, "site": "UZ Ghent"},
            {"city": "Liege", "lat": 50.63, "lon": 5.58, "site": "CHU de Liege"},
            {"city": "Leuven", "lat": 50.88, "lon": 4.67, "site": "UZ Leuven"},
        ],
        "connectivity_weights": {"4G": 0.40, "5G": 0.30, "LTE-M": 0.20, "NB-IoT": 0.10},
        "device_count": 200,
    },
    "Industrial Manufacturing": {
        "device_types": {
            "Vibration Sensor": {"metrics": [("vibration_rms", "mm/s", 0, 25), ("frequency_peak", "Hz", 10, 5000), ("temperature", "C", 20, 120)], "interval_min": 5, "battery": True},
            "Pressure Gauge": {"metrics": [("pressure", "bar", 0, 100), ("temperature", "C", 10, 200)], "interval_min": 10, "battery": False},
            "Power Meter": {"metrics": [("power_consumption", "kW", 0, 500), ("voltage", "V", 210, 250), ("current", "A", 0, 800), ("power_factor", "ratio", 0.7, 1.0)], "interval_min": 15, "battery": False},
            "CNC Machine Monitor": {"metrics": [("spindle_speed", "rpm", 0, 15000), ("feed_rate", "mm/min", 0, 5000), ("tool_wear", "%", 0, 100)], "interval_min": 5, "battery": False},
            "Environmental Sensor": {"metrics": [("temperature", "C", 15, 45), ("humidity", "%", 20, 80), ("particulate_matter", "ug/m3", 0, 200)], "interval_min": 30, "battery": True},
            "Conveyor Belt Monitor": {"metrics": [("belt_speed", "m/s", 0, 5), ("motor_temperature", "C", 30, 90), ("load_weight", "kg", 0, 2000)], "interval_min": 10, "battery": False},
        },
        "locations": [
            {"city": "Antwerp", "lat": 51.27, "lon": 4.35, "site": "Port of Antwerp Industrial Zone"},
            {"city": "Charleroi", "lat": 50.41, "lon": 4.44, "site": "Charleroi Steel Works"},
            {"city": "Ghent", "lat": 51.07, "lon": 3.75, "site": "Ghent Chemical Cluster"},
            {"city": "Mechelen", "lat": 51.03, "lon": 4.48, "site": "Mechelen Tech Campus"},
            {"city": "Hasselt", "lat": 50.93, "lon": 5.33, "site": "Genk Auto Assembly"},
            {"city": "Liege", "lat": 50.62, "lon": 5.62, "site": "Liege Aerospace Park"},
        ],
        "connectivity_weights": {"5G": 0.35, "4G": 0.30, "LTE-M": 0.25, "NB-IoT": 0.10},
        "device_count": 200,
    },
    "Transport & Logistics": {
        "device_types": {
            "Fleet GPS Tracker": {"metrics": [("speed", "km/h", 0, 130), ("heading", "degrees", 0, 360), ("odometer", "km", 0, 500000)], "interval_min": 2, "battery": False},
            "Container Sensor": {"metrics": [("temperature", "C", -25, 30), ("humidity", "%", 20, 90), ("door_status", "bool", 0, 1), ("shock_g", "g", 0, 5)], "interval_min": 15, "battery": True},
            "Cold Chain Monitor": {"metrics": [("cargo_temperature", "C", -25, 8), ("ambient_temperature", "C", -10, 40), ("compressor_status", "bool", 0, 1)], "interval_min": 10, "battery": False},
            "Fuel Sensor": {"metrics": [("fuel_level", "%", 5, 100), ("consumption_rate", "L/100km", 5, 45), ("adblue_level", "%", 10, 100)], "interval_min": 15, "battery": False},
            "Trailer Tracker": {"metrics": [("tire_pressure", "bar", 5, 10), ("axle_temperature", "C", 10, 80), ("load_weight", "tonnes", 0, 30)], "interval_min": 30, "battery": True},
            "Drone Delivery": {"metrics": [("altitude", "m", 0, 120), ("speed", "km/h", 0, 80), ("battery_remaining", "%", 5, 100), ("payload_weight", "kg", 0, 5)], "interval_min": 5, "battery": True},
        },
        "locations": [
            {"city": "Antwerp", "lat": 51.30, "lon": 4.28, "site": "Port of Antwerp Container Terminal"},
            {"city": "Brussels", "lat": 50.90, "lon": 4.48, "site": "Brussels Airport Cargo"},
            {"city": "Liege", "lat": 50.64, "lon": 5.45, "site": "Liege Airport Logistics Hub"},
            {"city": "Zeebrugge", "lat": 51.33, "lon": 3.18, "site": "Zeebrugge Port"},
            {"city": "Ghent", "lat": 51.10, "lon": 3.74, "site": "Ghent Logistics Park"},
            {"city": "Mechelen", "lat": 51.02, "lon": 4.50, "site": "E19 Corridor Hub"},
        ],
        "connectivity_weights": {"4G": 0.40, "LTE-M": 0.30, "NB-IoT": 0.15, "5G": 0.15},
        "device_count": 220,
    },
    "OEM": {
        "device_types": {
            "Smart Meter": {"metrics": [("energy_reading", "kWh", 0, 50), ("voltage", "V", 210, 250), ("frequency", "Hz", 49.8, 50.2)], "interval_min": 60, "battery": False},
            "Connected Vehicle Module": {"metrics": [("speed", "km/h", 0, 200), ("engine_status", "bool", 0, 1), ("diagnostic_code", "count", 0, 10), ("mileage", "km", 0, 300000)], "interval_min": 30, "battery": False},
            "Industrial Gateway": {"metrics": [("cpu_usage", "%", 5, 95), ("memory_usage", "%", 20, 90), ("uptime", "hours", 0, 8760), ("connected_devices", "count", 1, 50)], "interval_min": 60, "battery": False},
            "Wearable Device": {"metrics": [("heart_rate", "bpm", 50, 150), ("steps", "count", 0, 1000), ("battery_level", "%", 5, 100)], "interval_min": 60, "battery": True},
            "Smart Display": {"metrics": [("screen_brightness", "%", 10, 100), ("content_updates", "count", 0, 50), ("uptime", "hours", 0, 720)], "interval_min": 60, "battery": False},
            "Edge Compute Node": {"metrics": [("cpu_load", "%", 5, 100), ("gpu_utilization", "%", 0, 100), ("inference_latency", "ms", 1, 200), ("throughput", "req/s", 0, 1000)], "interval_min": 15, "battery": False},
        },
        "locations": [
            {"city": "Brussels", "lat": 50.86, "lon": 4.36, "site": "Brussels Smart City Deployment"},
            {"city": "Antwerp", "lat": 51.22, "lon": 4.40, "site": "Antwerp Connected Fleet"},
            {"city": "Ghent", "lat": 51.05, "lon": 3.72, "site": "Ghent IoT Living Lab"},
            {"city": "Leuven", "lat": 50.88, "lon": 4.70, "site": "imec Research Campus"},
            {"city": "Mechelen", "lat": 51.03, "lon": 4.48, "site": "Telenet HQ Connected Home"},
            {"city": "Mons", "lat": 50.45, "lon": 3.96, "site": "Digital Innovation Hub Mons"},
        ],
        "connectivity_weights": {"4G": 0.35, "5G": 0.25, "LTE-M": 0.25, "NB-IoT": 0.15},
        "device_count": 200,
    },
}

SIM_TYPES = {"eSIM": 0.50, "Traditional SIM": 0.35, "iSIM": 0.15}

READINGS_PER_DEVICE = 150

def weighted_choice(choices_dict, n):
    items = list(choices_dict.keys())
    weights = list(choices_dict.values())
    return np.random.choice(items, size=n, p=weights)


def generate_device_registry(industry_name, config):
    devices = []
    device_types = list(config["device_types"].keys())
    type_weights = np.ones(len(device_types)) / len(device_types)
    locations = config["locations"]
    conn_types = config["connectivity_weights"]

    for i in range(config["device_count"]):
        dev_type = np.random.choice(device_types, p=type_weights)
        loc = locations[np.random.randint(len(locations))]
        conn = weighted_choice(conn_types, 1)[0]
        sim = weighted_choice(SIM_TYPES, 1)[0]

        lat_jitter = np.random.normal(0, 0.015)
        lon_jitter = np.random.normal(0, 0.015)

        devices.append({
            "device_id": f"BICS-{industry_name[:3].upper()}-{i+1:05d}",
            "industry": industry_name,
            "device_type": dev_type,
            "connectivity_type": conn,
            "sim_type": sim,
            "country": "Belgium",
            "city": loc["city"],
            "site_name": loc["site"],
            "latitude": round(loc["lat"] + lat_jitter, 6),
            "longitude": round(loc["lon"] + lon_jitter, 6),
        })
    return devices


def generate_telemetry(devices, config, start_date, end_date):
    rows = []
    total_days = (end_date - start_date).days + 1

    for dev in devices:
        dev_type_cfg = config["device_types"][dev["device_type"]]
        has_battery = dev_type_cfg["battery"]

        n = READINGS_PER_DEVICE
        timestamps = [start_date + timedelta(
            days=np.random.randint(0, total_days),
            hours=np.random.randint(0, 24),
            minutes=np.random.randint(0, 60)
        ) for _ in range(n)]
        timestamps.sort()

        battery_base = np.random.uniform(60, 100) if has_battery else None
        signal_base = np.random.randint(-85, -40)

        for ts in timestamps:
            metric = dev_type_cfg["metrics"][np.random.randint(len(dev_type_cfg["metrics"]))]
            metric_name, unit, vmin, vmax = metric

            if unit == "bool":
                value = round(float(np.random.choice([0, 1])), 1)
            else:
                value = round(np.random.uniform(vmin, vmax), 2)

            hour = ts.hour
            is_working = 6 <= hour <= 22

            signal = signal_base + np.random.randint(-10, 10)
            signal = max(-100, min(-20, signal))

            data_kb = round(np.random.exponential(2.5), 2)

            battery = None
            if has_battery:
                decay = (ts - start_date).total_seconds() / (total_days * 86400) * np.random.uniform(10, 40)
                battery = round(max(5, battery_base - decay + np.random.normal(0, 2)), 1)

            alert = False
            status = "active"
            if np.random.random() < 0.02:
                status = "offline"
            elif np.random.random() < 0.05:
                status = "warning"
                alert = True
            elif np.random.random() < 0.01:
                status = "critical"
                alert = True

            rows.append({
                "device_id": dev["device_id"],
                "industry": dev["industry"],
                "device_type": dev["device_type"],
                "connectivity_type": dev["connectivity_type"],
                "sim_type": dev["sim_type"],
                "country": dev["country"],
                "city": dev["city"],
                "site_name": dev["site_name"],
                "latitude": dev["latitude"],
                "longitude": dev["longitude"],
                "timestamp": ts,
                "date": ts.date(),
                "hour": hour,
                "metric_name": metric_name,
                "metric_value": value,
                "metric_unit": unit,
                "signal_strength_dbm": signal,
                "data_usage_kb": data_kb,
                "battery_level_pct": battery,
                "device_status": status,
                "alert_flag": alert,
            })
    return rows


print("=" * 60)
print("GENERATING BICS IoT DATASETS - JANUARY 2026")
print("=" * 60)

start_date = datetime(2026, 1, 1)
end_date = datetime(2026, 1, 31)

all_devices = []
all_telemetry = []

for ind_name, ind_cfg in INDUSTRIES.items():
    print(f"\n--- {ind_name} ---")
    devs = generate_device_registry(ind_name, ind_cfg)
    all_devices.extend(devs)
    print(f"  Devices registered: {len(devs)}")

    telemetry = generate_telemetry(devs, ind_cfg, start_date, end_date)
    all_telemetry.extend(telemetry)
    print(f"  Telemetry records: {len(telemetry):,}")

devices_df = pd.DataFrame(all_devices)
devices_file = "bics_iot_devices.csv"
devices_df.to_csv(devices_file, index=False)
dev_size = os.path.getsize(devices_file) / (1024 * 1024)
print(f"\nDevice registry saved: {devices_file} ({len(devices_df):,} devices, {dev_size:.1f} MB)")

telemetry_df = pd.DataFrame(all_telemetry)
telemetry_df = telemetry_df.sort_values(["industry", "device_id", "timestamp"]).reset_index(drop=True)
telemetry_file = "bics_iot_telemetry.csv"
telemetry_df.to_csv(telemetry_file, index=False)
tel_size = os.path.getsize(telemetry_file) / (1024 * 1024)
print(f"Telemetry saved: {telemetry_file} ({len(telemetry_df):,} records, {tel_size:.1f} MB)")

print("\n" + "=" * 60)
print("SUMMARY BY INDUSTRY")
print("=" * 60)
for ind in INDUSTRIES:
    d_count = len(devices_df[devices_df["industry"] == ind])
    t_count = len(telemetry_df[telemetry_df["industry"] == ind])
    alerts = telemetry_df[(telemetry_df["industry"] == ind) & (telemetry_df["alert_flag"] == True)]
    print(f"  {ind:30} | {d_count:4} devices | {t_count:>8,} readings | {len(alerts):>5,} alerts")

print("=" * 60)
print(f"  {'TOTAL':30} | {len(devices_df):4} devices | {len(telemetry_df):>8,} readings")
print("=" * 60)
print("\nFiles generated:")
print(f"  1. {devices_file} - Device registry (load into BICS_TELCO.IOT_DATA.BICS_IOT_DEVICES)")
print(f"  2. {telemetry_file} - Telemetry data (load into BICS_TELCO.IOT_DATA.BICS_IOT_TELEMETRY)")
