from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from app.patient.models import Patient
from app import db

class PatientSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Patient
        sqla_session = db.session
        load_instance = True  # 允许将反序列化的字典直接加载为模型实例

    id = fields.Number(dump_only=True)
    name = fields.String(required=True)  # 使用单个name字段
    age = fields.Integer(required=True)
    gender = fields.String(required=True)
    medical_history = fields.String()
    email = fields.Email(required=True)
    created = fields.String(dump_only=True)
    doctor_id = fields.Integer()  # 确保这里是 Integer，而不是 Int
    status = fields.String(missing="未就诊")  # 添加status字段，默认值为"未就诊"
