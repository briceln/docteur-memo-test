from marshmallow import Schema, fields, validate


class PredictPatientSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1))