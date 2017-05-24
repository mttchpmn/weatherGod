
# TODO - Make JSON objects more verbose?

from flask import Flask, jsonify

from lib.rainRadar import RainRadar
from lib.snowReports import NzskiReport
from lib.webcam import NzskiWebcam, AirportWebcam, StaticWebcam

app = Flask(__name__)

############################################################################################################


@app.route('/')
def index():
    return 'API online.'

############################################################################################################


@app.route('/weathergod/api/v1.0/local')
def local():
    pass


@app.route('/weathergod/api/v1.0/mountain')
def mountain():
    pass

############################################################################################################


@app.route('/weathergod/api/v1.0/snowreport')
def snow_report():
    coronet = NzskiReport('https://www.nzski.com/queenstown/the-mountains/coronet-peak/coronet-peak-weather-report',
                          'Coronet Peak')
    remarks = NzskiReport('https://www.nzski.com/queenstown/the-mountains/the-remarkables/the-remarkables-weather-report',
                          'The Remarkables')

    l = [coronet.json_object, remarks.json_object]

    return jsonify({'snowReport': l})


############################################################################################################


@app.route('/weathergod/api/v1.0/rainradar')
def radar():
    metvuw = RainRadar('http://metvuw.com/forecast/forecast.php?type=rain&region=nzsi&noofdays=3')
    return jsonify({'rainRadar': metvuw.json_object})

############################################################################################################


@app.route('/weathergod/api/v1.0/webcam')
def webcams():
    coronet = NzskiWebcam('https://www.nzski.com/queenstown/the-mountains/coronet-peak/coronet-peak-weather-report',
                          'Coronet Peak')
    remarks = NzskiWebcam('https://www.nzski.com/queenstown/the-mountains/the-remarkables/the-remarkables-weather-report',
                          'The Remarkables')
    airport = AirportWebcam('http://www.queenstownairport.co.nz/travelling/flight-info/webcam')

    print airport.json_object

    static = StaticWebcam()

    d = {
        'coronetPeak': coronet.json_object,
        'theRemarkables': remarks.json_object,
        'airport': airport.json_object,
        'static': static.json_object
    }

    return jsonify({'webcams':d})

############################################################################################################


@app.route('/weathergod/api/v1.0/riverflow')
def river():
    d = {
        'dart': 'http://water.orc.govt.nz/Drop/Graphs/HillocksFlow7.gif',
        'shotover': 'http://water.orc.govt.nz/Drop/Graphs/PeatsFlow7.gif',
        'kawarau': 'http://water.orc.govt.nz/Drop/Graphs/Chards7.gif'
    }
    return jsonify({'riverFlow': d})

if __name__ == '__main__':
    app.run()
