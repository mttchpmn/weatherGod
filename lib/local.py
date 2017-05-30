# TODO - Move Mountain to separate module
# TODO - Change class attributes to absolute values rather than strings

# Import required lib
import requests

############################################################################################################


# Create a parent weather class that the forecasts inherit from
class Weather(object):
    def __init__(self, api_address):
        self.api_address = api_address
        self.response = self.get_response(api_address)

    # Retrieve API response from given URL
    def get_response(self, address):
        print 'Getting response from: ', self.api_address
        r = requests.get(address)
        response = r.json()
        return response

############################################################################################################


# Create instance of local weather forecast, retrieve and save data to variables
class Aerodrome(Weather):
    #  Access via 'http://www.metservice.com/publicData/localObsPage'
    def __init__(self, api_address, locationCode):
        super(Aerodrome, self).__init__(api_address)
        self.locationCode = locationCode
        forecast = self.get_info()

        default = 'Data not found.'

        self.location = forecast.get('locationDesc')
        self.validTime = forecast.get('dateTime', default)
        self.tempDegrees = forecast.get('temp', default)
        self.windSpeedKm = forecast.get('windSpeed', default)
        self.windDirection = forecast.get('windDirection', default)
        self.rainLastHour = forecast.get('rainfall', default)
        self.humidity = forecast.get('humidity', default)
        self.pressure = forecast.get('pressure', default)

    #######################################################

    @property
    def json_object(self):
        d = {
            'location': self.location,
            'validTime':self.validTime,
            'windData': {
                'windSpeedKm': self.windSpeedKm,
                'windDirection': self.windDirection,
                },
            'airData': {
                'rainLastHour': self.rainLastHour,
                'humidity': self.humidity,
                'pressure': self.pressure,
                'tempDegrees': self.tempDegrees
                }
        }
        return d

    #######################################################

    # Identify correct part of API response based on provided description
    def get_info(self):
        for i in self.response:
            if i['location'] == self.locationCode:
                info = i
                return info

############################################################################################################

""" DEPRECATED - API redirects directly to the metservice page.
# Create instance of mountain weather forecast, retrieve and save data to variables
class Mountain(Weather):
    #  Access via 'http://www.metservice.com/publicData/alpineLocForecastSouthern-Lakes_5'
    def __init__(self, api_address, day):
        super(Mountain, self).__init__(api_address)
        for i in self.response:
            if i['validFromDay'] == day:
                fc = i
        self.day = '%s - %s' % (fc['location'], fc['validFromDay'])
        self.issued = "Issued: %s" % fc['issued']
        self.status = fc['forecast']
        self.fzl = 'Freezing Level: %s' % fc['fzl']
        self.wind1 = 'Wind at 1000m: %s' % fc['wind1000']
        self.wind2 = 'Wind at 2000m: %s' % fc['wind2000']
"""

############################################################################################################


# Create instance of Holfuy Weather Station Data, retrieve and save data to variables
class Holfuy(Weather):
    #  Access through 'http://holfuy.com/en/modules/mjso.php?k=s409'
    #  The last 3 digits refer to the site code
    def __init__(self, api_address, location):
        super(Holfuy, self).__init__(api_address)
        self.location = location

    @property
    def json_object(self):
        d = {
            'location': self.location,
            'units': {
                'windUnits': self.response['speed_unit'],
                'tempUnits': self.response['temp_unit']
            },
            'currentWind': {
                'curWindSpeed': self.response['speed'],
                'curWindGust': self.response['gust'],
                'curMaxGust': self.response['max_gust'],
                'curWindBearing': self.response['dir'],
                'curWindDirection': self.response['dir_str']
            },
            'currentTemp': {
                'curTemp': self.response['temperature'],
                'windChill': self.response['wind_chill']
            },
            'windTendency': {
                'speedTendency': self.response['speed_tendency'],
                'speedRate': self.response['speed_rate'],
                'bearingTendency': self.response['dir_tendency'],
                'rateTendency': self.response['dir_rate']
            },
            'averageWind': {
                'avgWindSpeed': self.response['avg_speed'],
                'avgWindBearing': self.response['avg_dir'],
                'avgWindDirection': self.response['avg_dir_str']
            },
            'dailyWind':{
                'dayAvgWindSpeed': self.response['daily_avg_speed'],
                'dayMaxWindSpeed': self.response['daily_max_wind']
            },
            'dailyTemp': {
                'dayMaxTemp': self.response['daily_max_temp'],
                'dayMinTemp': self.response['daily_min_temp']
            }

        }
        return d


