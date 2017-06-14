
# TODO - Make JSON objects more verbose?

from flask import Flask, jsonify, render_template, redirect
from requests import get as GET
from pprint import pprint

from lib.rainRadar import RainRadar
from lib.snowReports import NzskiReport
from lib.webcam import NzskiWebcam, AirportWebcam, StaticWebcam
from lib.local import Aerodrome, Holfuy

app = Flask(__name__)

############################################################################################################


@app.route('/')
def index():
    return 'API online.'


@app.route('/api/v1.0/docs')
def docs():
    return render_template('docs.html')

############################################################################################################


@app.route('/api/v1.0/local')
def local():
    ad = Aerodrome('http://www.metservice.com/publicData/localObsPage', '93831')
    flightpark = Holfuy('http://holfuy.com/en/modules/mjso.php?k=s409', 'Flightpark')
    gondola = Holfuy('http://holfuy.com/en/modules/mjso.php?k=s170', 'Skyline Gondola')
    glenorchy = Holfuy('http://holfuy.com/en/modules/mjso.php?k=s278', 'Glenorchy')
    coronetExpress = Holfuy('http://holfuy.com/en/modules/mjso.php?k=s256', 'Coronet Express')

    ws = [
        gondola.json_object,
        coronetExpress.json_object,
        flightpark.json_object,
        glenorchy.json_object
    ]

    return jsonify([{'aerodrome': ad.json_object}, {'weatherStations': ws}])


@app.route('/api/v1.0/mountain')
def mountain():
    return redirect('http://www.metservice.com/publicData/alpineLocForecastSouthern-Lakes_5')

############################################################################################################


@app.route('/api/v1.0/snowreport')
def snow_report():
    coronet = NzskiReport('https://www.nzski.com/queenstown/the-mountains/coronet-peak/coronet-peak-weather-report',
                          'Coronet Peak')
    remarks = NzskiReport('https://www.nzski.com/queenstown/the-mountains/the-remarkables/the-remarkables-weather-report',
                          'The Remarkables')

    l = [coronet.json_object, remarks.json_object]

    return jsonify({'snowReport': l})


############################################################################################################


@app.route('/api/v1.0/rainradar')
def radar():
    metvuw = RainRadar('http://metvuw.com/forecast/forecast.php?type=rain&region=nzsi&noofdays=3')
    return jsonify({'rainRadar': metvuw.json_object})

############################################################################################################


@app.route('/api/v1.0/webcam')
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


@app.route('/api/v1.0/riverflow')
def river():
    d = {
        'dart': 'http://water.orc.govt.nz/Drop/Graphs/HillocksFlow7.gif',
        'shotover': 'http://water.orc.govt.nz/Drop/Graphs/PeatsFlow7.gif',
        'kawarau': 'http://water.orc.govt.nz/Drop/Graphs/Chards7.gif'
    }
    return jsonify({'riverFlow': d})

############################################################################################################

@app.route('/view/webcam')
def view_webcam():
    r = GET('https://weathergod.herokuapp.com/api/v1.0/webcam').json()

    airport = r['webcams']['airport']
    coronet = r['webcams']['coronetPeak']
    remarks = r['webcams']['theRemarkables']
    static = r ['webcams']['static']

    return render_template('webcam.html', 
                            airport=airport, 
                            coronet=coronet, 
                            remarks=remarks, 
                            static=static
                            )

############################################################################################################

@app.route('/view/local')
def view_local():
    r = GET('https://weathergod.herokuapp.com/api/v1.0/local').json()

    pprint(r)
    aerodrome = r[0]['aerodrome']
    

    return render_template('local.html', 
                            aerodrome=aerodrome
                            )


if __name__ == '__main__':
    app.run()
