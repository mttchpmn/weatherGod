from bs4 import BeautifulSoup
import requests

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
            'status': {
                'mountainName': self.mountain_name,
                'mountainStatus': self.mountain_status,
                'liftStatus': self.lift_status,
                'groomedRuns': self.groomed_runs
                },
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
                'lastSnowDate': self.last_snow_date
                }
            }
        return d


############################################################################################################

def test():
    # test = NzskiReport("https://www.nzski.com/mt-hutt/mt-hutt-weather-report", 'mtHutt')
    # test = NzskiReport("https://www.nzski.com/queenstown/the-mountains/coronet-peak/coronet-peak-weather-report",
    #                   'coronetPeak')
    test = NzskiReport("https://www.nzski.com/queenstown/the-mountains/the-remarkables/the-remarkables-weather-report",
                      'theRemarkables')

    print test.mountain_status
    print "BREAK"
    print test.snow_conditions
    print "BREAK"
    print test.current_temp
    print "BREAK"
    print test.weather_conditions
    print "BREAK"
    print test.road_conditions
    print "BREAK"
    print test.min_base
    print "BREAK"
    print test.max_base
    print "BREAK"
    print test.last_snow
    print "BREAK"
    print test.last_snow_date
    print "BREAK"
    print test.groomed_runs
    print "BREAK"
    print test.lift_status

#######################################################

if __name__ == '__main__':
    test()
