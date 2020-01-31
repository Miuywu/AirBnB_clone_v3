#!/usr/bin/python3
""" state module """
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def list_plays(city_id):
    """returns place of city objs"""
    place_list = []
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    for obj in storage.all("Place").values():
        if obj.city_id == city_id:
            place_list.append(obj.to_dict())
    return jsonify(place_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """returns place with given id"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """deletes state of given id"""
    the_forsaken_one = storage.get("Place", place_id)
    if not the_forsaken_one:
        abort(404)
    the_forsaken_one.delete()
    storage.save()
    return {}, 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """creates a city"""
    derulo = request.get_json()
    if not derulo:
        abort(400, "Not a JSON")
    if "name" not in derulo:
        abort(400, "Missing name")
    if "user_id" not in derulo:
        abort(400, "Missing name")
    city_link = storage.get("City", city_id)
    if not city_link:
        abort(404)
    user_link = storage.get("User", derulo['user_id'])
    if not user_link:
        abort(404)
    derulo['city_id'] = city_id
    jason = Place(**derulo)
    storage.new(jason)
    storage.save()
    return make_response(jason.to_dict(), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """update a state with given id"""
    derulo = request.get_json()
    if not derulo:
        abort(400, "Not a JSON")
    place_link = storage.get("Place", place_id)
    if not place_link:
        abort(404)
    for k, v in derulo.items():
            setattr(place_link, k, v)
    storage.save()
    return make_response(place_link.to_dict(), 200)
