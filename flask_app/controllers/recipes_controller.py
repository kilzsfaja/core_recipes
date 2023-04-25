from flask import render_template, request, redirect, session
from flask import flash
from flask_app import app
from flask_app.models.recipes_model import Recipe
from flask_app.models.users_model import User

# ----------- CREATE RECIPE (render) -----------
@app.route('/recipes/new', methods=['GET'])
def new_recipe():
    return render_template('create_recipe.html')

# ----------- CREATE RECIPE (POST) -----------
@app.route('/recipes/create', methods=['POST'])
def create_new_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    recipe_data = {
        **request.form,
        'user_id': session['user_id']
    }
    Recipe.create_recipe(recipe_data)
    return redirect('/recipes')

# ---------- READ ONE RECIPE (render) ---------
@app.route('/recipes/<int:id>')
def show_recipe(id):
    this_recipe = Recipe.get_one_by_id(id)
    return render_template('show_recipe.html', this_recipe=this_recipe)

# ---------- EDIT ONE RECIPE (render) ---------
@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    this_recipe = Recipe.get_one_by_id(id)
    return render_template('edit_recipe.html', this_recipe=this_recipe)

# ---------- UPDATE ONE RECIPE ---------
@app.route('/recipes/update/<int:id>', methods=['POST'])
def update_recipe(id):
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/edit/{id}')
    data = {
        'id': id,
        **request.form,
        'user_id': session['user_id']
    }
    Recipe.update_recipe(data)
    return redirect('/recipes')

# ---------- DELETE ONE RECIPE ---------
@app.route('/recipes/delete/<int:id>')
def delete_recipe(id):
    Recipe.delete_recipe({'id':id})
    return redirect('/recipes')