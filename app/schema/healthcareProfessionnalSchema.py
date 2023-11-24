from marshmallow import Schema, fields, validate
from schema.FieldObjectId import FieldObjectId


class HealthcareProfessionnalSchema(Schema):
    _id = FieldObjectId()
    name = fields.Str(required=True, validate=validate.Length(min=1))
    status = fields.Str(required=True, validate=validate.OneOf(["healthcare_professionnal"]))
    type = fields.Str(required=True, validate=validate.OneOf(["general_practitionner", "neurologist", "psychologist"]))