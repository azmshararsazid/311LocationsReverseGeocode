import pandas as pd
import requests
import json
import time

API_URL = "https://api.nyc.gov/arcgis/rest/services/NYC_OTI_Locator/GeocodeServer/reverseGeocode"
# IMPORTANT: Replace *** with your own API subscription key
# Instructions for obtaining a key are in the README
SUBSCRIPTION_KEY = "***"

HEADERS = {
    "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
    "Cache-Control": "no-cache",
}

FIELD_MAPPING = {
    "Assembly District": "ASSEMBLYDISTRICT",
    "Borough": "City",
    "Census Block": "CENSUSBLOCK_2020",
    "Census Tract": "CENSUSTRACT_2020",
    "City": "City",
    "Community District": "COMMUNITYDISTRICT",
    "Congressional District": "CONGRESSIONALDISTRICT",
    "Council District": "CITYCOUNCILDISTRICT",
    "Court District": "CIVILCOURTDISTRICT",
    "Election District": "ELECTIONDISTRICT",
    "Fire Battalion": "FIREBATTALION",
    "Fire Company": "FIRECOMPANYNUMBER",
    "Fire Company Type": "FIRECOMPANYTYPE",
    "Health Area": "HEALTHAREA",
    "Health Center District": "HEALTHCENTERDISTRICT",
    "ID": "SEGMENTID",
    "Latitude": "InputY",
    "Longitude": "InputX",
    "Police Borough Command": "PATROLBOROUGHCOMMAND",
    "Police Precinct": "PRECINCT",
    "Police Sector": "NYPD_SECTOR",
    "School District": "COMMUNITYSCHOOLDISTRICT",
    "State Senatorial District": "STATESENATORIALDISTRICT",
    "X Coordinate": "X",
    "Y Coordinate": "Y",
    "Zip Code": "Postal",
}

def reverse_geocode(lat, lon):
    location = json.dumps({
        "x": lon,
        "y": lat,
        "spatialReference": {"wkid": 4326}
    })
    params = {
        "location": location,
        "outSR": json.dumps({"wkid": 4326}),
        "outFields": "*",
        "f": "json",
    }
    try:
        resp = requests.get(API_URL, params=params, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if "error" in data:
            print(f"  API error for ({lat}, {lon}): {data['error']}")
            return {}
        attrs = data.get("address", {})
        loc = data.get("location", {})
        
        result = {
            "Longitude": loc.get("x"),
            "Latitude": loc.get("y"),
        }
        
        for output_field, api_field in FIELD_MAPPING.items():
            if api_field is None:
                result[output_field] = None
            else:
                result[output_field] = attrs.get(api_field)
        
        return result
    except Exception as e:
        print(f"  Request failed for ({lat}, {lon}): {e}")
        return {}

def main():
    hl = pd.read_csv(r"311HL.csv", encoding="cp1252") #change 311HL to what is needed r"C:\Users\USER\311Solvedv2.csv"
    print(f"Loaded {len(hl)} rows from 311HL.csv")
    print(f"Columns: {list(hl.columns)}")

    results = []
    for i, row in hl.iterrows():    #Main loop
        lat = row["Latitude"]    #Reads the Latitude column and assigns it to y
        lon = row["Longitude"]   #Reads the Longitude column and assigns it to x
        print(f"[{i+1}/{len(hl)}] Geocoding ({lat}, {lon})...")
        geocoded = reverse_geocode(lat, lon)
        
        record = {col: row.get(col) for col in hl.columns}
        
        for output_field in FIELD_MAPPING.keys():
            record[output_field] = geocoded.get(output_field)
        
        results.append(record)
        time.sleep(0.1)

    out_df = pd.DataFrame(results)
    out_path = "311Solvedv2.csv" #change 311Solvedv2 to what is needed such as: r"C:\Users\USER\311Solvedv2.csv"
    out_df.to_csv(out_path, index=False)
    print(f"\nDone. Results saved to {out_path}")

if __name__ == "__main__":
    main()
