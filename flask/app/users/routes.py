from flask import request
from flask_jwt_extended import create_access_token
from app import db
from marshmallow import ValidationError
from app.users import users_bp
from app.users.models import User 
from app.users.schema import UserSchema
from app.patient.schema import PatientSchema
from app.patient.models import Patient
from app.utils.responses import response_with
from app.utils import responses as resp
from flask_jwt_extended import jwt_required, get_jwt_identity

@users_bp.route('/search', methods=['GET'])
def get_patient_by_doctor_and_name():
    """
    根据doctor_id和名字获取指定病人的信息。
    ---
    tags:
      - User
    summary: 根据doctor_id和名字获取指定病人的信息
    description: 根据doctor_id和名字获取指定病人的信息。
    parameters:
      - in: query
        name: name
        type: string
        required: true
        description: 要搜索的患者的名字
      - in: query
        name: doctor_id
        type: integer
        required: true
        description: 医生的ID
    produces:
      - application/json
    responses:
      200:
        description: 成功获取患者信息
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
                    description: 患者的医疗历史
                  email:
                    type: string
                  doctor_id:
                    type: integer
                  status:
                    type: string
                    description: 患者的状态（已就诊/未就诊）
      404:
        description: 没有找到匹配的患者
    """
    try:
        # 获取查询参数中的doctor_id和name
        doctor_id = request.args.get('doctor_id')
        name = request.args.get('name')
        
        if not doctor_id or not name:
            return response_with(resp.INVALID_INPUT_422, message="Both doctor_id and name query parameters are required.")
        
        # 查询时加上doctor_id和name的过滤条件
        fetched = Patient.query.filter(Patient.name.ilike(f"%{name}%"), Patient.doctor_id == doctor_id).all()
        
        if not fetched:
            return response_with(resp.SUCCESS_200, value={"patients": []})
        
        # 序列化查询结果
        patient_schema = PatientSchema(many=True)
        patients = patient_schema.dump(fetched)
        return response_with(resp.SUCCESS_200, value={"patients": patients})
    except Exception as e:
        print(f"Error fetching patients by doctor_id and name: {str(e)}")
        return response_with(resp.INVALID_INPUT_422)


@users_bp.route('/<int:doctor_id>/patients', methods=['GET'])
def get_patients_by_doctor(doctor_id):
    """
    获取指定医生的所有病人信息。
    ---
    tags:
      - User
    summary: 获取指定医生的所有病人信息
    description: 获取指定医生的所有病人信息。
    parameters:
      - in: path
        name: doctor_id
        required: true
        type: integer
        description: 医生的唯一标识符
    produces:
      - application/json
    responses:
      200:
        description: 成功获取病人列表
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
                  doctor:
                    type: object
                    properties:
                      id:
                        type: integer
                      username:
                        type: string
                  status:
                    type: string
                    description: 患者的状态（已就诊/未就诊）
      404:
        description: 医生未找到
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
    doctor = User.query.get_or_404(doctor_id)
    patients = Patient.query.filter_by(doctor_id=doctor_id).all()
    patient_schema = PatientSchema(many=True)
    result = patient_schema.dump(patients)
    return response_with(resp.SUCCESS_200, value={"patients": result})

# 注册
@users_bp.route('/register', methods=['POST'])
def create_user():
    """
    用户注册接口
    ---
    parameters:
        - in: body
          name: body
          schema:
            required:
                - username
                - password
            properties:
                username:
                    type: string
                    description: 用户名
                    default: ""
                password:
                    type: string
                    description: 用户密码
                    default: ""
    responses:
        201:
            description: 注册成功
            schema:
                properties:
                    code:
                        type: string
        422:
            description: 注册失败
            schema:
                properties:
                    code:
                        type: string
                    message:
                        type: string
    """
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return response_with(resp.INVALID_INPUT_422, value={"error": "Missing required fields"})

        data['password'] = User.generate_hash(data['password'])  # 哈希密码

        # 初始化 schema 并验证数据
        user_schema = UserSchema()
        validated_data = user_schema.load(data)  # 这是一个经过验证的字典

        # 创建用户实例
        user = User(**validated_data)
        db.session.add(user)  # 将用户实例添加到数据库会话
        db.session.commit()  # 提交数据库会话

        return response_with(resp.SUCCESS_201, value={"user": user_schema.dump(user)})
    
    except ValidationError as err:
        return response_with(resp.INVALID_INPUT_422, value={"errors": err.messages})
    except Exception as e:
        print(f"Error: {e}")
        return response_with(resp.INVALID_INPUT_422, value={"error": str(e)})

    
    

# 登录
@users_bp.route('/login', methods=['POST'])
def authenticate_user():
    """
    用户登录接口
    ---
    parameters:
        - in: body
          name: body
          schema:
            required:
                - username
                - password
            properties:
                username:
                    type: string
                    description: 用户名
                    default: ""
                password:
                    type: string
                    description: 用户密码
                    default: ""
    responses:
        201:
            description: 登录成功
            schema:
                properties:
                    message:
                        type: string
                    access_token:
                        type: string
                    id:
                        type: integer
        401:
            description: 未授权
            schema:
                properties:
                    error:
                        type: string
    """
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return response_with(resp.INVALID_INPUT_422, value={"error": "Missing required fields"})

        current_user = User.find_by_username(data['username'])
        if not current_user:
            return response_with(resp.SERVER_ERROR_404, value={"error": "User not found"})

        if User.verify_hash(data['password'], current_user.password):
            # 使用用户的 ID 创建访问令牌
            access_token = create_access_token(identity=current_user.id)
            
            # 返回用户的 ID 和访问令牌
            return response_with(resp.SUCCESS_201, value={
                'message': 'Logged in as {}'.format(current_user.username), 
                "access_token": access_token,
                "id": current_user.id  # 在响应中包含用户的 ID
            })
        else:
            return response_with(resp.UNAUTHORIZED_401, value={"error": "Invalid password"})
    except Exception as e:
        print(f"Error: {e}")
        return response_with(resp.INVALID_INPUT_422, value={"error": str(e)})
