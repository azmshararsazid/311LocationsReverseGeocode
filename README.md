# NYC 311 Reverse Geocoder

Queries the NYC OTI Locator API for latitude/longitude coordinates and returns administrative boundaries.

## Getting Your NYC OTI Locator API Key

1. **Visit the NYC API Portal**
   - Go to https://api-portal.nyc.gov

2. **Sign Up or Sign In**
   - Click "Sign up" to create a new account, or "Sign in" if you already have one

3. **Subscribe to NYC OTI Locator**
   - Navigate to the Products section
   - Find and click on "NYC OTI Locator User"
   - Click "Subscribe" to add it to your subscriptions
   - Enter a name for your subscription (e.g., "311 Geocoding")

4. **Get Your API Key**
   - Once subscribed, go to your Profile (top right)
   - Under Subscriptions, find your "NYC OTI Locator" subscription
   - Click "Show" next to "Primary key" to reveal your API key
   - Copy this key

5. **Update the Script**
   - Open `311reversegeocode.py`
   - Replace the `***` in the SUBSCRIPTION_KEY variable with your copied key:
     ```python
     SUBSCRIPTION_KEY = "your_key_here"
     ```

**Note:** Keep your API key private and do not share it publicly.

## Configuration

Your CSV must have columns named exactly: `Latitude` and `Longitude` if not, see below.

Modify these variables in `311reversegeocode.py` as needed:

- `INPUT_CSV = r"your_file.csv"` for input path (line 17 in `311reversegeocode.py`).
- `OUTPUT_CSV = r"your_output.csv"` for output path (line 18 in `311reversegeocode.py`).
- `INPUT_ENCODING = "cp1252"` (or `"utf-8"` for many Google Sheets/Mac exports) (line 19 in `311reversegeocode.py`).
- If your coordinate columns are not named `Latitude` and `Longitude`, update these lines in `main()`:
   - `lat = row["Latitude"]` (line 95 in `311reversegeocode.py`)
   - `lon = row["Longitude"]` (line 96 in `311reversegeocode.py`)

Run with:

```bash
python 311reversegeocode.py
```

## Troubleshooting

- **`KeyError: 'Latitude'` or `'Longitude'`** - Column name doesn't match (case-sensitive). Update the `lat = row[...]` and `lon = row[...]` lines in `main()`.
- **`ModuleNotFoundError: pandas`** - Run `pip install pandas requests`
- **Script runs slow** - The 0.1s delay per request is normal (prevents API rate limit).
- **Blank geocoded fields in output** - Coordinates may be outside NYC or invalid.

## Output

Original columns + 26 new geocoded fields. Failed rows have blank geocoded fields.

## If Needed: Change in FIELD_MAPPING

```python
# Fields not available in API:
# "Fire Division": None  # Not available in API
# "Instructional Region": None  # Not available in API
# "Lines": None  # Not available in API
# "Lines Filter": None  # Not available in API
# "Lines Filter Query": None  # Not available in API
# "Name Alias": None  # Not available in API
# "Parent": None  # Not available in API
# "Parent Unique ID": None  # Not available in API
# "Record Created On": None  # Not available in API
# "Record Type": None  # Not available in API
# "Sequence": None  # Not available in API
# "Status": None  # Not available in API
# "Status Reason": None  # Not available in API
# "Transit District": None  # Not available in API

# Fields in API but not requested by 311:
# "?": "ADDRESSPOINTID"  # is in API but not requested by 311
# "?": "ADDRESSUNIQUEID"  # is in API but not requested by 311
# "?": "AS_ED"  # is in API but not requested by 311
# "?": "AddNum"  # is in API but not requested by 311
# "?": "Addr_type"  # is in API but not requested by 311
# "?": "Address"  # is in API but not requested by 311
# "?": "B10SC_STREETCODE"  # is in API but not requested by 311
# "?": "B7SC_STREETCODE"  # is in API but not requested by 311
# "?": "BBL"  # is in API but not requested by 311
# "?": "BIN"  # is in API but not requested by 311
# "?": "BLDGCLASS"  # is in API but not requested by 311
# "?": "Block"  # is in API but not requested by 311
# "?": "CENSUSBLOCK_2010"  # is in API but not requested by 311
# "?": "CENSUSTRACT_2010"  # is in API but not requested by 311
# "?": "CONDONO"  # is in API but not requested by 311
# "?": "CntryName"  # is in API but not requested by 311
# "?": "CountryCode"  # is in API but not requested by 311
# "?": "DSNY_BULK_SCHEDULE"  # is in API but not requested by 311
# "?": "DSNY_DISTRICT"  # is in API but not requested by 311
# "?": "DSNY_ORGANIC_SCHEDULE"  # is in API but not requested by 311
# "?": "DSNY_RECYCLING_SCHEDULE"  # is in API but not requested by 311
# "?": "DSNY_SECTIONANDSUBSECTION"  # is in API but not requested by 311
# "?": "DSNY_TRASH_SCHEDULE"  # is in API but not requested by 311
# "?": "District"  # is in API but not requested by 311
# "?": "FROM_CROSS_STREETS"  # is in API but not requested by 311
# "?": "GCUID"  # is in API but not requested by 311
# "?": "HURRICANE_EVACUATION_ZONE"  # is in API but not requested by 311
# "?": "LongLabel"  # is in API but not requested by 311
# "?": "Match_addr"  # is in API but not requested by 311
# "?": "MetroArea"  # is in API but not requested by 311
# "?": "NTA_NAME"  # is in API but not requested by 311
# "?": "NYCHA_DEVELOPMENTNAME"  # is in API but not requested by 311
# "?": "NYCHA_TDS_NUM"  # is in API but not requested by 311
# "?": "NYPD_PSA"  # is in API but not requested by 311
# "?": "Neighborhood"  # is in API but not requested by 311
# "?": "POIUNIQUEID"  # is in API but not requested by 311
# "?": "PRIMARY_STREETNAME"  # is in API but not requested by 311
# "?": "PlaceName"  # is in API but not requested by 311
# "?": "PostalExt"  # is in API but not requested by 311
# "?": "RELEASEID"  # is in API but not requested by 311
# "?": "Region"  # is in API but not requested by 311
# "?": "RegionAbbr"  # is in API but not requested by 311
# "?": "SEGMENTID_ORIG"  # is in API but not requested by 311
# "?": "Sector"  # is in API but not requested by 311
# "?": "ShortLabel"  # is in API but not requested by 311
# "?": "Subregion"  # is in API but not requested by 311
# "?": "TO_CROSS_STREETS"  # is in API but not requested by 311
# "?": "Territory"  # is in API but not requested by 311
# "?": "Type"  # is in API but not requested by 311
```
