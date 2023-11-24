from marshmallow import Schema, fields, validate
from schema.FieldObjectId import FieldObjectId


class PatientSchema(Schema):
    _id = FieldObjectId()
    name = fields.Str(required=True, validate=validate.Length(min=1))
    status = fields.Str(required=True, validate=validate.OneOf(["patient"]))
    age = fields.Int(required=True, validate=validate.Range(min=0, max=120))
    memory_score = fields.Int(required=True, validate=validate.Range(min=-999, max=999))