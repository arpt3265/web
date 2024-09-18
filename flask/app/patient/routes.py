from flask import request ,jsonify
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.patient import patient_bp
from app.patient.models import Patient
from app.users.models import User
from app.patient.schema import PatientSchema
from app.utils.responses import response_with
from app.utils import responses as resp
from marshmallow import ValidationError

@patient_bp.route('/', methods=['POST'])
@jwt_required()
def create_patient():
    """
    创建一个新的患者记录。
    ---
    tags:
      - Patient
    summary: 创建一个新的患者记录
    description: 创建一个新的患者记录。
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: 患者信息
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              description: 患者的姓名
            age:
              type: integer
              description: 患者的年龄
            gender:
              type: string
              description: 患者的性别
            medical_history:
              type: string
              description: 患者的医疗历史
            email:
              type: string
              description: 患者的电子邮件
    responses:
      201:
        description: 成功创建患者记录
        schema:
          type: object
          properties:
            code:
              type: string
            patient:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                age:
                  type: integer
                gender:
                  type: string
                medical_history:
                  type: string
                email:
                  type: string
                doctor_id:
                  type: integer
                status:
                  type: string
      422:
        description: 输入数据无效
        schema:
          type: object
          properties:
            code:
              type: string
            message:
              type: string
    """
    try:
        # 从JWT令牌中提取用户ID
        user_id = get_jwt_identity()
        
        # 获取请求数据
        data = request.get_json()
        print("Received data before adding doctor_id:", data)
        
        # 设置doctor_id为当前用户的ID
        data['doctor_id'] = user_id  # 使用用户的ID作为doctor_id
        
        # 调试输出
        print("Received data:", data)

        # 通过schema验证并加载数据
        patient_schema = PatientSchema()
        patient = patient_schema.load(data)

        # 将患者记录保存到数据库
        db.session.add(patient)
        db.session.commit()

        result = patient_schema.dump(patient)
        return response_with(resp.SUCCESS_201, value={"patient": result})
    except ValidationError as err:
        # 调试输出
        print("Validation Error:", err.messages)
        return jsonify({"code": "invalidInput", "message": str(err.messages)}), 422
    except Exception as e:
        # 调试输出
        print(f"Error: {e}")
        return response_with(resp.INVALID_INPUT_422, value={"error": str(e)})

# 获取患者列表 (Get Patient List)
@patient_bp.route('/', methods=['GET'])
def get_patient_list():
    """
    获取所有患者的列表。
    ---
    tags:
      - Patient
    summary: 获取所有患者的列表
    description: 获取所有患者的列表。
    produces:
      - application/json
    responses:
      200:
        description: 成功获取患者列表
        schema:
          type: object
          properties:
            code:
              type: string
            message:
              type: string
            patients:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  name:
                    type: string
                  age:
                    type: integer
                  gender:
                    type: string
                  medical_history:
                    type: string
                  email:
                    type: string
                  doctor_id:
                    type: integer
                  status:
                    type: string
    """
    try:
        fetched = Patient.query.all()
        patient_schema = PatientSchema(many=True)
        patients = patient_schema.dump(fetched)
        return response_with(resp.SUCCESS_200, value={"patients": patients})
    except Exception as e:
        return response_with(resp.INVALID_INPUT_422)

#根据id获取病人信息
@patient_bp.route('/<int:id>', methods=['GET'])
def get_patient_by_id(id):
    """
    根据病人ID获取病人详细信息。
    ---
    tags:
      - Patient
    summary: 根据病人ID获取病人详细信息
    description: 根据病人ID获取病人详细信息。
    produces:
      - application/json
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: 病人ID
    responses:
      200:
        description: 成功获取病人详细信息
        schema:
          type: object
          properties:
            code:
              type: string
            message:
              type: string
            patient:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                age:
                  type: integer
                gender:
                  type: string
                medical_history:
                  type: string
                email:
                  type: string
                doctor_id:
                  type: integer
                status:
                  type: string
      404:
        description: 病人未找到
        schema:
          type: object
          properties:
            code:
              type: string
            message:
              type: string
    """
    try:
        patient = Patient.query.get(id)
        if patient:
            patient_schema = PatientSchema()
            patient_data = patient_schema.dump(patient)
            return response_with(resp.SUCCESS_200, value={"patient": patient_data})
        else:
            return response_with(resp.NOT_FOUND_404, message="Patient not found")
    except Exception as e:
        return response_with(resp.INVALID_INPUT_422)



# 更新患者详情 (Update Patient Detail)
@patient_bp.route('/<int:id>', methods=['PUT'])
def update_patient_detail(id):
    """
    更新指定患者的所有信息。
    ---
    tags:
      - Patient
    summary: 更新指定患者的所有信息
    description: 更新指定患者的所有信息。
    parameters:
      - in: path
        name: id
        required: true
        type: integer
        description: 患者的唯一标识符
      - in: body
        name: body
        description: 更新的患者信息
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              description: 患者的姓名
            age:
              type: integer
              description: 患者的年龄
            gender:
              type: string
              description: 患者的性别
            medical_history:
              type: string
              description: 患者的医疗历史
            email:
              type: string
              description: 患者的电子邮件
            doctor_id:
              type: integer
              description: 医生的唯一标识符
            status:
              type: string
              description: 患者的状态
    responses:
      200:
        description: 成功更新患者记录
        schema:
          type: object
          properties:
            code:
              type: string
            message:
              type: string
            patient:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                age:
                  type: integer
                gender:
                  type: string
                medical_history:
                  type: string
                email:
                  type: string
                doctor_id:
                  type: integer
                status:
                  type: string
      404:
        description: 患者未找到
        schema:
          type: object
          properties:
            code:
              type: string
            error:
              type: string
            message:
              type: string
    """
    try:
        data = request.get_json()
        get_patient = Patient.query.get_or_404(id)

        # 更新患者信息
        if 'name' in data:
            get_patient.name = data['name']
        if 'age' in data:
            get_patient.age = data['age']
        if 'gender' in data:
            get_patient.gender = data['gender']
        if 'medical_history' in data:
            get_patient.medical_history = data['medical_history']
        if 'email' in data:
            get_patient.email = data['email']
        if 'doctor_id' in data:
            get_patient.doctor_id = data['doctor_id']  # 更新 doctor_id
        if 'status' in data:
            get_patient.status = data['status']  # 更新 status

        # 提交更改到数据库
        db.session.commit()

        # 序列化患者数据
        patient_schema = PatientSchema()
        patient = patient_schema.dump(get_patient)
        
        return response_with(resp.SUCCESS_200, value={"patient": patient})
    
    except Exception as e:
        # 捕获异常并返回错误响应
        return response_with(resp.INVALID_INPUT_422, value={"code": "updateError", "message": str(e)})


# 修改患者部分信息 (Modify Patient Detail)
@patient_bp.route('/<int:id>', methods=['PATCH'])
def modify_patient_detail(id):
    """
    修改指定患者的部分信息，包括 doctor_id 和 status。
    ---
    tags:
      - Patient
    summary: 修改指定患者的部分信息
    description: 修改指定患者的部分信息，包括 doctor_id 和 status。
    parameters:
      - in: path
        name: id
        required: true
        type: integer
        description: 患者的唯一标识符
      - in: body
        name: body
        description: 部分患者信息
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              description: 患者的姓名
            age:
              type: integer
              description: 患者的年龄
            gender:
              type: string
              description: 患者的性别
            medical_history:
              type: string
              description: 患者的医疗历史
            email:
              type: string
              description: 患者的电子邮件
            doctor_id:
              type: integer
              description: 患者的医生ID
            status:
              type: string
              description: 患者的状态
    responses:
      200:
        description: 成功修改患者记录
        schema:
          type: object
          properties:
            code:
              type: string
            message:
              type: string
            patient:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                age:
                  type: integer
                gender:
                  type: string
                medical_history:
                  type: string
                email:
                  type: string
                doctor_id:
                  type: integer
                status:
                  type: string
      404:
        description: 患者未找到
        schema:
          type: object
          properties:
            code:
              type: string
            error:
              type: string
            message:
              type: string
    """
    data = request.get_json()
    get_patient = Patient.query.get(id)
    
    if not get_patient:
        return response_with(resp.NOT_FOUND_404, value={"code": "notFound", "message": "Patient not found"})

    if 'name' in data:
        get_patient.name = data['name']
    if 'age' in data:
        get_patient.age = data['age']
    if 'gender' in data:
        get_patient.gender = data['gender']
    if 'medical_history' in data:
        get_patient.medical_history = data['medical_history']
    if 'email' in data:
        get_patient.email = data['email']
    if 'doctor_id' in data:
        doctor = User.query.get(data['doctor_id'])
        if doctor is None:
            return response_with(resp.NOT_FOUND_404, value={"code": "notFound", "message": "Doctor not found"})
        get_patient.doctor_id = data['doctor_id']
    if 'status' in data:
        get_patient.status = data['status']  # 更新 status
    
    db.session.commit()
    
    patient_schema = PatientSchema()
    patient = patient_schema.dump(get_patient)
    
    return response_with(resp.SUCCESS_200, value={"patient": patient})


# 删除患者 (Delete Patient)
@patient_bp.route('/<int:id>', methods=['DELETE'])
def delete_patient(id):
    """
    删除指定患者的记录。
    ---
    tags:
      - Patient
    summary: 删除指定患者的记录
    description: 删除指定患者的记录。
    parameters:
      - in: path
        name: id
        required: true
        type: integer
        description: 患者的唯一标识符
    responses:
      204:
        description: 成功删除患者记录
      404:
        description: 患者未找到
        schema:
          type: object
          properties:
            code:
              type: string
            error:
              type: string
            message:
              type: string
    """
    get_patient = Patient.query.get(id)
    if not get_patient:
        return response_with(resp.ERROR_404, value={"error": "Patient not found", "message": "Patient not found"})
    
    db.session.delete(get_patient)
    db.session.commit()
    return response_with(resp.SUCCESS_204)  # 204 No Content
