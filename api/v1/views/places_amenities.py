#!/usr/bin/python3
""" state module """
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def list_place_amenities(place_id):
    """returns list of amenity objs"""
    if models.storage_t == 'db':
        return None
    place_link = storage.get("Place", place_id)
    if not place_link:
        abort(404)
    return jsonify(place_link.amenity_ids)


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_amenity_place(place_id, amenity_id):
    """deletes state of given id"""
    if models.storage_t == 'db':
        return None
    place_link = storage.get("Place", place_id)
    if not place_link:
        abort(404)
    amenity_link = storage.get("Amenity", amenity_id)
    if not amenity_link:
        abort(404)
    if amenity_id not in place_link.amenity_ids:
        abort(404)
    place_link.amenity_ids.remove(amenity_id)
    storage.save()
    return {}, 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def post_amenity_to_place(place_id, amenity_id):
    """creates a city"""
    if models.storage_t == 'db':
        return None
    place_link = storage.get("Place", place_id)
    if not place_link:
        abort(404)
    amenity_link = storage.get("Amenity", amenity_id)
    if not amenity_link:
        abort(404)
    if amenity_id in place_link.amenity_ids:
        return make_response(amenity_link.to_dict(), 201)
    place_link.amenity_ids.append(amenity_id)
    storage.save()
    return make_response(amenity_link.to_dict(), 201)
