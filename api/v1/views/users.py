#!/usr/bin/python3
"""
User API Routes
"""
from api.v1.views import api_views
from flask import jsonify
from flasgger.utils import swag_from
from models import storage
from models.user import User

@api_views.route('/users', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/all_users.yml')
def get_users():
    """
    Retrieves the list of all user objects
    or a specific user
    """
    users = storage.all(User).values()
    user_lists = []
    for user in users:
        user_lists.append(user.to_dict())
    return jsonify(user_lists)
