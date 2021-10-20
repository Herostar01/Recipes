from flask_app.config.mysqlconnection import connectToMySQL

import re	

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

from flask import flash 

DATABASE = "recipes" 

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all_user(cls):
        query = 'SELECT * FROM users;'
        results = connectToMySQL(DATABASE).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users 

    @classmethod 
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password ) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s  ) ;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results 
    @classmethod
    def destroy_user(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s ;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) < 1:
            return False 
        return cls(results[0]) 

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return cls(results[0])

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, user)
        if len(results) >= 1:
            flash("Email already in use.", "Please register because we love you Tyler :D " )
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!", "Please Register Pablo because Tyler needs you lol :D")
            is_valid = False
        if len(user['first_name']) < 3: 
            flash("First name must be at least 3 characters","register")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters","register") 
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid = False
        if user['password'] != user['confirm']: #this part of the code makes sure the passwords match  
            flash("Passwords don't match","register")
        return is_valid 

    @staticmethod 
    def validate_user(user):
        is_valid = True
        #Line that tests email pattern to match with database
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!")
            is_valid = False
        return is_valid 

    # @classmethod 
    # def save(cls,data):
    #     query = "INSERT INTO users (first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
    #     return connectToMySQL(cls.db).query_db(query,data)