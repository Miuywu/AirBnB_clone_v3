#!/usr/bin/python3
""" state module """
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def list_states():
    """returns list of state objs"""
    st_list = []

    for obj in storage.all("State").values():
        st_list.append(obj.to_dict())
    return jsonify(st_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """returns state with given id"""
    the_chosen_one = storage.get("State", state_id)
    if not the_chosen_one:
        abort(404)
    return jsonify(the_chosen_one.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_state(state_id):
    """deletes state of given id"""
    the_forsaken_one = storage.get("State", state_id)
    if not the_forsaken_one:
        abort(404)
    the_forsaken_one.delete()
    storage.save()
    return {}, 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """creates a state"""
    derulo = request.get_json()
    if not derulo:
        abort(400, "Not a JSON")
    if "name" not in derulo:
        abort(400, "Missing name")
    Jason = State(**derulo)
    storage.new(Jason)
    storage.save()
    return make_response(Jason.to_dict(), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """update a state with given id"""
    derulo = request.get_json()
    if not derulo:
        abort(400, "Not a JSON")
    new_me = storage.get("State", state_id)
    if not new_me:
        abort(404)
    for k, v in derulo.items():
            setattr(new_me, k, v)
    storage.save()
    return make_response(new_me.to_dict(), 200)
