from marshmallow import Schema, fields, validate, EXCLUDE


class CredentialsSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=1))
    password = fields.Str(required=True, validate=[validate.Length(min=6, max=36)], load_only=True)

    class Meta:
        unknown = EXCLUDE