#!/usr/bin/python3
"""Amenities functions"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def list_amenities():
    """returns list of amenity objs"""
    ay_list = []

    for obj in storage.all("Amenity").values():
        ay_list.append(obj.to_dict())
    return jsonify(ay_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """returns amenity with given id"""
    the_chosen_one = storage.get("Amenity", amenity_id)
    if not the_chosen_one:
        abort(404)
    return jsonify(the_chosen_one.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_amenity(amenity_id):
    """deletes amenity of given id"""
    the_forsaken_one = storage.get("Amenity", amenity_id)
    if not the_forsaken_one:
        abort(404)
    the_forsaken_one.delete()
    storage.save()
    return {}, 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenities():
    """creates an amenity"""
    derulo = request.get_json()
    if not derulo:
        abort(400, "Not a JSON")
    if "name" not in derulo:
        abort(400, "Missing name")
    Jason = State(**derulo)
    storage.new(Jason)
    storage.save()
    return make_response(Jason.to_dict(), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """update a amenity with given id"""
    derulo = request.get_json()
    if not derulo:
        abort(400, "Not a JSON")
    new_me = storage.get("Amenity", amenity_id)
    if not new_me:
        abort(404)
    for k, v in derulo.items():
            setattr(new_me, k, v)
    storage.save()
    return make_response(new_me.to_dict(), 200)
