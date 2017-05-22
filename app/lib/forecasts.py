# Import required modules
import json
import requests

###################################


# Create a parent weather class that the forecasts inherit from
class Weather(object):
	def __init__(self, api_address):
		self.api_address = api_address
		self.response = self.getResponse(api_address)

	# Retrieve API response from given URL
	def getResponse(self, address):
		print 'Getting response from: ', self.api_address
		r = requests.get(address)
		response = r.json()
		return response

###################################


# Create instance of local weather forecast, retrieve and save data to variables
class Local(Weather):
	def __init__(self, api_address, description):
		super(Local, self).__init__(api_address)
		self.description = description
		forecast = self.getInfo()

		default = 'Data not found.'
		self.location = forecast['locationDesc'].upper()
		self.time = 'Effective: %s' % forecast.get('dateTime', default)
		self.temp = 'Temperature: %s degrees Celsius' % forecast.get('temp', default)
		self.windSpd  = 'Wind Speed: %skm/h' % forecast.get('windSpeed', default)
		self.windDir = 'Wind Direction: %s' % forecast.get('windDirection', default)
		self.rain = 'Rainfall (Last hour): %smm' % forecast.get('rainfall', default)
		self.rh = 'Humidity: %s%%' % forecast.get('humidity', default)
		self.pressure = 'Pressure: %shPa' % forecast.get('pressure', default)

		#self.fc = '%s\n%s\n\n%s\n%s\n%s\n%s\n%s\n%s\n' % (location, time, temp, windSpd, windDir, rain, rh, pressure)

	# Print forecast to console (deprecated)
	def printForecast(self):
		stats = [self.location, self.time, '-'*30, self.temp, self.windSpd, self.windDir, self.rain, self.rh, self.pressure]
		for item in stats:
			print item

	# Identify correct part of API response based on provided description
	def getInfo(self):
		for i in self.response:
			if i['locationDesc'] == self.description:
				info = i
		return info

###################################


# Create instance of mountain weather forecast, retrieve and save data to variables
class Mountain(Weather):
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

###################################


# Create instance of Holfuy Weather Station Data, retrieve and save data to variables
class Holfuy(Weather):
	def __init__(self, api_address):
		super(Holfuy, self).__init__(api_address)

		self.curWind = 'Current Wind: %s%s %s gusting %s' % (self.response['speed'], self.response['speed_unit'], self.response['dir_str'], self.response['gust'])
		self.avgWind = 'Average Wind: %s%s %s max gust %s' % (self.response['avg_speed'], self.response['speed_unit'], self.response['avg_dir_str'], self.response['max_gust'])
		self.tendency = 'Speed: %s Direction: %s' % (self.response['speed_tendency'], self.response['dir_tendency'])
		self.curTemp = 'Current Temp: %s%s' % (self.response['temperature'], self.response['temp_unit'])
		self.wChill = 'Wind Chill: %s%s' % (self.response['wind_chill'], self.response['temp_unit'])
		self.dayWind = 'Daily Wind - Avg: %s%s Max: %s%s' % (self.response['daily_avg_speed'], self.response['speed_unit'], self.response['daily_max_wind'], self.response['speed_unit'])
		self.dayTemp = 'Daily Temp - Min: %s%s Max: %s%s' % (self.response['daily_min_temp'], self.response['temp_unit'], self.response['daily_max_temp'], self.response['temp_unit'])








