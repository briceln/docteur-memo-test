from schema.healthcareProfessionnalSchema import HealthcareProfessionnalSchema
from models.user import User

class HealthcareProfessionnal(User):

    _data = None

    def __init__(self, init_object = None):
        if init_object is None:
            return
        self.fill_values_from_db(init_object)

    def fill_values_from_db(self, data):
        schema = HealthcareProfessionnalSchema()
        self._data = schema.load(data)
    
    def check_create_values(self, values):
        values['name'] = values['username']
        values_cp = values.copy()
        values_cp.pop('username')
        values_cp.pop('password')
        schema = HealthcareProfessionnalSchema()
        return schema.load(values_cp)
    
    def create(self, values):
        healthcareProfessionnal = self.check_create_values(values)

        healthcareProfessionnal['password'] = super().hash_password(values['password'])

        db = User.get_user_collection()

        result = db.insert_one(healthcareProfessionnal)
        return result.inserted_id