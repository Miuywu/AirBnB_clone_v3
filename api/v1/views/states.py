#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify, abort
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from api.v1.app import *
from Flask import request


@app_views.route('/api/v1/states', methods=['GET'])
    """You must use to_dict() to retrieve an object into a valid JSON
    Retrieves the list of all State objects: GET /api/v1/states"""
    return State.to_dict()


@app_views.route('/api/v1/states/<state_id>', methods=['GET'])
    """Retrieves a State object: GET /api/v1/states/<state_id>"""
    """If the state_id is not linked to any State object, raise a 404 error"""
    if State(state_id) == NULL:
        abort(404)
    return State(state_id)

@app_views.route('/api/v1/states/<state_id>', methods=['DELETE'])
    """Deletes a State object:: DELETE /api/v1/states/<state_id>"""
    """If the state_id is not linked to any State object, raise a 404 error"""
    if State(state_id) == NULL:
        abort(404)
    return {}, 200

@app_views.route('/api/v1/states', methods=['POST'])
    """Creates a State: POST /api/v1/states"""
    derulo = request.get_json()
    try:
        check = json.loads(derulo)
        return 
    except valueError:
        print("Not a JSON")
        abort(400)

    If the HTTP body request is not valid JSON, raise a 400 error with the message Not a JSON
    If the dictionary doesnt contain the key name, raise a 400 error with the message Missing name
    Returns the new State with the status code 201

"""Updates a State object: PUT /api/v1/states/<state_id>"""

    If the state_id is not linked to any State object, raise a 404 error
    You must use request.get_json from Flask to transform the HTTP body request to a dictionary
    If the HTTP body request is not valid JSON, raise a 400 error with the message Not a JSON
    Update the State object with all key-value pairs of the dictionary.
    Ignore keys: id, created_at and updated_at
    Returns the State object with the status code 200
