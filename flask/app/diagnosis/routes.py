from flask import request, jsonify
from app import db
from app.diagnosis import diagnosis_bp
from app.diagnosis.models import Diagnosis
from app.diagnosis.schema import diagnosis_schema, diagnoses_schema
from app.utils.responses import response_with, INVALID_INPUT_422, SERVER_ERROR_404, SERVER_ERROR_500, SUCCESS_201, SUCCESS_200

from app.utils import responses as resp
from marshmallow import ValidationError
from app.patient.models import Patient  # Assuming you have a Patient model


@diagnosis_bp.route('/', methods=['POST'])
def create_diagnosis():
    """
    创建新的诊断记录。
    ---
    tags:
      - Diagnosis
    summary: 创建新的诊断记录
    description: 提供诊断描述和患者ID来创建新的诊断记录。
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            video:
              type: string
              example: "/path/to/video.mp4"
            description:
              type: string
              example: "这是一个测试诊断"
            suggestion:
              type: string
              example: "建议多休息"
            patient_id:
              type: integer
              example: 
    responses:
      201:
        description: 成功创建诊断记录
        schema:
          type: object
          properties:
            id:
              type: integer
            video:
              type: string
            description:
              type: string
            suggestion:
              type: string
            date:
              type: string
              format: date-time
            patient_id:
              type: integer
      422:
        description: 输入数据无效
        schema:
          type: object
          properties:
            code:
              type: string
            message:
              type: string
      500:
        description: 服务器内部错误
        schema:
          type: object
          properties:
            code:
              type: string
            message:
              type: string
    """

    try:
        data = request.json
        video = data.get('video')
        description = data.get('description')
        suggestion = data.get('suggestion')
        patient_id = data.get('patient_id')

        # 检查必填字段
        if not video or not description:
            return response_with(INVALID_INPUT_422, value={"error": "Missing required fields: video or description"})

        # 如果 patient_id 提供，检查患者是否存在
        if patient_id and not Patient.query.get(patient_id):
            return response_with(SERVER_ERROR_404, value={"error": "Patient not found"})

        # 创建诊断记录
        diagnosis = Diagnosis(video=video, description=description, suggestion=suggestion, patient_id=patient_id)
        db.session.add(diagnosis)
        db.session.commit()

        return response_with(SUCCESS_201, value={"diagnosis": diagnosis_schema.dump(diagnosis)})

    except ValidationError as err:
        print("Validation Error:", err.messages)
        return response_with(INVALID_INPUT_422, value={"error": str(err.messages)})

    except Exception as e:
        print(f"Error: {e}")
        return response_with(SERVER_ERROR_500, value={"error": str(e)})



@diagnosis_bp.route('/patient/<int:patient_id>', methods=['GET'])
def get_diagnoses_by_patient(patient_id):
    """
    根据患者ID获取所有诊断记录。
    ---
    tags:
      - Diagnosis
    summary: 根据患者ID获取所有诊断记录
    description: 根据患者ID获取所有与该患者相关的诊断记录的列表。
    produces:
      - application/json
    parameters:
      - name: patient_id
        in: path
        type: integer
        required: true
        description: 患者的唯一标识符
    responses:
      200:
        description: 成功获取诊断记录列表
        schema:
          type: object
          properties:
            diagnoses:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  video:
                    type: string
                  description:
                    type: string
                  suggestion:
                    type: string
                  date:
                    type: string
                    format: date-time
                  patient_id:
                    type: integer
      404:
        description: 未找到对应的诊断记录
        schema:
          type: object
          properties:
            code:
              type: string
            message:
              type: string
      500:
        description: 服务器内部错误
        schema:
          type: object
          properties:
            code:
              type: string
            message:
              type: string
    """
    try:
        diagnoses = Diagnosis.query.filter_by(patient_id=patient_id).all()
        if not diagnoses:
            return response_with(SERVER_ERROR_404, value={"error": "No diagnoses found for the given patient_id"})
        
        return response_with(SUCCESS_200, value={"diagnoses": diagnoses_schema.dump(diagnoses)})
    
    except Exception as e:
        print(f"Error: {e}")
        return response_with(SERVER_ERROR_500, value={"error": str(e)})
    
    
@diagnosis_bp.route('/', methods=['GET'])
def get_all_diagnoses():
    """
    获取所有诊断记录。
    ---
    tags:
      - Diagnosis
    summary: 获取所有诊断记录
    description: 获取数据库中所有诊断记录的列表。
    produces:
      - application/json
    responses:
      200:
        description: 成功获取诊断记录列表
        schema:
          type: object
          properties:
            diagnoses:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  video:
                    type: string
                  description:
                    type: string
                  suggestion:
                    type: string
                  date:
                    type: string
                    format: date-time
                  patient_id:
                    type: integer
      404:
        description: 未找到诊断记录
        schema:
          type: object
          properties:
            code:
              type: string
            message:
              type: string
      500:
        description: 服务器内部错误
        schema:
          type: object
          properties:
            code:
              type: string
            message:
              type: string
    """
    try:
        diagnoses = Diagnosis.query.all()
        if not diagnoses:
            return response_with(SERVER_ERROR_404, value={"error": "No diagnoses found"})
        
        return response_with(SUCCESS_200, value={"diagnoses": diagnoses_schema.dump(diagnoses)})
    
    except Exception as e:
        print(f"Error: {e}")
        return response_with(SERVER_ERROR_500, value={"error": str(e)})



