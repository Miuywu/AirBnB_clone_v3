#!/usr/bin/python3
"""Users functions"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def list_users():
    """returns list of users objs"""
    ur_list = []

    for obj in storage.all("User").values():
        ur_list.append(obj.to_dict())
    return jsonify(ur_list)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """returns user with given id"""
    the_chosen_one = storage.get("User", user_id)
    if not the_chosen_one:
        abort(404)
    return jsonify(the_chosen_one.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_user(user_id):
    """deletes user of given id"""
    the_forsaken_one = storage.get("User", user_id)
    if not the_forsaken_one:
        abort(404)
    the_forsaken_one.delete()
    storage.save()
    return {}, 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_users():
    """creates a user"""
    derulo = request.get_json()
    if not derulo:
        abort(400, "Not a JSON")
    if "email" not in derulo:
        abort(400, "Missing email")
    if "password" not in derulo:
        abort(400, "Missing password")
    Jason = User(**derulo)
    storage.new(Jason)
    storage.save()
    return make_response(Jason.to_dict(), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """update a user with given id"""
    derulo = request.get_json()
    if not derulo:
        abort(400, "Not a JSON")
    new_me = storage.get("User", user_id)
    if not new_me:
        abort(404)
    for k, v in derulo.items():
        if k != "id" and k != "email":
            setattr(new_me, k, v)
    storage.save()
    return make_response(new_me.to_dict(), 200)
