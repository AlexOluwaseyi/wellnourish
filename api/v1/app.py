#!/usr/bin/python3
"""
API module of wellnourish
"""
from models import storage
from flask import Flask, jsonify, make_response
from api.v1.views import api_views
from flask_cors import CORS
from flasgger import Swagger
from flasgger.utils import swag_from


api = Flask(__name__)
api.register_blueprint(api_views)
cors = CORS(api, resources={r"/api/v1/*": {"origins": "*"}})


@api.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()


@api.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)

api.config['SWAGGER'] = {
    'title': 'WellNourish API',
    'uiversion': 3
}

Swagger(api)


if __name__ == "__main__":
    api.run(host="0.0.0.0", port=5000, threaded=True)
