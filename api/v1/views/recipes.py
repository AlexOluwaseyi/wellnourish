#!/usr/bin/python3
"""
Recipe API Routes
"""
from api.v1.views import api_views
from flask import jsonify, abort, make_response, request
import requests
from creds import apiKey


@api_views.route('/recipes', methods=['GET'], strict_slashes=False)
def get_random_recipes():
    """
    Retrieves a random list of recipes
    """
    url = f"https://api.spoonacular.com/recipes/random"

    params = {
        "apiKey": apiKey,
        "number": 100
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            new_recipes = []
            recipes = response.json().get("recipes")
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
        "apiKey": apiKey,
        "ingredients": ingredients,
        "number": 100
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
        "apiKey": apiKey
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
