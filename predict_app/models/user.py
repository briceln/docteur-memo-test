from werkzeug.security import generate_password_hash
from db import DatabaseSingleton

class User:

    @staticmethod
    def get_user_collection():
        client = DatabaseSingleton().get_db_connection()
        db = client["memo"].user
        return db

    def get(self, id):
        raise TypeError('User.get function not implemented')

    def update(self):
        raise TypeError('User.update function not implemented')
    
    def save(self):
        raise TypeError('User.save function not implemented')
    
    def dump(self):
        raise TypeError('User.dump function not implemented')
    
    def fill_values_from_db(self, data):
        raise TypeError('User.fill_values_from_db function not implemented')

    def check_create_values(self, values):
        raise TypeError('User.check_create_values function not implemented')
    
    def create(self, values):
        raise TypeError('User.create function not implemented')
    
    def hash_password(self, password):
        hashed_password = generate_password_hash(password, method='sha256')
        return hashed_password
