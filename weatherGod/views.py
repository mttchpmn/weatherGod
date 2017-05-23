from weatherGod import app
from rainRadar import RainRadar

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
    radar_dict = {
            'sixAhead': metvuw.img06,
            'twelveAhead': metvuw.img12,
            'eighteenAhead': metvuw.img18,
            'twentyFourAhead': metvuw.img24,
            'thirtyAhead': metvuw.img30,
            'thirtySixAhead': metvuw.img36,
            'fortyTwoAhead': metvuw.img42,
            'fortyEightAhead': metvuw.img48,
                }
        return jsonify({'rainRadar': radar_dict})


@app.route('/weathergod/api/v1.0/webcams')
def webcams():
    pass


@app.route('/weathergod/api/v1.0/river')  # Is this necessary? Static URLs
def river():
    pass