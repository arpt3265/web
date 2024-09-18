
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from app.users.models import User
from app import db

class UserSchema(SQLAlchemyAutoSchema):
    class Meta(SQLAlchemyAutoSchema.Meta):
        model = User
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    username = fields.String(required=True)