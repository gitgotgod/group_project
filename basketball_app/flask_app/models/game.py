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
            this_team = cls(team)
            user_data = {
                "id": team['users.id'],
                "firstname": team['firstname'],
                "lastname": team['lastname'],
                "email": team['email'],
                "password": "",
                "created_at": team['users.created_at'],
                "updated_at": team['users.updated_at']
            }
            this_team.creator = User(user_data)
            games.append(this_team)
        return games

    @classmethod
    def save(cls, form_data):
        query = """
                INSERT INTO games (hometeam,homescore,awayteam,awayscore,user_id)
                VALUES (%(hometeam)s,%(homescore)s,%(awayteam)s,%(awayscore)s,%(user_id)s);
                """
        return connectToMySQL(mydb).query_db(query,form_data)
    
    @classmethod
    def get_one(cls,data):
        query = """
                SELECT * FROM games
                JOIN users on games.user_id = users.id
                WHERE games.id = %(id)s;
                """
        result = connectToMySQL(mydb).query_db(query,data)
        if not result:
            return False

        result = result[0]
        this_team = cls(result)
        user_data = {
                "id": result['users.id'],
                "firstname": result['firstname'],
                "lastname": result['lastname'],
                "email": result['email'],
                "password": "",
                "created_at": result['users.created_at'],
                "updated_at": result['users.updated_at']
        }
        this_team.creator = User(user_data)
        return this_team

    @classmethod
    def update(cls,data):
        query = "UPDATE games SET hometeam=%(hometeam)s,homescore=%(homescore)s,awayteam=%(awayteam)s,awayscore=%(awayscore)s,created_at=NOW(),updated_at=NOW() WHERE user_id = %(user_id)s;"
        return connectToMySQL(mydb).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM games WHERE id = %(id)s;"
        return connectToMySQL(mydb).query_db(query,data)