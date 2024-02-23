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
@api_views.route('/recipes/find_by_ingr/<ingredients>/<offset>', methods=['GET'], strict_slashes=False)
@api_views.route('/recipes/find_by_ingr/<ingredients>/d/<diets>/<offset>', methods=['GET'], strict_slashes=False)
@api_views.route('/recipes/find_by_ingr/<ingredients>/i/<intolerances>/<offset>', methods=['GET'], strict_slashes=False)
@api_views.route('/recipes/find_by_ingr/<ingredients>/<diets>/<intolerances>/<offset>', methods=['GET'], strict_slashes=False)
def get_recipes_by_ingredient(ingredients, offset=0, diets=None, intolerances=None):
    """
    Retrieves a random list of recipes
    """
    #url = f"https://api.spoonacular.com/recipes/findByIngredients"
    url = f"https://api.spoonacular.com/recipes/complexSearch"

    ingredients = ingredients.replace(", ", ",").strip()

    params = {
        "apiKey": apiKey,
        "includeIngredients": ingredients,
        "addRecipeInformation": True,
        "fillIngredients": True,
        "number": 20,
        "offset": 0
    }

    print(f"Diets: {diets}")
    if diets:
        params["diet"] = diets

    print(f"Intolerance: {intolerances}")
    if intolerances:
        params["intolerances"] = intolerances

    params["offset"] = offset

    print(params)
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
        else:
            return jsonify({"error": "No recipe information"})
    except requests.exceptions.RequestException:
        return jsonify({"error": "No recipe information"})
