from flask import Blueprint
diagnosis_bp = Blueprint('diagnosis_bp',__name__)
from app.diagnosis import routes