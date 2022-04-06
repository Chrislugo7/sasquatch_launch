from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

class Recipe:
    db_name = 'sasquatch_schema'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.number_of_sasquatches = db_data['number_of_sasquatches']
        self.location = db_data['location']
        self.what_happaned = db_data['what_happaned']
        self.date_made = db_data['date_made']
        self.user_id = User.get_by_id({"id": db_data['user_id']})
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO recipes (number_of_sasquatches, location, what_happaned, date_made, user_id) VALUES (%(number_of_sasquatches)s,%(location)s,%(what_happaned)s,%(date_made)s,%(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        print(results)
        all_recipes = []
        for row in results:
            print(row['date_made'])
            all_recipes.append( cls(row) )
        print(all_recipes)
        return all_recipes
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET number_of_sasquatches=%(number_of_sasquatches)s, location=%(location)s, what_happaned=%(what_happaned)s, date_made=%(date_made)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['location']) < 3:
            is_valid = False
            flash("Location must be at least 3 characters","recipe")
        if len(recipe['what_happaned']) < 3:
            is_valid = False
            flash("What Happaned must be at least 3 characters","recipe")
        if len(recipe['number_of_sasquatches']) < 1:
            is_valid = False
            flash("Number of Sasquatches min 1","recipe")
        if recipe['date_made'] == "":
            is_valid = False
            flash("Please enter a date","recipe")
        return is_valid





        