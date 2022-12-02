from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Magazine:
    db_name = 'magazines'
    def __init__(self,data):
        self.id = data['id'],
        self.title = data['tittle'],
        self.description = data['description'],
        self.created_at = data['created_at'],
        self.updated_at = data['updated_at']

    
    @classmethod
    def addMagazine(cls,data):
        query = 'INSERT INTO magazines ( tittle, description, user_id ) VALUES ( %(tittle)s, %(description)s, %(user_id)s );'
        return connectToMySQL(cls.db_name).query_db(query,data)

    
    @classmethod
    def getMagazineByID(cls,data):
        query = 'SELECT * FROM magazines LEFT JOIN users ON magazines.user_id = users.id WHERE magazines.id = %(magazine_id)s;'
        result = connectToMySQL(cls.db_name).query_db(query,data)
        return result[0]


    @classmethod
    def getAllMagazines(cls,data):
        query = 'SELECT magazines.tittle, magazines.id, users.first_name FROM magazines LEFT JOIN users on magazines.user_id = users.id;'
        result = connectToMySQL(cls.db_name).query_db(query, data)
        magazines = []
        for row in result:
            magazines.append(row)
        return magazines

    @classmethod
    def getSubsCount(cls,data):
        query = 'SELECT count(subscriptions.id) as number FROM subscriptions LEFT JOIN magazines ON subscriptions.magazine_id = magazines.id WHERE magazines.id = %(magazine_id)s GROUP BY magazine.id;'
        result = connectToMySQL(cls.db_name).query_db(query,data)
        return result[0]

    @classmethod
    def subscribeMagazine(cls,data):
        query = 'INSERT INTO subscriptions ( magazine_id, user_id ) VALUES ( %(magazine_id)s, %(user_id)s ); '
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def unsubscribeMagazine(cls,data):
        query = 'DELETE FROM subscriptions WHERE magazine_id = %(magazine_id)s AND user_id = %(user_id)s;'
        return connectToMySQL(cls.db_name).query_db(query,data)
    

    @classmethod
    def destroyMagazine(cls,data):
        query = 'DELETE FROM magazines WHERE magazines.id = %(magazine_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)


    @staticmethod
    def validata_magazine(magazine):
        is_valid = True
        if len(magazine['tittle']) < 2:
            flash("Tittle should be at least 2 characters long", 'tittle')
            is_valid = False
        if len(magazine['description']) < 10:
            flash("Description should be at least 10 characters  long", 'description')
            is_valid = False
        return is_valid