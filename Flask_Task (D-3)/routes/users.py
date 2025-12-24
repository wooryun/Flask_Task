from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from db import db
from models import User

user_blp = Blueprint('Users', 'users', description='Operations on users', url_prefix='/users')


@user_blp.route('/', strict_slashes=False)
class UserList(MethodView):
    def get(self):
        users = User.query.all()
        user_data = [{"id":user.id, 
                    "name": user.name, 
                    "email": user.email
                    } for user in users] 
        return jsonify(user_data)

    def post(self):
        user_data = request.json
        new_user = User(name=user_data['name'], 
                        email=user_data['email'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg": "Success create new user", "id": new_user.id}), 201


@user_blp.route('/<int:user_id>') 
class Users(MethodView):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return jsonify({"name": user.name, 'email': user.email})

    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        data = request.json

        user.name = data['name']
        user.email = data['email']

        db.session.commit()
        return jsonify({"msg": "Success update user", "id": user.id}), 200

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"msg": "Success delete user", "id": user_id}), 200