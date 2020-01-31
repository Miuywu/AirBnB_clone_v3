#!/usr/bin/python3
""" state module """
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/api/v1/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def list_cities(state_id):
    """returns list of city objs"""
    city_list = []

    for obj in storage.all("City").values():
        if obj.state_id == state_id:
            city_list.append(obj.to_dict())

    return jsonify(city_list)


@app_views.route('/api/v1/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_cities(city_id):
    """returns city with given id"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/api/v1/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_city(city_id):
    """deletes state of given id"""
    the_forsaken_one = storage.get("City", city_id)
    if not the_forsaken_one:
        abort(404)
    the_forsaken_one.delete()
    storage.save()
    return {}, 200


@app_views.route('/api/v1/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """creates a city"""
    derulo = request.get_json()
    if not derulo:
        abort(400, "Not a JSON")
    if "name" not in derulo:
        abort(400, "Missing name")
    new_me = storage.get("State", state_id)
    if not new_me:
        abort(404)
    jason = City(**derulo)
    storage.new(jason)
    storage.save()
    return make_response(jason.to_dict(), 201)


@app_views.route('/api/v1/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """update a state with given id"""
    derulo = request.get_json()
    if not derulo:
        abort(400, "Not a JSON")
    new_me = storage.get("City", city_id)
    if not new_me:
        abort(404)
    for k, v in derulo.items():
            setattr(new_me, k, v)
    storage.save()
    return make_response(new_me.to_dict(), 200)
