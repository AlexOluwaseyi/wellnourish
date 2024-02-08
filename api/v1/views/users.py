#!/usr/bin/python3
"""
User API Routes
"""
from api.v1.views import api_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.user import User


@api_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Retrieves the list of all user objects
    """
    users = storage.all(User).values()
    user_lists = []
    for user in users:
        user_lists.append(user.to_dict())
    return jsonify(user_lists)


@api_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_with_id(user_id):
    """
    Retrieves a specific user
    """
    user  = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user)

@api_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    Delete a specific user
    """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)


@api_views.route('/user', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Creates a user
    """
    if not request.get_json():
        abort(404, 'Not a JSON')

    if 'email' not in request.get_json():
        abort(404, 'Missing email!!!')

    if 'username' not in request.get_json():
        abort(404, 'Missing username!!!')

    if 'password' not in request.get_json():
        abort(404, 'Missing password!!!')

    user_details = request.get_json()
    user = User(**user_details)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@api_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    Updates a user
    """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    ignore = ['id', 'email', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
