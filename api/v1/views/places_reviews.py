#!/usr/bin/python3
""" state module """
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def list_reviews(place_id):
    """returns list or reviews objs"""
    review_list = []
    place_link = storage.get("Place", place_id)
    if not place_link:
        abort(404)
    for obj in storage.all("Review").values():
        if obj.place_id == place_id:
            review_list.append(obj.to_dict())
    return jsonify(review_list)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """returns review with given id"""
    review_link = storage.get("Review", review_id)
    if not review_link:
        abort(404)
    return jsonify(review_link.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_review(review_id):
    """deletes state of given id"""
    the_forsaken_one = storage.get("Review", review_id)
    if not the_forsaken_one:
        abort(404)
    the_forsaken_one.delete()
    storage.save()
    return {}, 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """creates a city"""
    derulo = request.get_json()
    if not derulo:
        abort(400, "Not a JSON")
    if "user_id" not in derulo:
        abort(400, "Missing user_id")
    if "text" not in derulo:
        abort(400, "Missing text")
    place_link = storage.get("Place", place_id)
    if not place_link:
        abort(404)
    user_link = storage.get("User", derulo['user_id'])
    if not user_link:
        abort(404)
    derulo['place_id'] = place_id
    jason = Review(**derulo)
    storage.new(jason)
    storage.save()
    return make_response(jason.to_dict(), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """update a review with given id"""
    derulo = request.get_json()
    if not derulo:
        abort(400, "Not a JSON")
    review_link = storage.get("Review", review_id)
    if not review_link:
        abort(404)
    for k, v in derulo.items():
            setattr(review_link, k, v)
    storage.save()
    return make_response(review_link.to_dict(), 200)
