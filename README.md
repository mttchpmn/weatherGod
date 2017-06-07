# WeatherGod
#### A Python and Flask API for simplifying **Weather Awareness in Queenstown, NZ**


<img src="/static/logo-small.png" alt="alt text" width="150">

## Overview

WeatherGod has been created to simplify Weather Awareness for adventure personnel.  It does this through collection, aggregation, and propagation of actual and forecast weather information from numerous sources.  The WeatherGod API currently only supports weather information for Queenstown, New Zealand; additional location support is planned in the future.

## Structure

The API is served via Flask in 'app.py'.  The 'lib' folder contains the Python scripts that do the work of collection and aggregation.  Each forecast type is contained via its own script. See below for an example of how the code runs if you make a request to the 'snowreport' endpoint.

*Request made to endpoint - Flask detects route and creates object calling Python script from lib.*
*JSON object is then returned.*

```python
@app.route('/api/v1.0/snowreport')
def snow_report():
    coronet = NzskiReport('https://www.nzski.com/queenstown/the-mountains/coronet-peak/coronet-peak-weather-report',
                          'Coronet Peak')
    remarks = NzskiReport('https://www.nzski.com/queenstown/the-mountains/the-remarkables/the-remarkables-weather-report',
                          'The Remarkables')

    l = [coronet.json_object, remarks.json_object]

    return jsonify({'snowReport': l})
```
*Python script instantiates class which uses Beautiful Soup to scrape data, and save to variables.*
*Class property is then created which the Flask route retuns as JSON data.*

```python
from iceScraper import IceScraper

############################################################################################################


class NzskiReport(IceScraper):
    """Uses parent IceScraper class to extract Snow Report data from NZSki website. 
    Data can be accessed as attributes of class. Specific to NZSki website, and current as of May 2017."""
    def __init__(self, address, mountain_name):
        super(NzskiReport, self).__init__(address)
        self.mountain_name = mountain_name

        # Returns value of 'open' or 'closed'
        self.mountain_status = self.item_by_class("div", "status")
        self.report_time = self.item_by_class("div", "reportDate")[6::]

        # Information Blurbs
        # Return strings of current conditions for snow, weather, and roads
        sn_wx_rd = self.list_by_class("weatherConditionReportText")
        self.snow_conditions = sn_wx_rd[0]
        self.weather_conditions = sn_wx_rd[1]
        self.current_temp = self.item_by_class("span", "weather-temp")
        self.road_conditions = sn_wx_rd[2]

        # Snow Data (cm)
        self.min_base = self.list_from_parent("div", "snowBaseMin")[1].text
        self.max_base = self.list_from_parent("div", "snowBaseMax")[1].text

        self.last_snow = self.list_from_parent("div", "lastSnow")[0].strip()
        self.last_snow_date = self.list_from_parent("div", "lastSnowDate")[1].text

        self.groomed_runs = self.list_from_parent("div", "groomedStatus")[1].text

        # Lists of lift names and corresponding statuses.
        # lift_status zips the two into a dictionary.
        lift_names = self.list_by_class("liftName")
        lift_states = self.list_by_class("statusType")
        self.lift_status = self.dict_from_lists(lift_names, lift_states)

    #######################################################

    @property
    def json_object(self):
        d = {
            'mountainName': self.mountain_name,
            'reportTime': self.report_time,
            'mountainStatus': self.mountain_status,
            'detail': {
                'snowConditions': self.snow_conditions,
                'weatherConditions': self.weather_conditions,
                'roadConditions': self.road_conditions
                },
            'stats':{
                'currentTemp': self.current_temp,
                'minSnowBase': self.min_base,
                'maxSnowBase': self.max_base,
                'lastSnowfall': self.last_snow,
                'lastSnowDate': self.last_snow_date,
                'groomedRuns': self.groomed_runs,
                'liftStatus': self.lift_status,
                }
            }
        return d


############################################################################################################
```
