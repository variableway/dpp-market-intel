# UN Comtrade API Research: China-EU Bilateral Trade Data by HS Code

## 1. API Endpoint URL and Authentication

### Base URL
```
https://comtradeapi.un.org/data/v1/comtrade/final/get
```

### Authentication
- **Header name**: `Ocp-Apim-Subscription-Key`
- **How to obtain**:
  1. Register for a free account at [https://comtradeplus.un.org/](https://comtradeplus.un.org/)
  2. Go to the API Developer Portal at [https://comtradedeveloper.un.org/](https://comtradedeveloper.un.org/)
  3. Sign in and subscribe to the free API plan
  4. You will receive an `Ocp-Apim-Subscription-Key`
- The key can be passed either as an HTTP header or as a query parameter `subscription-key=YOUR_KEY`

### Official Python Library
```bash
pip install comtradeapicall
```
- GitHub: [https://github.com/uncomtrade/comtradeapicall](https://github.com/uncomtrade/comtradeapicall)
- Version: 1.3.0

---

## 2. Querying China-EU Bilateral Trade Data by HS Code

### Key Parameters (Selection Criteria)

| Parameter | Description | Example Values |
|-----------|-------------|----------------|
| `typeCode` | Product type | `C` (Goods), `S` (Services) |
| `freqCode` | Frequency | `A` (Annual), `M` (Monthly) |
| `clCode` | Classification system | `HS` (Harmonized System) |
| `period` | Time period | `2024` (annual), `202401` (monthly) |
| `reporterCode` | Country reporting trade | `156` (China) |
| `partnerCode` | Trade partner country | `276` (Germany), `250` (France), etc. |
| `cmdCode` | Commodity/HS code | `TOTAL`, `85` (chapter), `851712` (subheading), `AG2`,`AG4`,`AG6` (aggregates) |
| `flowCode` | Trade flow direction | `M` (Import), `X` (Export), `RX` (Re-export), `RM` (Re-import) |
| `partner2Code` | Secondary partner | Usually `None` |
| `customsCode` | Customs procedure | Usually `None` |
| `motCode` | Mode of transport | Usually `None` |

### Query Options

| Parameter | Description | Example |
|-----------|-------------|---------|
| `maxRecords` | Max records returned | 500 (preview), up to 250,000 (authenticated) |
| `format_output` | Output format | `JSON`, `CSV` |
| `aggregateBy` | Aggregation option | `None`, or field name |
| `breakdownMode` | Breakdown mode | `classic` (by partner/product), `plus` (extended) |
| `countOnly` | Return count only | `True`, `False` |
| `includeDesc` | Include descriptions | `True`, `False` |

### Flow Code Values

| Code | Meaning |
|------|---------|
| `M` | Import |
| `X` | Export |
| `RM` | Re-import |
| `RX` | Re-export |
| `DX` | Domestic Export |

### China Country Code
- **M49/UN Code**: `156`
- **ISO Alpha-3**: `CHN`

### EU Member State Codes (27 members)

| Country | Code | ISO | Country | Code | ISO |
|---------|------|-----|---------|------|-----|
| Austria | 40 | AUT | Latvia | 428 | LVA |
| Belgium | 56 | BEL | Lithuania | 440 | LTU |
| Bulgaria | 100 | BGR | Luxembourg | 442 | LUX |
| Croatia | 191 | HRV | Malta | 470 | MLT |
| Cyprus | 196 | CYP | Netherlands | 528 | NLD |
| Czechia | 203 | CZE | Poland | 616 | POL |
| Denmark | 208 | DNK | Portugal | 620 | PRT |
| Estonia | 233 | EST | Romania | 642 | ROU |
| Finland | 246 | FIN | Slovakia | 703 | SVK |
| France | 250 | FRA | Slovenia | 705 | SVN |
| Germany | 276 | DEU | Spain | 724 | ESP |
| Greece | 300 | GRC | Sweden | 752 | SWE |
| Hungary | 348 | HUN | Ireland | 372 | IRL |
| Italy | 380 | ITA | | | |

> **Important**: There is no single "EU27" aggregate code for partner queries. You must query each EU member individually or use specific aggregate area codes if available. Check [comtradeplus.un.org/ListOfReferences](https://comtradeplus.un.org/ListOfReferences) for any available EU aggregate codes.

### HS Code Structure
- **2 digits**: Chapter (e.g., `85` = Electrical machinery)
- **4 digits**: Heading (e.g., `8517` = Telephone sets)
- **6 digits**: Subheading (e.g., `851712` = Telephones for cellular networks)
- **Aggregate codes**: `AG1`, `AG2`, `AG4`, `AG6` (aggregate by 1-digit, 2-digit, 4-digit, 6-digit HS level)
- **`TOTAL`**: All commodities combined
- Multiple codes can be comma-separated: `cmdCode='85,84'`

---

## 3. Rate Limits and Data Availability

### Rate Limits

| Tier | Calls/Day | Records/Call | Cost |
|------|-----------|--------------|------|
| **Free** | 500 | 100,000 | Free |
| **Premium** | Higher limits | Up to 250,000 per call | Paid subscription |

### Preview (No Auth) Limits
- `previewFinalData`: Max 500 records per call, no subscription key needed
- `previewTarifflineData`: Max 500 records per call, no subscription key needed

### Authenticated Limits
- `getFinalData`: Max 250,000 records per call
- `getTarifflineData`: Max 250,000 records per call
- Async download: Up to 2.5 million records

### Data Availability (2024/2025)
- **2024 data**: Partially available for some countries. China 2024 annual data has been spotted in direct query URLs.
- **2025 data**: Likely NOT yet available in annual form. Annual data is typically reported with significant lag.
- There is **no fixed schedule** for data releases -- data appears as national statistical authorities submit it.
- Check [comtradeplus.un.org/DataAvailability](https://comtradeplus.un.org/DataAvailability) for the latest availability by country and year.
- Use `getFinalDataAvailability()` or `getLiveUpdate()` functions to programmatically check availability.

### HS Classification Versions
- Available: HS1992, HS1996, HS2002, HS2007, HS2012, HS2017, HS2022
- Use `clCode='HS'` for the latest applicable version

---

## 4. Example API Calls for China-EU Import/Export Data

### Example 1: Raw HTTP Request -- China exports to Germany, annual 2024, all HS chapters
```
GET https://comtradeapi.un.org/data/v1/comtrade/final/get?typeCode=C&freqCode=A&clCode=HS&period=2024&reporterCode=156&partnerCode=276&cmdCode=TOTAL&flowCode=X
Header: Ocp-Apim-Subscription-Key: YOUR_KEY
```

### Example 2: Python (comtradeapicall) -- China exports to Germany by HS 2-digit chapter
```python
import comtradeapicall

mydf = comtradeapicall.getFinalData(
    subscription_key='YOUR_KEY',
    typeCode='C',
    freqCode='A',
    clCode='HS',
    period='2024',
    reporterCode='156',       # China
    partnerCode='276',        # Germany
    cmdCode='AG2',            # Aggregate by 2-digit HS chapter
    flowCode='X',             # Export
    partner2Code=None,
    customsCode=None,
    motCode=None,
    maxRecords=25000,
    format_output='JSON',
    aggregateBy=None,
    breakdownMode='classic',
    countOnly=None,
    includeDesc=True
)
```

### Example 3: Preview (no auth) -- China imports from Germany, limited to 500 records
```python
mydf = comtradeapicall.previewFinalData(
    typeCode='C',
    freqCode='A',
    clCode='HS',
    period='2023',
    reporterCode='156',
    partnerCode='276',
    cmdCode='AG2',
    flowCode='M',             # Import
    partner2Code=None,
    customsCode=None,
    motCode=None,
    maxRecords=500,
    format_output='JSON',
    aggregateBy=None,
    breakdownMode='classic',
    countOnly=None,
    includeDesc=True
)
```

### Example 4: Raw HTTP with requests library
```python
import requests

url = "https://comtradeapi.un.org/data/v1/comtrade/final/get"
headers = {"Ocp-Apim-Subscription-Key": "YOUR_KEY"}
params = {
    "typeCode": "C",
    "freqCode": "A",
    "clCode": "HS",
    "period": "2024",
    "reporterCode": "156",     # China
    "partnerCode": "276",      # Germany
    "cmdCode": "AG2",          # HS 2-digit chapters
    "flowCode": "X",           # Export
    "maxRecords": 25000,
    "format_output": "JSON",
    "breakdownMode": "classic",
    "includeDesc": "true"
}
response = requests.get(url, headers=headers, params=params)
data = response.json()
```

### Example 5: Loop through all EU27 countries
```python
import comtradeapicall
import pandas as pd

eu_countries = [
    '40',   # Austria
    '56',   # Belgium
    '100',  # Bulgaria
    '191',  # Croatia
    '196',  # Cyprus
    '203',  # Czechia
    '208',  # Denmark
    '233',  # Estonia
    '246',  # Finland
    '250',  # France
    '276',  # Germany
    '300',  # Greece
    '348',  # Hungary
    '372',  # Ireland
    '380',  # Italy
    '428',  # Latvia
    '440',  # Lithuania
    '442',  # Luxembourg
    '470',  # Malta
    '528',  # Netherlands
    '616',  # Poland
    '620',  # Portugal
    '642',  # Romania
    '703',  # Slovakia
    '705',  # Slovenia
    '724',  # Spain
    '752',  # Sweden
]

all_data = []
for partner in eu_countries:
    df = comtradeapicall.getFinalData(
        subscription_key='YOUR_KEY',
        typeCode='C',
        freqCode='A',
        clCode='HS',
        period='2024',
        reporterCode='156',     # China
        partnerCode=partner,
        cmdCode='AG2',          # HS 2-digit chapters
        flowCode='X',           # Export
        partner2Code=None,
        customsCode=None,
        motCode=None,
        maxRecords=25000,
        format_output='JSON',
        aggregateBy=None,
        breakdownMode='classic',
        countOnly=None,
        includeDesc=True
    )
    all_data.append(df)
    # Respect rate limits -- 500 calls/day on free tier

result = pd.concat(all_data, ignore_index=True)
```

### Example 6: Check data availability before querying
```python
import comtradeapicall

# Check what data China has reported for annual 2024
availability = comtradeapicall.getFinalDataAvailability(
    subscription_key='YOUR_KEY',
    typeCode='C',
    freqCode='A',
    clCode='HS',
    period='2024',
    reporterCode='156'    # China
)
print(availability)

# Check recent releases
releases = comtradeapicall.getLiveUpdate(subscription_key='YOUR_KEY')
print(releases)
```

### Example 7: Bilateral comparison (mirror data)
```python
# Compare China's reported exports with EU countries' reported imports
mydf = comtradeapicall.getBilateralData(
    subscription_key='YOUR_KEY',
    typeCode='C',
    freqCode='A',
    clCode='HS',
    period='2024',
    reporterCode='156',      # China
    cmdCode='TOTAL',
    flowCode='X',            # Export
    partnerCode=None         # All partners
)
```

### Example 8: Convert ISO codes to Comtrade codes
```python
import comtradeapicall

# Convert ISO alpha-3 codes to UN Comtrade numeric codes
codes = comtradeapicall.convertCountryIso3ToCode('CHN,DEU,FRA,ITA,ESP,NLD')
print(codes)
```

---

## 5. Free Tier Details

| Feature | Free Tier |
|---------|-----------|
| **Registration** | Free at comtradeplus.un.org |
| **API Key** | Provided upon registration |
| **Daily API Calls** | 500 calls/day |
| **Records per Call** | Up to 100,000 |
| **Preview (no auth)** | 500 records max |
| **Data Access** | All publicly available trade data |
| **Bulk Download** | Premium only |
| **Async Download** | Premium only |

### Premium Features (Paid)
- Higher daily call limits
- Bulk file download
- Async batch processing (up to 2.5M records)
- Priority access

---

## 6. Key Reference Links

| Resource | URL |
|----------|-----|
| UN Comtrade+ Portal | [comtradeplus.un.org](https://comtradeplus.un.org/) |
| API Developer Portal | [comtradedeveloper.un.org](https://comtradedeveloper.un.org/) |
| Data Availability | [comtradeplus.un.org/DataAvailability](https://comtradeplus.un.org/DataAvailability) |
| Parameter References | [comtradeplus.un.org/ListOfReferences](https://comtradeplus.un.org/ListOfReferences) |
| Official Python Library | [github.com/uncomtrade/comtradeapicall](https://github.com/uncomtrade/comtradeapicall) |
| R Package | [docs.ropensci.org/comtradr](https://docs.ropensci.org/comtradr/) |
| Methodology Guide (PDF) | [MethodologyGuideforComtradePlus.pdf](https://comtradeapi.un.org/files/v1/app/wiki/MethodologyGuideforComtradePlus.pdf) |
| Data Items Reference (Excel) | [ComtradePlus_DataItems.xlsx](https://comtradeapi.un.org/files/v1/app/wiki/ComtradePlus_DataItems.xlsx) |
| M49 Country Codes | [unstats.un.org/unsd/methodology/m49](https://unstats.un.org/unsd/methodology/m49/) |
| HS Classifications | [unstats.un.org/unsd/trade/dataextract/dataclass.htm](https://unstats.un.org/unsd/trade/dataextract/dataclass.htm) |

---

## 7. Summary and Recommendations for DPP Market Intel Project

### Feasibility Assessment
- **Data source**: UN Comtrade is the authoritative source for bilateral trade data by HS code
- **Free tier is sufficient** for periodic data pulls (500 calls/day covers all 27 EU countries with room to spare)
- **Recommended approach**:
  1. Register for free API key
  2. Query China (reporter=156) exports (flowCode=X) to each EU27 partner
  3. Use `AG2` or `AG4` for HS chapter/heading level aggregation
  4. Fall back to 2023 data if 2024 is not yet available for China
  5. Use bilateral comparison (`getBilateralData`) for data validation

### Rate Limit Strategy
- 27 EU countries x 2 flows (import/export) = 54 calls per year's data
- Well within the 500 calls/day free tier limit
- Can retrieve multiple years in a single day

### Data Freshness Consideration
- Annual trade data typically has 12-18 month reporting lag
- 2024 data may be partially available; 2025 almost certainly not yet
- Use `getFinalDataAvailability()` to check before querying
