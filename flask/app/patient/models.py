from app import db

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    medical_history = db.Column(db.Text)
    email = db.Column(db.String(120), unique=True)
    created = db.Column(db.DateTime, server_default=db.func.now())

    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='未就诊')  # 添加状态字段，默认值为 "未就诊"

    def __init__(self, name, age, gender, medical_history, email, doctor_id, status='未就诊'):
        self.name = name
        self.age = age
        self.gender = gender
        self.medical_history = medical_history
        self.email = email
        self.doctor_id = doctor_id
        self.status = status

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    @property
    def doctor(self):
        from app.users.models import User  # 延迟导入
        return db.relationship('User', backref=db.backref('patients', lazy=True))
