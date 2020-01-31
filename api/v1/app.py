#!/usr/bin/python3
"""starts a Flask web application"""

from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, make_response, jsonify
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
hst = getenv("HBNB_API_HOST") or '0.0.0.0'
prt = getenv("HBNB_API_PORT") or '5000'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
cors = CORS(app, resources={r'/*': {'origins': '0.0.0.0'}})


@app.teardown_appcontext
def session_pooff(self):
    """Alchemy down"""
    storage.close()


@app.errorhandler(404)
def not_found(self):
    """route not found handler"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host=hst, port=prt, threaded=True)
