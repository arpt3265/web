from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask import Flask, jsonify, make_response
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema 
from marshmallow import fields
from flask import request


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# 作者信息模型
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    specialisation = db.Column(db.String(50))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, name, specialisation):
        self.name = name
        self.specialisation = specialisation

    def __repr__(self):
        return f'<Author {self.id}>'

# 序列化接口数据为 JSON 格式
class AuthorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Author
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    specialisation = fields.String(required=True)

@app.route('/authors', methods=['GET'])
def get_authors():
    get_authors = Author.query.all()
    author_schema = AuthorSchema(many=True)
    authors = author_schema.dump(get_authors)
    return make_response(jsonify({"authors": authors}))

@app.route('/authors/<id>',methods=['GET'])
def get_author_by_id(id):
    get_author = Author.query.get(id)
    author_schema = AuthorSchema()
    author = author_schema.dump(get_author)
    return make_response(jsonify({"author":author}))

@app.route('/authors/<id>',methods=['PUT'])
def update_author_by_id(id):
    data = request.get_json()
    get_author = Author.query.get(id)
    if data.get('specialisation'):
        get_author.specialisation = data['specialisation']

    if data.get('name'):
        get_author.name = data['name']

    db.session.add(get_author)
    db.session.commit()
    author_schema = AuthorSchema(only=['id','name','specialisation'])
    author = author_schema.dump(get_author)
    return make_response(jsonify({"author":author}))

@app.route('/authors',methods=['POST'])
def create_author():
    data = request.get_json()
    author_schema = AuthorSchema()
    
    # 将请求数据加载到 Author 实例中
    author_data = author_schema.load(data)
    author = Author(**author_data)  # 使用 **author_data 将字典解包为关键字参数
    
    # 调用 create 方法保存到数据库
    result = author.create()
    
    # 使用 author_schema.dump() 序列化保存后的实例
    result_data = author_schema.dump(result)
    return make_response(jsonify({"author": result_data}), 201)

@app.route('/authors/<id>',methods=['DELETE'])
def delete_author_by_id(id):
    get_author = Author.query.get(id)
    db.session.delete(get_author)
    db.session.commit()
    return make_response({"msg":"ok"},204)


if __name__ == '__main__':
    app.run(debug=True)
