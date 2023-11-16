from flask import jsonify, make_response
from flask_restful import Resource, reqparse
from models import Role, User, db
from flask import current_app as app
import jwt
from sqlalchemy.exc import IntegrityError
from auth import auth_req
from werkzeug.security import generate_password_hash, check_password_hash

class Login(Resource):
    def get(self):
        return jsonify({'message': 'Welcome to login!'})
    
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str, help="Email of the user")
            parser.add_argument('password', type=str, help='Password to create user')
            args = parser.parse_args()
            print(args)
            user = User.query.filter_by(email=args['email']).first()
            if user is None:
                return {'err': 'User doesn\'t exist'}, 400
            if user.email == args['email'] and check_password_hash(user.password_hash, args['password']):
                token = jwt.encode({'user': user.id, 'role':1}, app.config['SECRET_KEY'],algorithm="HS256")

                return make_response({"message": token}, 200)
            else:
                return make_response({'err': 'Wrong Password'}, 400)
        except Exception as e:
            print(e)
            return make_response({'err': 'Something went wrong'}, 500)
    
class AdminLogin(Resource):
    def get(self):
        return jsonify({'message': 'Welcome to login!'})
    
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str, help="Email of the user")
            parser.add_argument('password', type=str, help='Password to create user')
            args = parser.parse_args()
            print(args)
            user = User.query.filter_by(email=args['email']).first()
            if user is None:
                return {'err': 'User doesn\'t exist'}, 400
            if user.email == args['email'] and check_password_hash(user.password_hash, args['password']):
                if user.role_id == 2:
                    token = jwt.encode({'user': user.id, 'role':2}, app.config['SECRET_KEY'],algorithm="HS256")
                    return make_response({"message": token}, 200)
                else:
                    return make_response({'err': 'You are not an admin'}, 400)
            else:
                return make_response({'err': 'Wrong Password'}, 400)
        except Exception as e:
            print(e)
            return make_response({'err': 'Something went wrong'}, 500)

class Signup(Resource):
    
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str, help='Username to create user')
            parser.add_argument('email', type=str, help='Email to create user')
            parser.add_argument('password', type=str, help='Password to create user')
            parser.add_argument('role_id', type=int, help='Role to create user')
            args = parser.parse_args()
            if args['email'] is None:
                return {"err": "Email field is empty"}
            if args['username'] is None:
                return {"err": "Username field is empty"}
            if args['password'] is None:
                return {"err": "Password field is empty"}
            role_id = 1
            if(args['role_id'] is not None):
                role_id = args['role_id']
            password = generate_password_hash(args['password'])
            new_user = User(username=args['username'], email=args['email'], password_hash=password, role_id=role_id)
            db.session.add(new_user)
            db.session.commit()
            return {'message': 'User {} created'.format(args['username'])}, 200
        except IntegrityError as e:
            print(e)
            db.session.rollback()
            return make_response({"err": "An user with this email already exists"})
        except Exception as e:
            db.session.rollback()
            print(e)
            return make_response({"err": "Something went wrong"})
        

class Roles(Resource):
    method_decorators = {'get': [auth_req], 'post': [auth_req]}
    def get(self):
        roles = Role.query.all()
        return [role.serialize() for role in roles]
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, help='Name of role')
            args = parser.parse_args()
            new_role = Role(name=args['name'])
            db.session.add(new_role)
            db.session.commit()
            return {'message': 'Role {} created'.format(args['name'])}, 200
        except IntegrityError as e:
            db.session.rollback()
            return make_response({"err": "Role Already Exists"})
        except Exception as e:
            db.session.rollback()
            print(e)
            return make_response({"err": "Something went wrong!!"})