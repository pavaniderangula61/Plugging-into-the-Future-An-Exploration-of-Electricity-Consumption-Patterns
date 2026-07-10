import numpy as np
import pandas as pd

np.random.seed(42)

# Region -> States mapping (matches the real dataset's grouping)
REGION_STATES = {
    "Northern": ["Delhi", "Haryana", "Himachal Pradesh", "Jammu and Kashmir",
                 "Punjab", "Rajasthan", "Uttar Pradesh", "Uttarakhand", "Chandigarh"],
    "Western": ["Chhattisgarh", "Gujarat", "Madhya Pradesh", "Maharashtra", "Goa", "DNH"],
    "Southern": ["Andhra Pradesh", "Karnataka", "Kerala", "Tamil Nadu", "Telangana", "Puducherry"],
    "Eastern": ["Bihar", "Jharkhand", "Odisha", "West Bengal", "Sikkim"],
    "NorthEastern": ["Assam", "Tripura", "Meghalaya", "Manipur", "Mizoram", "Nagaland"],
}

# Approx lat/long for each state (rough centroids, good enough for map plots)
STATE_COORDS = {
    "Delhi": (28.7041, 77.1025), "Haryana": (29.0588, 76.0856),
    "Himachal Pradesh": (31.1048, 77.1734), "Jammu and Kashmir": (33.7782, 76.5762),
    "Punjab": (31.1471, 75.3412), "Rajasthan": (27.0238, 74.2179),
    "Uttar Pradesh": (26.8467, 80.9462), "Uttarakhand": (30.0668, 79.0193),
    "Chandigarh": (30.7333, 76.7794), "Chhattisgarh": (21.2787, 81.8661),
    "Gujarat": (22.2587, 71.1924), "Madhya Pradesh": (22.9734, 78.6569),
    "Maharashtra": (19.7515, 75.7139), "Goa": (15.2993, 74.1240),
    "DNH": (20.1809, 73.0169), "Andhra Pradesh": (15.9129, 79.7400),
    "Karnataka": (15.3173, 75.7139), "Kerala": (10.8505, 76.2711),
    "Tamil Nadu": (11.1271, 78.6569), "Telangana": (18.1124, 79.0193),
    "Puducherry": (11.9416, 79.8083), "Bihar": (25.0961, 85.3131),
    "Jharkhand": (23.6102, 85.2799), "Odisha": (20.9517, 85.0985),
    "West Bengal": (22.9868, 87.8550), "Sikkim": (27.5330, 88.5122),
    "Assam": (26.2006, 92.9376), "Tripura": (23.9408, 91.9882),
    "Meghalaya": (25.4670, 91.3662), "Manipur": (24.6637, 93.9063),
    "Mizoram": (23.1645, 92.9376), "Nagaland": (26.1584, 94.562)
}
BASE_USAGE = {
    "Delhi": 90, "Haryana": 110, "Himachal Pradesh": 20, "Jammu and Kashmir": 25,
    "Punjab": 130, "Rajasthan": 180, "Uttar Pradesh": 320, "Uttarakhand": 35,
    "Chandigarh": 8, "Chhattisgarh": 150, "Gujarat": 340, "Madhya Pradesh": 220,
    "Maharashtra": 380, "Goa": 12, "DNH": 15, "Andhra Pradesh": 180,
    "Karnataka": 230, "Kerala": 90, "Tamil Nadu": 320, "Telangana": 190,
    "Puducherry": 6, "Bihar": 90, "Jharkhand": 80, "Odisha": 110,
    "West Bengal": 160, "Sikkim": 3, "Assam": 45, "Tripura": 6,
    "Meghalaya": 5, "Manipur": 4, "Mizoram": 3, "Nagaland": 4,
}


def generate(start="2019-01-01", end="2020-12-05"):
    dates = pd.date_range(start, end, freq="D")
    lockdown_start = pd.Timestamp("2020-03-25")
    lockdown_end = pd.Timestamp("2020-06-08")

    rows = []
    for region, states in REGION_STATES.items():
        for state in states:
            base = BASE_USAGE[state]
            lat, lon = STATE_COORDS[state]
            # Industrial-heavy states drop more during lockdown; others (residential-heavy) rise
            industrial_bias = np.random.uniform(0.6, 1.0) if base > 100 else np.random.uniform(0.2, 0.5)

            for d in dates:
                day_of_year = d.dayofyear
                # Seasonality: higher usage in summer (Apr-Jun) & winter heating dip in between
                seasonal = 1 + 0.18 * np.sin(2 * np.pi * (day_of_year - 80) / 365)
                # Weekly effect: slightly lower on Sundays (less industrial activity)
                weekly = 0.95 if d.dayofweek == 6 else 1.0
                # Year-over-year growth
                yearly_growth = 1.03 if d.year == 2020 else 1.0

                usage = base * seasonal * weekly * yearly_growth

                if lockdown_start <= d <= lockdown_end:
                    # industrial states drop, residential-leaning states rise slightly
                    usage *= (1 - 0.35 * industrial_bias) if base > 100 else (1 + 0.10)

                noise = np.random.normal(0, base * 0.03)
                usage = max(usage + noise, 0)

                rows.append({
                    "Date": d.strftime("%Y-%m-%d"),
                    "States": state,
                    "Regions": region,
                    "latitude": lat,
                    "longitude": lon,
                    "Usage": round(usage, 2),
                })

    df = pd.DataFrame(rows)
    return df


if __name__ == "__main__":
    df = generate()
    out_path = "data/raw/long_data_.csv"
    df.to_csv(out_path, index=False)
    print(f"Generated {len(df):,} rows -> {out_path}")
    print(df.head())
