from app import db
from app.patient.models import Patient  # 引用 Patient 模型

class Diagnosis(db.Model):
    __tablename__ = 'diagnoses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 必须字段
    video = db.Column(db.String(255), nullable=False)  # 存储本地视频文件路径
    description = db.Column(db.Text, nullable=False)  # 必须字段
    suggestion = db.Column(db.Text, nullable=True)  # 可为空字段
    date = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)  # 必须字段
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=True)  # 可为空字段

    # 建立与 Patient 模型的关系
    patient = db.relationship('Patient', backref=db.backref('diagnoses', lazy=True))

    def __init__(self, video, description, suggestion=None, patient_id=None):
        self.video = video  # 本地视频文件路径
        self.description = description
        self.suggestion = suggestion
        self.patient_id = patient_id

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
