#!/usr/bin/python3
""" View for Place objects that handles default API actions """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places(city_id):
    """ Retrieves the list of all Place objects """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def r_place_id(place_id):
    """ Retrieves a Place object """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """ Deletes a Place object """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """ Creates a Place object """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    new_place = request.get_json()
    if not new_place:
        abort(400, "Not a JSON")
    if "user_id" not in new_place:
        abort(400, "Missing user_id")
    user_id = new_place['user_id']
    if not storage.get("User", user_id):
        abort(404)
    if "name" not in new_place:
        abort(400, "Missing name")
    place = Place(**new_place)
    setattr(place, 'city_id', city_id)
    storage.new(place)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """ Updates a Place object """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")

    for k, v in body_request.items():
        if k not in ['id', 'user_id', 'city_at',
                     'created_at', 'updated_at']:
            setattr(place, k, v)

    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
