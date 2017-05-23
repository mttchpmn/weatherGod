from flask import Flask, jsonify

from weatherGodapp import app
from lib.rainRadar import RainRadar

############################################################################################################


@app.route('/')
def index():
    return 'API online.'


@app.route('/weathergod/api/v1.0/local')
def local():
    pass


@app.route('/weathergod/api/v1.0/mountain')
def mountain():
     pass


@app.route('/weathergod/api/v1.0/snowreport')
def snow_report():
    pass


@app.route('/weathergod/api/v1.0/radar')
def radar():
    metvuw = RainRadar('http://metvuw.com/forecast/forecast.php?type=rain&region=nzsi&noofdays=3')

    return jsonify({'rainRadar': metvuw.json_object})


@app.route('/weathergod/api/v1.0/webcams')
def webcams():
    pass


@app.route('/weathergod/api/v1.0/river')  # Is this necessary? Static URLs
def river():
    pass