from flask_app.config.mysqlconnection import connectToMySQL
import re	#regex thing
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from flask import flash



class User: 
    db_name = 'magazines'
    def __init__(self,data):
        self.id = data['id'],
        self.first_name = data['first_name'],
        self.last_name = data['last_name'],
        self.email = data['email'],
        self.password = data['password'],
        self.created_at = data['created_at'],
        self.updated_at = data['updated_at']
    

    @classmethod
    def addUser(cls,data):
        query = 'INSERT INTO users ( first_name, last_name, email, password ) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s );'
        return connectToMySQL(cls.db_name).query_db(query,data)


    @classmethod
    def getUserByID(cls,data):
        query = 'SELECT * FROM users WHERE id = %(user_id)s;'
        result = connectToMySQL(cls.db_name).query_db(query,data)
        return result[0]

    @classmethod
    def getUserByEmail(cls,data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        result = connectToMySQL(cls.db_name).query_db(query,data)
        if result:
            return result[0]
        return False
        

    @classmethod
    def subscribeUnsubcribe(cls,data):
        query = 'SELECT magazine_id as id FROM subscriptions LEFT JOIN users ON subscriptions.user_id = users.id WHERE user_id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        subs = []
        for row in results:
            subs.append(row['id'])
        return subs

    @classmethod
    def getUsersMagazines(cls,data):
        query = 'SELECT magazines.tittle FROM magazines LEFT JOIN users ON magazines.user_id = users.id WHERE users.id = %(user_id)s;'
        result = connectToMySQL(cls.db_name).query_db(query,data)
        magazines = []
        for row in result:
            magazines.append(row)
        return magazines


    @classmethod
    def updateUser(cls,data):
        query = 'UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE users.id = %(user_id)s;'
        return connectToMySQL(cls.db_name).query_db(query,data)



    #method to validate user
    @staticmethod
    def validate_user(user):
        is_valid = True  #we assume this is true so if there is nothing wrong in the login-register no flash will appear
        if len(user['first_name']) < 3:
            flash("First name must have at least 3 characters", 'first_name')
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must have at least 3 characters", 'last_name') 
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): #the email is not like this someone@something.something
            flash("Invalid email address!", 'emailRegister')
            is_valid = False
        if len(user['password']) < 8: 
            flash("Password must be at least 8 characters long!", 'passwordRegister')
            is_valid = False
        if user['password']!=user['confirmPassword']: 
            flash("Passwords do not match", 'passwordConfirm')
            is_valid = False
        return is_valid


    @staticmethod
    def validate_updated_user(user):
        is_valid = True
        if len(user['first_name']) < 3:
            flash("First name must have at least 3 characters", 'first_name')
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must have at least 3 characters", 'last_name') 
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): #the email is not like this someone@something.something
            flash("Invalid email address!", 'emailUpdate')
            is_valid = False
        return is_valid