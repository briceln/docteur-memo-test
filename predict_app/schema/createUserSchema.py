from marshmallow import Schema, fields, validate, EXCLUDE
from schema.credentialsSchema import CredentialsSchema


class CreateUserSchema(CredentialsSchema):
    status = fields.Str(required=True, validate=validate.OneOf(["caregiver", "patient", "healthcare_professionnal"]))

    class Meta:
        unknown = EXCLUDE