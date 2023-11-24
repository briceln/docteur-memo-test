from werkzeug.security import check_password_hash
from marshmallow import ValidationError
from bson.objectid import ObjectId

from schema.createUserSchema import CreateUserSchema
from models.user import User
from models.healthcareProfessionnal import HealthcareProfessionnal
from models.patient import Patient
from models.caregiver import Caregiver

class UserFactory:
    """ @staticmethod
    def build(id):
        if not ObjectId.is_valid(id):
            return None

        db = User.get_user_collection()

        filter = {'_id': ObjectId(id)}

        user_data = db.find_one(filter)
        if user_data is None:
            return None

        user = None
        status = user_data['status']
        if (status == 'patient'):
            user = Patient(user_data)
        elif status == 'caregiver':
            user = Caregiver(user_data)
        elif status == 'healthcare_professionnal':
            user = HealthcareProfessionnal(user_data)
        return user"""
    
    @staticmethod
    def create(data):
        schema = CreateUserSchema()
        schema.load(data)
        
        user_status = data['status']
        username = data['username']

        db = User.get_user_collection()
        filter = {'name': username}

        if db.count_documents(filter) > 0:
            raise ValidationError(message=['User already exist'], field_name='username')

        id = None
        if user_status == 'caregiver':
            id = Caregiver().create(data)
        elif user_status == 'patient':
            id = Patient().create(data)
        elif user_status == 'healthcare_professionnal':
            id = HealthcareProfessionnal().create(data)
        return id
    
    @staticmethod
    def login(username, password):
        db = User.get_user_collection()

        user = db.find_one({'name': username})

        if user is None:
            raise ValidationError(message=['Wrong username or password.'])
        
        if not check_password_hash(user['password'], password):
            raise ValidationError(message=['Wrong username or password.'])
        return user