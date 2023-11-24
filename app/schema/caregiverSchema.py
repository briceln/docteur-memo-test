from marshmallow import Schema, ValidationError, fields, validate, validates
from db import DatabaseSingleton
from schema.FieldObjectId import FieldObjectId

class CaregiverSchema(Schema):
    _id = FieldObjectId()
    name = fields.Str(required=True, validate=validate.Length(min=1))
    status = fields.Str(required=True, validate=validate.OneOf(["caregiver"]))
    related_patients = fields.List(FieldObjectId(), required=True)

    @validates('related_patients')
    def no_duplicate_patients(self, value):
        if len(value) != len(set(value)):
            raise ValidationError('related_patients must not contain duplicate elements')
        
    @validates('related_patients')
    def patients_exist(self, values):
        client = DatabaseSingleton().get_db_connection()
        db = client["memo"].user
        if db.count_documents({"$and":[{ '_id': { "$in": values}}, {"status": "patient"}]}) != len(values):
            raise ValidationError('related_patients contain unknown patients')