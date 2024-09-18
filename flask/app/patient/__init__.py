from flask import Blueprint
patient_bp = Blueprint('patient_bp',__name__)
from app.patient import routes