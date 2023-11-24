from schema.patientSchema import PatientSchema
from models.user import User

class Patient(User):

    _data = None

    def __init__(self, init_object = None):
        if init_object is None:
            return
        self.fill_values_from_db(init_object)

    def fill_values_from_db(self, data):
        schema = PatientSchema()
        if 'password' in data:
            data.pop('password')
        self._data = schema.load(data)

    def get(self, username):
        db = User.get_user_collection()

        filter = {"$and":[{ 'name': username}, {"status": "patient"}]}

        user = db.find_one(filter)
        if user is None:
            return None

        self.fill_values_from_db(user)
        return True
    
    def dump(self):
        schema = PatientSchema()
        result = schema.load(self._data)
        return schema.dump(result)
    
    def check_create_values(self, values):
        values['name'] = values['username']
        values_cp = values.copy()
        values_cp.pop('username')
        values_cp.pop('password')
        schema = PatientSchema()
        return schema.load(values_cp)
    
    def create(self, values):
        patient = self.check_create_values(values)
        patient['password'] = super().hash_password(values['password'])

        db = User.get_user_collection()

        result = db.insert_one(patient)
        return result.inserted_id
    
    @staticmethod
    def count_patient(score, age = None, age_order = None):
        db = User.get_user_collection()

        if age is None:
            filter = {
                "$and":[
                    {
                        'memory_score': { '$gt': score }
                    },
                    {
                        "status": "patient"
                    }
            ]}

            return db.count_documents(filter)
        else:
            order = '$gt'
            if age_order == 'lt':
                order = '$lt'
            filter = {
                "$and":[
                    {
                        'memory_score': { '$gt': score }
                    },
                    {
                        "status": "patient"
                    },
                    {
                        'age': { order: age }
                    }
                ]}

            return db.count_documents(filter)