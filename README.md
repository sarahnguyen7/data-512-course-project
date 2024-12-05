# data-512-course-project
# Wildfire Smoke Impact and AQI Analysis

## Project Goal
### Updated Project Goals and Purpose of Analysis

The project initially focused on assessing the impact of wildfire smoke on air quality in Gresham, OR, from 1961 to 2021, with the aim of forecasting potential trends through 2050. This phase of the analysis was divided into three notebooks to enhance modularity and clarity:

- **`common_analysis_pt1A_smoke_estimate.ipynb`**: This notebook calculates the annual smoke impact from wildfires using geographic wildfire data from the USGS Wildland Fire Dataset. It applies the inverse square law to quantify smoke dispersion based on fire size and proximity to Gresham, providing a foundational estimate of smoke's local impact.
  
- **`common_analysis_pt1B_AQI.ipynb`**: This notebook examines the relationship between the calculated smoke impact and air quality data (PM2.5 and PM10) from the EPA’s AQS API. It analyzes historical trends in air quality to assess how wildfire smoke has affected particulate matter levels over time.

- **`common_analysis_pt1C_forecasting_and_visualizations.ipynb`**: This notebook uses time-series forecasting with Prophet to project future smoke impact and associated air quality trends through 2050. It also includes visualizations to summarize historical and forecasted trends.

### Expanding the Scope to Respiratory Mortality

Following the initial analysis on smoke impact and air quality, the project expanded its scope to explore the relationship between wildfire smoke and **respiratory mortality** in Gresham, OR. This analysis was carried out in two distinct notebooks, ensuring a structured and systematic approach to handling the data and modeling tasks:

- **`social_impact_preprocessing.ipynb`**: This notebook focused on preparing the data necessary for forecasting trends in respiratory mortality. It included:
  - **IHME Data Integration**: Extracting respiratory mortality rates (1980–2014) for Multnomah County and filtering relevant diseases linked to PM2.5 and PM10 exposure, such as COPD and interstitial lung diseases.
  - **Population Data Processing**: Using population data from FRED to convert mortality rates into absolute annual mortality counts for accurate trend analysis.
  - **Data Cleaning**: Resolving missing values and aligning mortality data with annual smoke impact estimates.

- **`social_impact_execution.ipynb`**: This notebook implemented the analysis and forecasting:
  - **Correlation Analysis**: Performed Pearson correlation to identify respiratory illnesses most affected by wildfire smoke, showing strong positive correlations for conditions like COPD, chronic respiratory diseases, and interstitial lung diseases.
  - **Forecasting**: Using Prophet & linear regression, trends in respiratory mortality were forecasted for 2025–2050 based on historical data and smoke impact estimates.
  - **Visualization**: Generated clear and interpretable charts to present historical trends and forecasted outcomes for respiratory mortality, highlighting critical insights.

NOTE: Steps to reproduce each notebook are written in the markdown of the notebook. Begin in the order you see here, starting with `common_analysis_pt1A_smoke_estimate.ipynb`, working your way up to `common_analysis_pt1C_forecasting_and_visualizations.ipynb`. If you only want to do wildfire analysis, do not do the extension analysis. 
For extension analysis, begin with `social_impact_preprocessing.ipynb`.

These analyses collectively serve as a foundation for crafting actionable recommendations for public health and wildfire mitigation strategies in Gresham, OR.

At the beginning of this project, I aimed to answer two main research questions: What is the future smoke impact of wildfires based on historical data? How does this smoke impact affect respiratory mortality in Gresham, Oregon? Through my analysis, I found that both wildfire smoke impact and respiratory mortality rates are expected to rise significantly by 2050. Chronic respiratory diseases, COPD, and interstitial lung disease showed the strongest correlations with smoke exposure, highlighting the serious public health risks that wildfires pose to the region.

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
```
DATA-512-COURSE-PROJECT
│
├── input_data/                # Raw data files
│   ├── IHME_USA_COUNTY_RESP_DISEASE_MORTALITY.csv
│   ├── ORMULT1POP.csv
│   ├── wildfire/              # Subdirectory for wildfire-related scripts and data
│   │   ├── __init__.py
│   │   ├── Reader.py
│
├── intermediary_files/        # Intermediate data processing outputs
│   ├── particulate_aqi_summary.csv
│   ├── smoke_impact_estimates1.csv
│   ├── updated_aqi_summary.csv
│
├── output_files/              # Final output files (visualizations, forecasts)
│   ├── AnnualAQIvsSmokeImpact.png
│   ├── ChronicRespiratoryMortalityForecast.png
│   ├── CorrelationAnalysis_RespiratoryvsSmoke.png
│   ├── HistogramofFireDistances1800.png
│   ├── SmokeImpactForecast.png
│   ├── TotalAcresBurned.png
│
├── wildfire/                  # Scripts related to wildfire data handling
│   ├── __init__.py
│   ├── Reader.py
│
├── writeup_reports/           # Reports and write-ups for analysis
│   ├── Common_Analysis_Write_Up.pdf
│   ├── Final_Report.pdf
│
├── LICENSE                    # Project license
├── README.md                  # Project overview
│
├── common_analysis_pt1A_smoke_estimate.ipynb
├── common_analysis_pt1B_AQI_.ipynb
├── common_analysis_pt1C_forecasting_and_plots.ipynb
├── social_impact_execution.ipynb  # Execution-related notebook
├── social_impact_preprocessing.ipynb  # Preprocessing-related notebook
```

## Source Data
#### **US EPA Air Quality System (AQS) API**
- **Description**: Provides historical air quality data, including measurements for pollutants such as PM2.5 and PM10. Data was used to correlate smoke impacts with air quality trends in Gresham, OR.
- **Terms of Use**: The data is publicly accessible and provided by the U.S. Environmental Protection Agency. Users must adhere to their **[API Terms of Use](https://aqs.epa.gov/aqsweb/documents/data_api_terms_of_use.html)**, which outline restrictions on commercial use and emphasize proper attribution in research and applications.

#### **[USGS Wildland Fire Dataset](https://www.sciencebase.gov/catalog/item/61aa537dd34eb622f699df81)**
- **Description**: A comprehensive dataset of U.S. wildfires, containing attributes like boundary coordinates, fire size, year, and origin. Used to calculate smoke impacts by estimating the distance and intensity of wildfires affecting Gresham, OR.
Note: The data was too big for GitHub so it was removed. Add it back into wildfire.
- **Terms of Use**: This dataset is part of the public domain as provided by the U.S. Geological Survey (USGS). Users are encouraged to cite the source when using or sharing the data, as outlined in their **[data policies](https://www.usgs.gov/about/organization/science-support/science-analytics-and-synthesis/policies-and-notices)**.

#### **[IHME USA County-Level Mortality Dataset](https://ghdx.healthdata.org/record/ihme-data/united-states-chronic-respiratory-disease-mortality-rates-county-1980-2014)**
- **Description**: Chronic respiratory disease mortality rates by county from 1980–2014, provided by the Institute for Health Metrics and Evaluation (IHME). This dataset was filtered for Multnomah County to assess respiratory mortality linked to wildfire smoke.
- **Terms of Use**: Available under the **[IHME Free-of-Charge Non-Commercial User Agreement](https://ghdx.healthdata.org/data-terms-use)**. The data can be used, shared, or modified for non-commercial purposes, provided proper attribution is given.

#### **[Federal Reserve Economic Data (FRED)](https://alfred.stlouisfed.org/series?seid=ORMULT1POP)**
- **Description**: Provides population data for Multnomah County, used to calculate actual mortality counts from the IHME mortality rate data.
- **Terms of Use**: FRED data is free for educational and non-commercial use. Users must comply with the **[FRED® Terms of Use](https://fred.stlouisfed.org/legal)**, ensuring proper attribution when integrating their data into research or projects.

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
   
### Intermediary Files:
3. **`particulate_aqi_summary.csv`**: Contains annual AQI data for PM10 and PM2.5 pollutants in Gresham, OR.
4. **`updated__aqi_summary.csv`**: Contains the same information as `particulate_aqi_summary.csv` but includes the Max AQI for each year.
5. **`smoke_impact_estimates1.csv`**: Summary of annual smoke impact estimates per wildfire based on distance and acres burned.

### Output Files located in `output_files`:
6. **`TotalAcresBurned.png`**: This time series plot shows the total acres burned by wildfires each year within a 650-mile radius of Gresham, OR. It provides insights into wildfire activity trends over time and helps assess potential long-term impacts on air quality.
7. **`HistogramofFireDistances1800.png`**: This histogram visualizes the number of wildfires occurring at various distances from Gresham, up to a maximum of 1800 miles, with bins spaced at 50-mile intervals. It highlights the distance distribution of wildfires, indicating which fires are close enough to impact air quality in Gresham, specifically marking the 650-mile cutoff used in the smoke impact model.
8. **`AnnualAQIvsSmokeImpact.png`**: Contains a comparison of annual maximum AQI values and smoke impact estimates, both scaled for Gresham, OR. It is used to visualize the potential correlation between wildfire smoke and air quality levels in the area.
9. **` SmokeImpactForecast.png`**: This visualization presents the forecasted smoke impact trends for Gresham, OR, from 2025 to 2050, based on historical data. It includes confidence intervals to indicate the range of possible outcomes, helping stakeholders understand future risks and uncertainties.

10. **` ChronicRespiratoryMortalityForecast.png`** This time series plot shows forecasted mortality rates for chronic respiratory diseases, such as COPD and interstitial lung disease, from 2025 to 2050. It illustrates the projected health impact of increasing wildfire smoke exposure on Gresham’s population.

11. **` CorrelationAnalysis_RespiratoryvsSmoke.png`**: This scatterplot matrix displays Pearson correlation results between wildfire smoke impact and respiratory mortality rates for specific illnesses. It helps identify the diseases most closely associated with smoke exposure, such as chronic respiratory disease and COPD, offering valuable insights for targeted public health interventions.


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
For the common_analysis portion:
1. **Coordinate Transformation Errors**: Occasionally, some coordinates may not transform correctly due to missing or malformed geometry data. These instances are logged and skipped.
3. **Missing Years in AQI Data**: AQI Monitor's weren't required until 1973 and were not fully installed until around the 1980s. There is a lot of missing data for AQIs.
4. **Outliers in Smoke Impact**: Some wildfires, such as the Riverside Fire in 2020, create outliers in smoke impact, which may affect model stability and forecasting.

For the social impact extension:

   
---

## Special Considerations
### Why the Inverse Square Law for Smoke Estimates? 
To create the smoke estimate/impact of wildfire smoke on Gresham, Oregon, I applied the [inverse square law](https://energyeducation.ca/encyclopedia/Inverse_square_law)), a principle that models how intensity decreases as distance from a source increases. Similar to how light or sound diminishes as it spreads outward, wildfire smoke disperses as it travels further from its source, resulting in lower concentrations at greater distances. By incorporating this principle, the smoke estimate accounts for the physical reality of dispersion, providing a more realistic measure of smoke intensity in Gresham.

For example:
A fire burning 10 miles away from Gresham will have a far greater impact than a similarly sized fire burning 100 miles away.
Larger fires, regardless of distance, contribute more smoke to the overall impact. For instance, a fire burning 1,000 acres at 50 miles will still contribute significantly compared to a smaller 50-acre fire at the same distance.
Formula and Calculation
The formula I used for the smoke estimate is:

Smoke Impact = Acres Burned / (Distance from Gresham)^2


Variables:
Acres Burned: Larger wildfires release more smoke, which increases their potential impact on air quality.
Distance from Fire: As smoke travels farther from the fire, it disperses and loses intensity. Squaring the distance emphasizes this dispersion effect, as smoke at twice the distance will have only a quarter of the impact.
This formula was applied to every wildfire occurring within 650 miles of Gresham, capturing both nearby and distant fires that might affect the city. For each fire, I calculated its individual smoke impact and then aggregated these values across all fires within a given year to obtain the annual smoke impact.
Why Use the Inverse Square Law?
While advanced atmospheric models like HYSPLIT or BlueSky account for meteorological factors (like wind direction, topography), these require extensive computational resources and meteorological data, which were not feasible time-wise or available for this study. The inverse square law offers a straightforward estimate of smoke dispersion based on the size of the fire and its distance from the city. This method ensures that both proximity and fire size are appropriately weighted, aligning the model with how smoke physically spreads through the atmosphere. By aggregating the annual impacts, the model captures year-to-year variations in wildfire activity and provides a robust measure of smoke exposure for trend analysis given the data and time we had for the project.
Data Processing and Integration
To ensure accurate results, wildfire data was preprocessed as follows:
Coordinate Transformation: Fire polygons from the ScienceBase dataset were converted from the ESRI:102008 coordinate system to EPSG:4326 (decimal degrees). This enabled consistent distance calculations between fire locations and Gresham.
Distance Calculations: Distances between each wildfire and Gresham were calculated in decimal degrees, using Gresham's geographic coordinates as the reference point.
Annual Aggregation: Once the smoke impact for each fire was calculated, impacts were summed across all wildfires in a year to produce the total annual smoke impact.


### Why PM2.5 and PM10? 
I specifically chose PM2.5 and PM10 as the core AQI parameters because these two are widely regarded as the best indicators of air quality impacts from wildfire smoke. PM2.5, especially, is a good gauge for smoke and can penetrate deeply into the lungs, affecting human health. Both parameters allow for a targeted look at the pollution type most associated with wildfire activity.

### Why Scale the Total Acres Burned Visualization? 
For `TotalAcresBurned.png` which involved comparing the annual AQI and the smoke impact, scaling both AQI and smoke impact helped us see trends together over time, making it easier to compare them on the same chart. Without scaling, the two datasets would be tough to view side by side since they naturally operate on very different value ranges.

### Why Prophet for Model Forecasting?
While there are existing models for analyzing wildfire smoke impact (which you can learn about in my final report located in `writeup-reports/Final_Report(1).pdf`, most are not open source, and they are not designed to be forecasting tools. That is why I have employed Prophet, a time-series forecasting tool developed by Meta. It is well-suited for handling seasonal trends and data gaps, making it ideal for generating reliable forecasts of smoke impact and associated mortality. It is specifically designed to capture non-linear trends with yearly seasonality and is robust against outliers, missing data, and significant fluctuations, much like the spike in smoke impact during the 2017 and 2020 wildfires.

### Limitations

Several limitations could affect the accuracy and applicability of the findings in this study. One major limitation is the data coverage. The mortality data used in the analysis only extends to 2014, which means recent trends in respiratory health impacts, especially given the increasing frequency and intensity of wildfires in recent years, are not captured. This gap restricts the ability to fully understand how more recent wildfire activity might influence respiratory health outcomes.

The absence of hospital admission data is another key limitation. By focusing solely on mortality, the study does not capture the broader spectrum of health impacts associated with wildfire smoke exposure, such as increased emergency room visits, long-term respiratory issues, or non-fatal exacerbations of chronic diseases. Including this data could provide a more comprehensive understanding of the health burden caused by wildfire smoke. 

Lastly, the lagged health effects of smoke exposure present a challenge. Many of the long-term impacts of PM2.5 exposure, such as chronic respiratory diseases, may take years to fully manifest. This delay can lead to an underestimation of the true health burden of wildfire smoke, as these effects may not be immediately visible within the study’s time frame.

---


## Instructions for Use
Python (3.8 or later): Ensure you have a compatible version of Python installed.

`pip install pyproj==3.4.1`

`pip install geojson==2.5.0`

`pip install matplotlib==3.6.2`

`pip install scikit-learn==1.1.3`

`pip install statsmodels==0.13.2`

`pip install seaborn==0.12.2`

`pip install prophet==1.1`

