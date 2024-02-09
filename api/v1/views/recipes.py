#!/usr/bin/python3
"""
Recipe API Routes
"""
from api.v1.views import api_views
from flask import jsonify, abort, make_response, request
import requests


@api_views.route('/recipes', methods=['GET'], strict_slashes=False)
def get_random_recipes():
    """
    Retrieves a random list of recipes
    """
    url = f"https://api.spoonacular.com/recipes/random"

    params = {
        "apiKey": "c238bda8889a4a9d8e203d71a0f67219",
        "number": 12000
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            recipes = response.json()
            return recipes
    except requests.exceptions.RequestException:
        return None


@api_views.route('/recipes/find_by_ingr/<ingredients>', methods=['GET'], strict_slashes=False)
def get_recipes_by_ingredient(ingredients):
    """
    Retrieves a random list of recipes
    """
    url = f"https://api.spoonacular.com/recipes/findByIngredients"

    params = {
        "apiKey": "c238bda8889a4a9d8e203d71a0f67219",
        "ingredients": ingredients
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            recipes = response.json()
            return recipes
    except requests.exceptions.RequestException:
        return None


@api_views.route('/recipes/<recipe_id>', methods=['GET'], strict_slashes=False)
def get_recipes_by_id(recipe_id):
    """
    Retrieves a random list of recipes
    """
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"

    params = {
        "apiKey": "c238bda8889a4a9d8e203d71a0f67219"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            recipes = response.json()
            return recipes
    except requests.exceptions.RequestException:
        return None
