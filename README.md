# Domestic Violence Risk in Seattle
## Helping organizations allocate domestic violence services resourc.es

In 2017, over 54,000 domestic violence offenses were reported to the Washington Association of Sheriffs and Police Chiefs (WASPC).  That equates to nearly 150 reported offenses per day making up over 50% of all crimes against persons in the state.  Rates of offenses vary widely on any given day and each community has different factors associated with changes in rates. Organizations offering victim services and educational service to reduce domestic violence struggle to know when and where services are most needed. Having the ability to forecast fluctuations in the risk of domestic violence by neighborhood dates would guide organizations in  deploying resources at the right time to individual communities. 

## Data

### Seattle Police Department Calls for Service
Calls for service data from January 1, 2010 to September 30, 2018, coded for domestic violence ('DV'), were downloaded as a .csv file from the Seattle Police Department "Calls for Service Dashboard" located at:  https://www.seattle.gov/police/information-and-data/calls-for-service-dashboard.
Note that the calls for service data on the City of Seattle Open Data Portal (https://data.seattle.gov/Public-Safety/Call-Data/33kz-ixgy) don't contain the neighborhood location.  While this dataset includes a police beat location these locations do not align with neighborhood boundaries.

### Weather data
Historical daily weather data and average daily weather data for Seattle was downloaded as .csv files from the National Oceanic and Atmospheric Administration National Ceters for Environmental Information webisie located at: https://www.ncdc.noaa.gov/cdo-web/search

Near-term, 15-day, weather forecast data is scraped using the weather_scraper.py file located in the src folder in this repo.  The data is scraped from weather.com at: https://weather.com/weather/tenday/l/Seattle+WA+USWA0395:1:US

### Holidays
Custom US Secular and Christian holiday calendars were made using the Holidays Python library (install by: pip install holidays). Chinese New Year holidays were added to the calendar using the Python library, calendra  using the country of Hong Kong's holidays (install by: pip install holidays). Code for recreating the calendar is located in the SeattleHolidays class of holiday_calendars.py.

Islamic holiday calendars were created using the Python library, calendra  using the country of Qatar's holidays (install by: pip install holidays).  Code for recreating the calendar is located in the SeattleHolidays class of holiday_calendars.py.

Jewish holiday calendar data was downloaded as .csv files from Hebcal at https://www.hebcal.com/holidays/. Code for using the calendar file can be found in the in the SeattleHolidays class of holiday_calendars.py.

## Sporting Events
Seattle Seahawks NFL football games information was scraped from Pro Football Reference at: https://www.pro-football-reference.com/years/2018/.  The data was scraped using the scrape_seahawks function in the sports_scrapers.py file located in the src folder in this repo.

Washington Huskies college football game information was scraped from College 

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Give examples
```

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

