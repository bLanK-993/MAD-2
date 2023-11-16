from flask import request, jsonify, make_response
from flask import current_app as app
from functools import wraps
from models import User
import json
import jwt

def auth_req(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            auth = str(request.authorization)
            if auth == "None":
                return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
            else:
                auth = auth.split(" ")[1]
            obj = jwt.decode(auth, app.config['SECRET_KEY'], algorithms=["HS256"])
            user = User.query.filter_by(id=obj["user"]).first()
            if user is None:
                return make_response('User does not exist!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
            return func(*args, **kwargs)
        except Exception as e :
            print(e)
            return make_response({'err':'Something Went Wrong'}, 500)
    return decorated

