from flask import Flask

app = Flask(__name__)

application = app

import app.views
import app.lib
