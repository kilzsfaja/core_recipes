from flask import render_template, request, redirect, session
from flask import flash
from flask_app import app
from flask_app.models.users_model import User
from flask_app.models.recipes_model import Recipe

# ----- INDEX -----
@app.route( "/", methods=["GET"] )
def index():
    return render_template( "index.html" )

# ----- REGISTER -----
@app.route( "/user/new", methods=["POST"] )
def create_user():
    if User.validate_user( request.form ) == False:
        return redirect( "/" )
    encrypted_password = User.encrypt_string( request.form["password"] )
    data = {
        **request.form,
        "password" : encrypted_password
    }
    user_id = User.create_one( data )
    session["user_id"] = user_id
    session["first_name"] = request.form["first_name"]
    return redirect( "/recipes" )


# ------- WELCOME USER -----
@app.route( "/recipes")
def welcome_page():
    if "user_id" not in session:
        return redirect( "/" )
    all_recipes = Recipe.get_all()
    return render_template( "welcome.html", all_recipes=all_recipes )


# ----- LOGIN -----
@app.route( "/user/login", methods=["POST"] )
def login():
    current_user = User.get_one( request.form )
    if current_user == None:
        flash( "Email not found!", "error_login_email" )
        return redirect( "/" )
    if User.validate_password( request.form["password"], current_user.password ) == False:
        return redirect( "/" )
    session["user_id"] = current_user.id
    session["first_name"] = current_user.first_name
    return redirect( "/recipes" )

# ----- LOGOUT -----
@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect("/")