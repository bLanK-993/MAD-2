from flask import request, make_response
from flask_restful import Api, Resource, reqparse
from models import User, db
from auth import auth_req
from sqlalchemy.exc import IntegrityError
import jwt
from flask import current_app as app


def getUser(auth):
    obj = jwt.decode(str(auth).split(" ")[1], app.config['SECRET_KEY'], algorithms=["HS256"])
    user_id = obj["user"]
    return user_id


class Users(Resource):
    method_decorators = {'post': [auth_req]}

    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str, help="Name of the user")
            parser.add_argument('email', type=str, help="Email of the user")
            parser.add_argument('password', type=str, help="Password of the user")
            parser.add_argument('role_id', type=int, help="Role of the user")
            args = parser.parse_args()
            user_id = getUser(request.authorization)
            user = db.one_or_404(
                db.select(User).filter_by(id=user_id),
                description="No user found"
            )
            if args['username'] is not None:
                user.username = args['username']
            if args['email'] is not None:
                user.email = args['email']
            if args['password'] is not None:
                user.password_hash = args['password']
            if args['role_id'] is not None:
                if user.role_id == 2:
                    user.role_id = args['role_id']
                else:
                    return make_response({"err": "You do not have permission to change role"})
            db.session.commit()
            return {"message": "User updated successfully"}, 200
        except IntegrityError as e:
            db.session.rollback()
            return make_response({"err": "Email Already Exists"})
        except Exception as e:
            db.session.rollback()
            print(e)
            return make_response({"err": "Something went wrong!!"})
        
    def delete(self):
        try:
            user_id = getUser(request.authorization)
            user = User.query.filter_by(id=user_id)
            if user is None:
                return make_response({"err": "User does not exist"})
            db.session.delete(user)
            db.session.commit()
            return {"message": "User deleted successfully"}, 200
        except Exception as e:
            print(e)
            return make_response({"err": "Something went wrong!!"})
