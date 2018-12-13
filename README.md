# Domestic Violence Risk in Seattle
### Helping organizations allocate domestic violence services resources

In 2017, over 54,000 domestic violence offenses were reported to the Washington Association of Sheriffs and Police Chiefs (WASPC).  That equates to nearly 150 reported offenses per day making up over 50% of all crimes against persons in the state.  Rates of offenses vary widely on any given day and each community has different factors associated with changes in rates. Organizations offering victim services and educational service to reduce domestic violence struggle to know when and where services are most needed. Having the ability to forecast fluctuations in the risk of domestic violence by neighborhood dates would guide organizations in  deploying resources at the right time to individual communities. 

## Presentation
https://drive.google.com/file/d/1h0zqaZnMsXsdqWhkXNoYCLrOtrL1DfyB/view?usp=sharing

## Data

### Seattle Police Department Calls for Service
Calls for service data from January 1, 2010 to September 30, 2018, coded for domestic violence ('DV'), were downloaded as a .csv file from the Seattle Police Department "Calls for Service Dashboard" located at:  https://www.seattle.gov/police/information-and-data/calls-for-service-dashboard.
Note that the calls for service data on the City of Seattle Open Data Portal (https://data.seattle.gov/Public-Safety/Call-Data/33kz-ixgy) don't contain the neighborhood location.  While this dataset includes a police beat location these locations do not align with neighborhood boundaries.

### Weather
Historical daily weather data and average daily weather data for Seattle was downloaded as .csv files from the National Oceanic and Atmospheric Administration National Ceters for Environmental Information webisie located at: https://www.ncdc.noaa.gov/cdo-web/search

Near-term, 15-day, weather forecast data is scraped using the weather_scraper.py file located in the src folder in this repo.  The data is scraped from weather.com at: https://weather.com/weather/tenday/l/Seattle+WA+USWA0395:1:US

### Holidays
Custom US Secular and Christian holiday calendars were made using the Holidays Python library (install by: pip install holidays). Chinese New Year holidays were added to the calendar using the Python library, calendra  using the country of Hong Kong's holidays (install by: pip install holidays). Code for recreating the calendar is located in the SeattleHolidays class of holiday_calendars.py.

Islamic holiday calendars were created using the Python library, calendra  using the country of Qatar's holidays (install by: pip install holidays).  Code for recreating the calendar is located in the SeattleHolidays class of holiday_calendars.py.

Jewish holiday calendar data was downloaded as .csv files from Hebcal at https://www.hebcal.com/holidays/. Code for using the calendar file can be found in the in the SeattleHolidays class of holiday_calendars.py.

### Sporting Events
Seattle Seahawks NFL football games information was scraped from Pro Football Reference at: https://www.pro-football-reference.com/years/2018/.  The data was scraped using the scrape_seahawks function in the sports_scrapers.py file located in the src folder in this repo.

Washington Huskies college football game information was scraped from Sports Reference at: https://www.sports-reference.com/cfb/schools/washington/{year}-schedule.html. The data was scraped using the scrape_huskies function in the sports_scrapers.py file located in the src folder in this repo.

Seattle Sounders FC soccer match information table was copied manually from Soccerway at https://us.soccerway.com/teams/united-states/seattle-sounders-fc/13024/matches/.  A copy of the table data is located in the sounders_schedule.csv file in the data_samples folder on this repo.

### Local Events
Dates of local events in Seattle since 2010 were compiled by searching the internet for information on the event.  Event information has been compiled for Seafair, Soltice Parade, Pride Parade and the Women's March.  The data is coded in the EventDummies class of featurizers.py.

## Modeling
To forecast daily domestic violence call rates by neighborhood the problem was broke into two models:

1. Daily call rates for the city of Seattle
2. Daily distribution of calls by Seattle neighborhood

### City level Model - Gradient Boosted Regression Tree

Target Variable:

* Number of domestic violence calls per day for the city of Seattle derived from the calls for service data.  Calls per day were derived  using the Count_Calls class of featurizers.py.

Model Features:

* 225 features including derived date features, weather, holidays, sporting events and      local events.  Features are created using FeaturizeCalls, DateDummies, HolidayDummies and  EventDummies classes in featurizers.py.

A Gradient Boosted Regression Tree model was used to forecast the daily call rates at the city level.  The model was tuned to the following parameters and cross-validated to optimize for lowest test error:

* Boosting stages: 752
* Max depth: 3
* Subsample size: 0.6
* Learning rate: 0.01

The model results in a the following mean squared errors used for cross-validation:
* Training error: 29.75
* Test error: 34.05

### Neighborhood distribution Model - Random Forest

Target Variable:
* The daily distribution of daily calls by Seattle neighborhood derived from the calls for service data.  The daily distribution by neighborhood is derived using...

Model Features:
* 225 features including derived date features, weather, holidays, sporting events and      local events.  Features are created using...

A Random Forest model was used to forecast the daily distribution of calls by neighborhood.  The model was tuned to the following parameters and cross-validated to optimize for lowest test error:

* Max depth: 10
* Max features: auto
* Min sample leaves: 1
* Min sample splits: 5
* Bootstrap: True
* Number of trees: 10,000

The model results in a the following mean squared errors used for cross-validation:

* Training error: 5.99 * 10^-4
* Test error: 6.34 * 10^-4

### Combined Models

Predicted daily rates by neighborhood are calculated by multiplying the city level predicted rates from the Gradient Boosted Regression Tree model by the neighborhood distributions from the Random Forest model.

The combined model results in a the following mean squared errors used for cross-validation:

* Training error: 0.0329
* Test error: 0.0373

## Web application: [enddvseattle.info](https://enddvseattle.info)
An interactive dashboard for users is at enddvseattle.info. Through this dashboard users can select a date and the dashboard returns a map of the city of Seattle with a heatmap of the projected domestic violence calls for service rates for that day. Colors for the heatmap have been set to:

* yellow:  Projected rate for the day is the mean for the neighborhood over next 12 months.
* red: Projected rate for the day is greater than one standard deviation more than the       mean for the neighborhood over next 12 months.
* green: Projected rate for the day is less than one standard-deviation less than the mean   for the neighborhood over next 12 months.

Additionally, the dashboard returns a table of all Seattle neighborhoods with the projected rate for that day and the average projected rate over the next 12 months.

## Access to this Project
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

1. Download this repo
2. Create a new directory titled "data"
3. Move files in example_data directory to data directory or create new data sets for the data directory
4. Follow the steps outlined in the how_to_run_model.ipynb file in the [Notebooks](https://github.com/analyticallycorrect/seattle_domestic_violence/tree/master/Notebooks) directory


## Future Actions
1. Deploy website to domain
2. Additional application features
3. Contact potential users

## Author

* **Joe Armes**  [AnalyticallyCorrect](https://github.com/analyticallycorrect)
