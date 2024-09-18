from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from app.diagnosis.models import Diagnosis
from app import db

class DiagnosisSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Diagnosis
        sqla_session = db.session  # 使用 SQLAlchemy session
        load_instance = True  # 允许将反序列化的字典直接加载为模型实例

    id = fields.Number(dump_only=True)  # ID 是只读字段
    video = fields.String(required=True)  # 新增的 video 字段，必填
    description = fields.String(required=True)  # Diagnosis 的描述字段，必填
    suggestion = fields.String(allow_none=True)  # 新增的 suggestion 字段，可选
    date = fields.DateTime(dump_only=True)  # 自动生成的日期字段
    patient_id = fields.Integer(allow_none=True)  # 引用的 patient_id，现在是可选字段

# 单个和多个诊断实例的序列化对象
diagnosis_schema = DiagnosisSchema()
diagnoses_schema = DiagnosisSchema(many=True)
