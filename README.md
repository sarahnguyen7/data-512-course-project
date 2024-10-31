# data-512-course-project-part_1
# Wildfire Smoke Impact and AQI Analysis

## Project Goal
The goal of this project is to assess the impact of wildfire smoke on air quality in Gresham, OR, from 1961 to 2021 and forecast potential trends through 2050. Using geographic wildfire data, air quality data from the EPA’s AQS API, and time series modeling, we analyze how smoke impact correlates with AQI for particulate matter. Analysis can be found in `common_analysis.ipynb`.

## Table of Contents
1. [License](#license)
2. [Source Data](#source-data)
3. [API Documentation](#api-documentation)
4. [Data Files](#data-files)
5. [Data Schema](#data-schema)
6. [Known Issues](#known-issues)
7. [Special Considerations](#special-considerations)
8. [Instructions for Use](#instructions-for-use)
9. [Functions](#functions)
   

---
## Source Data
- **US EPA Air Quality System (AQS) API**: For air quality data on PM10 and PM2.5 pollutants.
- **[USGS Wildland Fire Dataset](https://www.sciencebase.gov/catalog/item/61aa537dd34eb622f699df81)**: Contains data on wildfires, including boundary coordinates, fire size, year, and more.


## License
The code written was developed in combination of myself, ChatGPT, Dr. David. W. McDonald for use in Data 512, a UW MS Data Science Degree program. The authors of the code will be referenced in the specifc code they were used in. Licenses for all are listed down below. 

#### Dr. David W. McDonald's Example Code
This code example was developed by Dr. David W. McDonald for use in DATA 512, a course in the UW MS Data Science degree program. This code is provided under the [Creative Commons](https://creativecommons.org) [CC-BY license](https://creativecommons.org/licenses/by/4.0/). Revision 1.3 - August 16, 2024

#### Sarah Nguyen's Code
This code was developed by Sarah Nguyen for use in DATA 512 homework, which is coursework provided under the [MIT License](https://chatgpt.com/c/67048ab0-3d24-8001-88ce-c354bb934b32#:~:text=under%20the%20MIT-,License,-.).

#### GPT-4
Portions of this project were assisted by GPT-4, an AI model by OpenAI.  These are indicated in the notebook and subject to Open AI's [Terms of Use](https://openai.com/policies/row-terms-of-use/). It was also used to help rewrite some of my documentation to help standardize format.

---

## API Documentation
This project uses the **EPA Air Quality System (AQS) API** to retrieve historical air quality data based on particulate matter, specifically PM2.5 and PM10, which are primary indicators of wildfire impact.

### Relevant API Endpoints:
- `dailyData/byCounty`: Retrieves daily AQI data by county.
- `list/parametersByClass`: Lists parameter codes for specific air quality measures (e.g., PM10, PM2.5).

### Key Parameters
- **State**: Oregon (FIPS code `41`)
- **County**: Multnomah County (FIPS code `051`)
- **Particulate Codes**:
  - PM10 Total 0-10µm (81102)
  - PM2.5 (88101)
  - Acceptable PM2.5 (88502)

For additional details on API usage, refer to the EPA AQS [API documentation](https://aqs.epa.gov/api).

---

## Data Files
### Input File:
1. **`USGS_Wildland_Fire_Combined_Dataset.json`**: Wildfire dataset (GeoJSON) containing fire attributes and boundary information.
   
### Output Files:
3. **`particulate_aqi_summary.csv`**: Contains annual AQI data for PM10 and PM2.5 pollutants in Gresham, OR.
4. **`updated__aqi_summary.csv`**: Contains the same information as `particulate_aqi_summary.csv` but includes the Max AQI for each year.
5. **`smoke_impact_estimates1.csv`**: Summary of annual smoke impact estimates per wildfire based on distance and acres burned.

### Output Tables located in `output_tables`:
6. **`AnnualAQIvsSmokeImpact.png`**: Contains a comparison of annual maximum AQI values and smoke impact estimates, both scaled for Gresham, OR. It is used to visualize the potential correlation between wildfire smoke and air quality levels in the area.
7. **`TotalAcresBurned.png`**: This time series plot shows the total acres burned by wildfires each year within a 650-mile radius of Gresham, OR. It provides insights into wildfire activity trends over time and helps assess potential long-term impacts on air quality.
8. **`HistogramofFireDistances1800.png`**: This histogram visualizes the number of wildfires occurring at various distances from Gresham, up to a maximum of 1800 miles, with bins spaced at 50-mile intervals. It highlights the distance distribution of wildfires, indicating which fires are close enough to impact air quality in Gresham, specifically marking the 650-mile cutoff used in the smoke impact model.

---

## Data Schema
### Wildfire Data (`USGS_Wildland_Fire_Combined_Dataset.json`)
- **Fire_Year**: Year of the wildfire
- **Listed_Fire_Names**: Name of the wildfire
- **GIS_Acres**: Acres burned by the wildfire
- **geometry**: Polygon boundary coordinates of the wildfire

### AQI Data (`particulate_aqi_summary.csv`)
- **Year**: Year of the data
- **PM10_AQI**: AQI for PM10 particles
- **PM2.5_AQI**: AQI for PM2.5 particles
- **Acceptable_PM2.5_AQI**: Adjusted AQI for PM2.5 based on air quality standards

### Smoke Impact Summary (`smoke_impact_estimates1.csv`)
- **Year**: Year of the wildfire
- **Fire_Name**: Name of the wildfire
- **Fire_Size_Acres**: Size of the wildfire in acres
- **Distance_to_City_Miles**: Distance from Gresham, OR to the wildfire perimeter
- **Smoke_Impact**: Calculated smoke impact based on distance and acres burned

---

## Known Issues
1. **Coordinate Transformation Errors**: Occasionally, some coordinates may not transform correctly due to missing or malformed geometry data. These instances are logged and skipped.
3. **Missing Years in AQI Data**: AQI Monitor's weren't required until 1973 and were not fully installed until around the 1980s. There is a lot of missing data for AQIs.
4. **Outliers in Smoke Impact**: Some wildfires, such as the Riverside Fire in 2020, create outliers in smoke impact, which may affect model stability and forecasting.
   
---

## Special Considerations
### Why the Inverse Square Law for Smoke Estimates? 
The [inverse square law](https://energyeducation.ca/encyclopedia/Inverse_square_law) was applied to calculate the smoke impact, which essentially means that as the distance from a fire increases, the smoke concentration decreases exponentially. This is similar to how light or sound spreads out from its source; the further you are, the more the impact fades. So, by using this law, we’re accounting for the drop in smoke concentration the further it travels, giving a more realistic impact estimate.

### Why PM2.5 and PM10? 
I specifically chose PM2.5 and PM10 as the core AQI parameters because these two are widely regarded as the best indicators of air quality impacts from wildfire smoke. PM2.5, especially, is a good gauge for smoke and can penetrate deeply into the lungs, affecting human health. Both parameters allow for a targeted look at the pollution type most associated with wildfire activity.

### Why Scale the Final Visualization? 
For the last visualization which involved comparing the annual AQI and the smoke impact, scaling both AQI and smoke impact helped us see trends together over time, making it easier to compare them on the same chart. Without scaling, the two datasets would be tough to view side by side since they naturally operate on very different value ranges.
   
---

## Instructions for Use
Python (3.8 or later): Ensure you have a compatible version of Python installed.

`pip install pyproj==3.4.1`

`pip install geojson==2.5.0`

`pip install matplotlib==3.6.2`

`pip install scikit-learn==1.1.3`

`pip install statsmodels==0.13.2`

---

## Functions

- `get_daily_aqi_for_particulates(start_year, end_year)`
Retrieves daily AQI data for PM2.5 and PM10 pollutants in Multnomah County, OR, from the AQS API. Returns a DataFrame with annual AQI summaries.

- `convert_ring_to_epsg4326(ring_data)`
Transforms ESRI:102008 coordinates in wildfire boundaries to EPSG:4326. Caches results for efficiency.

- `process_data_in_batches(reader, batch_size, max_distance)`
Processes wildfire data in batches, filtering by date and distance, and calculates smoke impact for each wildfire. 

   `calculate_smoke_impact(acres, distance)`
Calculates smoke impact based on acres burned and distance from Gresham, OR. Used to assess the severity of wildfire impacts on air quality.

---

