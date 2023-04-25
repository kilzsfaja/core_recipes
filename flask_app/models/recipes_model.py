from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import users_model

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under = data['under']
        self.date = data['date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']


# ------ CREATE RECIPE ------
    @classmethod
    def create_recipe(cls, data):
        query = """
            INSERT INTO recipes (name, description, instructions, under, date, user_id)
            VALUES (%(name)s, %(description)s, %(instructions)s, %(under)s, %(date)s, %(user_id)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)

# ------ READ ALL ------
    @classmethod
    def get_all(cls):
        query = """
            SELECT * 
            FROM recipes
            LEFT JOIN users ON users.id = recipes.user_id;
        """
        results = connectToMySQL(DATABASE).query_db(query)
        # print(results)
        list_of_all_recipes = []
        for row in results:
            this_recipe = cls(row)
            user_data = {
                **row,
                'id': row['users.id'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            this_user = users_model.User(user_data)
            this_recipe.chef = this_user
            # adding chef to Recipe class -- chef = new attribute
            list_of_all_recipes.append(this_recipe)
        return list_of_all_recipes
    # this method returns a list of instances not dicts that have a user instance which is called chef

# ------ READ ONE ------
    @classmethod
    def get_one_by_id(cls, id):
        data_banana = {
            'id': id
        }
        query = """
            SELECT *
            FROM recipes
            JOIN users ON users.id = recipes.user_id
            WHERE recipes.id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data_banana)
        if results:
            this_recipe = cls(results[0])
            row = results[0]
            user_data = {
                **row,
                'id': row['users.id'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            this_user = users_model.User(user_data)
            this_recipe.chef = this_user
            return this_recipe
        return False
    # this method returns a dict that has a user instance which is called chef

# ------ UPDATE ONE ------
    @classmethod
    def update_recipe(cls, data):
        query = """
            UPDATE recipes
            SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, under = %(under)s, date = %(date)s
            WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
# ------ DELETE ONE ------
    @classmethod
    def delete_recipe(cls, data):
        query = """
            DELETE FROM recipes
            WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)

# ----- VALIDATION ---
    @staticmethod
    def validate_recipe(form_data):
        is_valid = True
        if len(form_data['name']) < 3:
            is_valid = False
            flash('Name must be at least 3 characters long')
        if len(form_data['description']) < 3:
            is_valid = False
            flash('Description must be at least 3 characters long')
        if len(form_data['instructions']) < 3:
            is_valid = False
            flash('Instructions must be at least 3 characters long')
        if len(form_data['date']) < 1:
            is_valid = False
            flash('Date is required')

        if 'under' not in form_data:
            is_valid = False
            flash('Field is required')
        return is_valid
