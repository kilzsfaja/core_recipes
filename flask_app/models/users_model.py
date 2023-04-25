from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, EMAIL_REGEX, app
from flask import flash
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt( app )

class User:
    def __init__( self, data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

# --- CREATE USER --- #
    @classmethod
    def create_one( cls, data ):
        query = """
            INSERT INTO users ( first_name, last_name, email, password )
            VALUES( %(first_name)s, %(last_name)s, %(email)s, %(password)s );
        """
        result = connectToMySQL( DATABASE ).query_db( query, data )
        return result

# ---- GET ONE USER --- #
    @classmethod
    def get_one( cls, data ):
        query = """
            SELECT *
            FROM users
            WHERE email = %(email)s;
        """
        result = connectToMySQL( DATABASE ).query_db( query, data )
        if len( result ) == 0:
            return None
        else:
            return cls( result[0] )

# ---- VALIDATION --- #
    @staticmethod
    def validate_user( data ):
        is_valid = True
        if len( data["first_name"] ) < 2:
            flash( "Your first name must be atleast 2 characters long.", "error_name" )
            is_valid = False
        if len( data["last_name"] ) < 2:
            flash( "Your last name must be atleast 2 characters long.", "error_name" )
            is_valid = False
        if not EMAIL_REGEX.match( data["email"] ):
            flash( "You must provide a valid email!", "error_email" )
            is_valid = False
        if len( data["password"] ) < 8:
            flash( "Please provide a password that is 8 characters long.", "error_password" )
            is_valid = False
        if data["password"] != data["password_confirmation"]:
            flash( "Passwords do not match!", "error_password" )
            is_valid = False
        if User.get_one( data ):
            flash( "The email is already taken!", "error_email" )
            is_valid = False
        return is_valid

    @staticmethod
    def validate_password( password, encrypted_password ):
        if not bcrypt.check_password_hash( encrypted_password, password ):
            flash( "Wrong password, please try again!", "error_login_password" )
            return False
        return True

    @staticmethod
    def encrypt_string( text ):
        encrypted_string = bcrypt.generate_password_hash( text )
        return encrypted_string