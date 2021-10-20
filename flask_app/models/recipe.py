from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 

DATABASE = "recipes"

class Recipe:

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description'] 
        self.instructions = data['instructions']
        self.under30 = data['under30']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod 
    def create_recipe (cls, data): #order doesn't matter on left side of values but has to match for right side
        query = "INSERT INTO recipes (name, description, instructions, under30, date_made, user_id) VALUES ( %(name)s, %(description)s, %(instructions)s, %(under30)s, %(date_made)s %(user_id)s  );"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all_recipe(cls):
        query = "SELECT * FROM recipes;"
        recipes_from_db = connectToMySQL(DATABASE).query_db(query)
        recipes = []
        for r in recipes_from_db:
            recipes.append(cls(r))
        return recipes 

    @classmethod
    def get_one_recipe(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        recipes_from_db = connectToMySQL(DATABASE).query_db(query, data)
        return cls(recipes_from_db[0])
    
    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, under30 = %(under30)s, date_made = %(date_made)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data) 

    @classmethod
    def destroy_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3: 
            is_valid = False
            flash("Name must be at least 3 characters", "recipe")
        if len(recipe['instructions']) < 3:
            is_valid = False
            flash("Instructions must be at least 3 characters", "recipe")
        if len(recipe['description']) < 3:
            is_valid = False
            flash("Description must be at least 3 characters","recipe")
        if recipe['date_made'] == "":
            is_valid = False
            flash("Please enter a date","recipe")
        return is_valid 