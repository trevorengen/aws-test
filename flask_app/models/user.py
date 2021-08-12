from flask_app.config.mysqlcontroller import connectToMySQL
from flask import flash
import re

DB = 'users_schema'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
INVALID_CHARS = re.compile(r'[\';<>\"]')
NUMS = re.compile(r'[0-9]')
CAPS = re.compile(r'[A-Z]')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_login_input(input):
        is_valid = True
        x = lambda s: INVALID_CHARS.match(s)
        if not EMAIL_REGEX.match(input['email']) or x('email'):
            if x('email'):
                flash(u'Invalid characters. Please don\'t use [\';<>"]', 'login')
                is_valid = False
            else:
                flash(u'Invalid email address.', 'login')
                is_valid = False
        if len(input['password']) < 8 or len(input['password']) > 30 or x('password'):
            if x('password'):
                flash(u'Invalid characters. Please don\'t use [\';<>"]', 'login')
                is_valid = False
            else:
                flash(u'Password must be between 8-30 characters.', 'login')
                is_valid = False
        return is_valid


    @staticmethod
    def validate_register_input(input):
        is_valid = True
        x = lambda s: INVALID_CHARS.match(s)
        if len(input['first_name']) < 3 or len(input['first_name']) > 25 or x('first_name'):
            if x('first_name'):
                flash(u'Invalid characters. Please don\'t use [\';<>"]', 'register')
                is_valid = False
            else:
                flash(u'First name must be between 2-25 characters.', 'register')
                is_valid = False
        if len(input['last_name']) < 3 or len(input['last_name']) > 25 or x('last_name'):
            if x('last_name'):
                flash(u'Invalid characters. Please don\'t use [\';<>"]', 'register')
                is_valid = False
            else:
                flash(u'Last name must be between 2-25 characters.', 'register')
                is_valid = False
        if not EMAIL_REGEX.match(input['email']) or x('email'):
            if x('email'):
                flash(u'Invalid characters. Please don\'t use [\';<>"]', 'register')
                is_valid = False
            else:
                flash(u'Invalid email address.', 'register')
                is_valid = False
        if len(input['password']) < 8 or len(input['password']) > 30 or x('password'):
            if x('password'):
                flash(u'Invalid characters. Please don\'t use [\';<>"]', 'register')
                is_valid = False
            else:
                flash('Password must be between 8-30 characters.', 'register')
                is_valid = False
        if input['password'] != input['confirm_password']:
            flash(u'Passwords must match.' 'register')
            is_valid = False
        if not NUMS.match(input['password']) or not CAPS.match(input['password']):
            flash(u'Password must have at least one uppercase letter and one number.', 'register')
            is_valid = False
        
        return is_valid
        
    @classmethod
    def save(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password) '
        query += 'VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'
        user_id = connectToMySQL(DB).query_db(query, data)
        return user_id

    @classmethod
    def get_user(cls, data):
        if 'email' in data:
            query = 'SELECT * FROM users WHERE email = %(email)s;'
        elif 'id' in data:
            query = 'SELECT * FROM users WHERE id = %(id)s;'
        else:
            return
        try:
            result = connectToMySQL(DB).query_db(query, data)
            user = cls(result[0])
            return user
        except Exception as e:
            print('WARNING', e)
            return False