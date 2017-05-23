from weatherGod import app


@app.route('/')
def index():
    return 'API online.'
