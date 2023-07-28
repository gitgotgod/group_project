from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
mydb = 'basketball_db'

class Game:
    def __init__(self,data):
        self.id = data['id']
        self.hometeam = data['hometeam']
        self.homescore = data['homescore']
        self.awayteam = data['awayteam']
        self.awayscore = data['awayscore']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

#get all method, used for displaying all the games
    @classmethod
    def get_all(cls):
        query = """SELECT * FROM games
        JOIN users on games.user_id = users.id;
        """
        results = connectToMySQL(mydb).query_db(query)

        games = []
        for team in results:
            games.append(team)
        return games
    
#method to save the game data into the database
    @classmethod
    def save(cls, form_data):
        query = """
                INSERT INTO games (hometeam,homescore,awayteam,awayscore,user_id)
                VALUES (%(hometeam)s,%(homescore)s,%(awayteam)s,%(awayscore)s,%(user_id)s);
                """
        return connectToMySQL(mydb).query_db(query,form_data)
    
#method to get one game from database by the id
    @classmethod
    def get_one(cls,id):
        query= '''
        SELECT *
        FROM games
        WHERE id = %(id)s;
        
        '''
        results = connectToMySQL(mydb).query_db(query,id)
        print(results)
        return results[0]


#method to delete a game in the database
    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM games WHERE id = %(id)s;"
        return connectToMySQL(mydb).query_db(query,data)

#method to update a game in the database
    @classmethod
    def edit (cls, id):
        query = '''
        UPDATE games
        SET hometeam = %(hometeam)s,
        awayteam = %(awayteam)s,
        homescore=%(homescore)s,
        awayscore=%(awayscore)s,
        updated_at = NOW()
        WHERE id = %(id)s;
        '''
        return connectToMySQL(mydb).query_db(query, id)