import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import h3
import os

np.random.seed(42)

ROWS_PER_REGION = 1_415_000

REGIONS = ['Brussels_Capital', 'Flanders', 'Wallonia']

NATIONALITIES = {
    'Belgian': 0.65,
    'French': 0.05,
    'Dutch': 0.04,
    'Moroccan': 0.04,
    'Turkish': 0.03,
    'Italian': 0.03,
    'Romanian': 0.03,
    'Polish': 0.02,
    'German': 0.02,
    'Portuguese': 0.02,
    'Other': 0.07
}

GENDER = {'Male': 0.50, 'Female': 0.50}

AGE_GROUPS = {
    '18-24': 0.15,
    '25-34': 0.22,
    '35-44': 0.20,
    '45-54': 0.20,
    '55+': 0.23
}

SUBSCRIPTION = {'Postpaid': 0.65, 'Prepaid': 0.35}

CITIES = {
    'Brussels': {'lat': 50.8503, 'lon': 4.3517, 'weight': 0.28},
    'Antwerp': {'lat': 51.2194, 'lon': 4.4025, 'weight': 0.16},
    'Ghent': {'lat': 51.0543, 'lon': 3.7174, 'weight': 0.10},
    'Charleroi': {'lat': 50.4108, 'lon': 4.4446, 'weight': 0.08},
    'Liège': {'lat': 50.6326, 'lon': 5.5797, 'weight': 0.08},
    'Bruges': {'lat': 51.2093, 'lon': 3.2247, 'weight': 0.05},
    'Namur': {'lat': 50.4674, 'lon': 4.8720, 'weight': 0.04},
    'Leuven': {'lat': 50.8798, 'lon': 4.7005, 'weight': 0.04},
    'Mons': {'lat': 50.4542, 'lon': 3.9563, 'weight': 0.03},
    'Mechelen': {'lat': 51.0259, 'lon': 4.4776, 'weight': 0.03},
    'Hasselt': {'lat': 50.9311, 'lon': 5.3378, 'weight': 0.03},
    'Kortrijk': {'lat': 50.8280, 'lon': 3.2650, 'weight': 0.03},
    'Ostend': {'lat': 51.2254, 'lon': 2.9180, 'weight': 0.03},
    'Arlon': {'lat': 49.6833, 'lon': 5.8167, 'weight': 0.02},
}

def weighted_choice(choices_dict, n):
    items = list(choices_dict.keys())
    weights = list(choices_dict.values())
    return np.random.choice(items, size=n, p=weights)

def generate_region_file(region_name, num_records):
    print(f"\nGenerating {region_name} data ({num_records:,} records)...")

    nationality = weighted_choice(NATIONALITIES, num_records)
    gender = weighted_choice(GENDER, num_records)
    age_group = weighted_choice(AGE_GROUPS, num_records)
    subscription_type = weighted_choice(SUBSCRIPTION, num_records)
    home_city = weighted_choice({k: v['weight'] for k, v in CITIES.items()}, num_records)

    start_date = datetime(2026, 1, 1)
    end_date = datetime(2026, 1, 31)
    date_range = (end_date - start_date).days + 1
    dates = [start_date + timedelta(days=np.random.randint(0, date_range)) for _ in range(num_records)]

    hour_probs = [
        0.01, 0.01, 0.01, 0.01, 0.02, 0.03,
        0.04, 0.06, 0.07, 0.07, 0.07, 0.07,
        0.06, 0.06, 0.06, 0.06, 0.06, 0.06,
        0.05, 0.05, 0.04, 0.03, 0.02, 0.02
    ]
    hour_probs = [p / sum(hour_probs) for p in hour_probs]
    hours = np.random.choice(range(24), size=num_records, p=hour_probs)

    avg_duration = np.clip(np.random.exponential(scale=30, size=num_records), 5, 480).round(1)

    print(f"  Generating H3 hexagon IDs...")
    h3_ids = []
    for city in home_city:
        city_info = CITIES[city]
        lat, lon = city_info['lat'], city_info['lon']
        lat_offset = np.random.normal(0, 0.04)
        lon_offset = np.random.normal(0, 0.04)
        h3_id = h3.latlng_to_cell(lat + lat_offset, lon + lon_offset, 9)
        h3_ids.append(h3_id)

    df = pd.DataFrame({
        'hexagon_id': h3_ids,
        'hour': hours,
        'date': dates,
        'avg_staying_duration_min': avg_duration,
        'subscription_type': subscription_type,
        'nationality': nationality,
        'gender': gender,
        'age_group': age_group,
        'subscriber_home_city': home_city
    })

    df['date'] = pd.to_datetime(df['date']).dt.date
    df = df.sort_values(['date', 'hour']).reset_index(drop=True)

    safe_name = region_name.lower().replace(' ', '_')
    filename = f'bics_roaming_{safe_name}_jan2026.csv'
    df.to_csv(filename, index=False)

    size_mb = os.path.getsize(filename) / (1024 * 1024)
    print(f"  Saved: {filename} ({size_mb:.1f} MB)")

    return filename, len(df), size_mb


print("="*50)
print("GENERATING BICS ROAMING DATASETS - JANUARY 2026")
print("="*50)

results = []
for region in REGIONS:
    filename, rows, size = generate_region_file(region, ROWS_PER_REGION)
    results.append((region, filename, rows, size))

print("\n" + "="*50)
print("SUMMARY")
print("="*50)
for region, filename, rows, size in results:
    print(f"{region:20} | {filename:45} | {rows:,} rows | {size:.1f} MB")
print("="*50)
total_rows = sum(r[2] for r in results)
total_size = sum(r[3] for r in results)
print(f"{'TOTAL':20} | {'':45} | {total_rows:,} rows | {total_size:.1f} MB")
