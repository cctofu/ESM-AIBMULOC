import os
import json
import pandas as pd
import colorful as cf

cf.use_style('monokai')
DATA_DIR = "./data"

FILE_MAP= {
    "avg_individual_income.csv": "ZIP code",
    "child_care_regulated.csv": "zip_code",
    "employment_rate.csv": "zipcode",
    "population.csv": "zipcode",
    "potential_locations.csv": "zipcode",
}

'''
Ensure zipcode is 5 digits, trim to 5 if longer than 5
'''
def normalize_zip(z):
    s = str(z).strip()
    s = s[:5] if len(s) > 5 else s
    return s if s else None

'''
Ensure zipcode is 5 digits, trim to 5 if longer than 5
'''
def load_csv(path, zip_col):
    df = pd.read_csv(path)
    df = df.copy()
    df[zip_col] = df[zip_col].map(normalize_zip)
    df = df.dropna(subset=[zip_col])
    return df

'''
Find the intersection between the zipcodes within the 5 data files
'''
def find_zipcode_intersection():
    intersection = None
    for fname, zcol in FILE_MAP.items():
        path = os.path.join(DATA_DIR, fname)
        df = load_csv(path, zcol)
        zips = set(df[zcol].astype(str))
        if intersection is None:
            intersection = zips
        else:
            intersection &= zips
    return sorted(intersection)


'''
For each file, group by ZIP and aggregate all numeric columns (sum).
Build a nested dict: { zip: { <file_base>: {<col>: value, ...} , ... } }
Only ZIPs in valid_zips are kept.
'''
def build_filled_zip_dict(valid_zips):
    zip_set = set(valid_zips)
    out = {z: {} for z in valid_zips}
    for fname, zcol in FILE_MAP.items():
        path = os.path.join(DATA_DIR, fname)
        df = load_csv(path, zcol)
        df = df[df[zcol].isin(zip_set)]
        num_cols = [c for c in df.select_dtypes(include="number").columns if c != zcol]
        agg_df = df.groupby(zcol, as_index=False)[num_cols].sum()
        base = os.path.splitext(fname)[0] 
        for _, row in agg_df.iterrows():
            z = row[zcol]
            out[z][base] = row.drop(labels=[zcol]).to_dict()
    return out

if __name__ == "__main__":
    print(cf.bold(cf.seaGreen('Creating zipcode data...')))
    # 1) Find intersection ZIPs (5-char strings) across all five files
    zipcode_intersection = find_zipcode_intersection()
    # 2) Build filled dictionary with values from each file
    filled = build_filled_zip_dict(zipcode_intersection)
    # 3) Save JSON next to your other artifacts
    out_path = os.path.join(DATA_DIR, "zipcodes.json")
    with open(out_path, "w") as f:
        json.dump(filled, f, indent=2)
    print(cf.bold(cf.seaGreen('Completed successfully')))
    print(cf.bold(cf.seaGreen(f"Saved data to: {out_path}")))
