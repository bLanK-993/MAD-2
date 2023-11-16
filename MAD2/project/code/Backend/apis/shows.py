from flask_restful import Resource, reqparse
from flask import make_response, request
from models import db, Show, User
from auth import auth_req
import jwt
from flask import current_app as app
from datetime import datetime
from models import TimeException

def getUser(auth):
    obj = jwt.decode(str(auth).split(" ")[1], app.config['SECRET_KEY'], algorithms=["HS256"])
    user_id = obj["user"]
    return user_id



class Shows(Resource):
    method_decorators = {'get': [auth_req], 'post': [auth_req]}
    def get(self):
        user_id = getUser(request.authorization)
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            return make_response({"err": "User does not exist"}, 404)
        shows = Show.query.filter_by(user_id=user_id).all()
        return [show.serialize() for show in shows]
    
    def post(self):
        try:
            user_id = getUser(request.authorization)
            parser = reqparse.RequestParser()
            parser.add_argument('event_id', type=int, help="ID of the event")
            parser.add_argument('theater_id', type=int, help="ID of the theater")
            parser.add_argument('date', type=int, help="Date of the show")
            parser.add_argument('start_time', type=int, help="Start time of the show")
            parser.add_argument('end_time', type=int, help="End time of the show")
            parser.add_argument('available_seats', type=int, help="Available seats of the show")
            args = parser.parse_args()
            date = datetime.fromtimestamp(args['date']/1000)
            start_time = datetime.fromtimestamp(args['start_time']/1000)
            end_time = datetime.fromtimestamp(args['end_time']/1000)

            new_show = Show(event_id=args['event_id'], theater_id=args['theater_id'], date=date, start_time=start_time, end_time=end_time, available_seats=args['available_seats'], user_id=user_id)
            
            db.session.add(new_show)
            db.session.commit()
            return {'message': 'Show created'}, 200
        except TimeException as e:
            print(e)
            return {'err': 'Time Conflict'}, 400
        except Exception as e:
            print(e)
            return {'err': 'Show creation failed'}, 400

    
        

