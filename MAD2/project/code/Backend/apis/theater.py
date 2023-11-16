from flask_restful import Resource, reqparse
from flask import jsonify, make_response, request
from models import db, User, Theater, City, Event, Show
from auth import auth_req
import jwt
from flask import current_app as app


def getUser(auth):
    obj = jwt.decode(str(auth).split(" ")[1], app.config['SECRET_KEY'], algorithms=["HS256"])
    user_id = obj["user"]
    return user_id

class Theaters(Resource):
    method_decorators = {'post': [auth_req], 'put': [auth_req], 'delete': [auth_req]}
    
    def post(self):
        try:
            auth = request.authorization
            user_id = getUser(auth)
            print(user_id)
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, help="Name of the theater")
            parser.add_argument('place', type=str, help="Place of the theater")
            parser.add_argument('city', type=str, help="City of the theater")
            parser.add_argument('capacity', type=int, help="Capacity of the theater")
            args = parser.parse_args()
            
            user = User.query.filter_by(id=user_id).first()
            if user is None:
                return make_response({"err": "User does not exist"})
            if user.role_id != 2:
                return make_response({"err": "You do not have permission to create theater"})
            if args['city'] is not None:
                city = City.query.filter_by(name=args['city']).first()
                if city is None:
                    city = City(name=args['city'])
                    db.session.add(city)
                    db.session.commit()
            new_theater = Theater(name=args['name'], place=args['place'], city=args['city'], capacity=args['capacity'], user_id=user_id)
            db.session.add(new_theater)
            db.session.commit()
            return {'message': 'Theater created'}, 200
                
            
        except Exception as e:
            db.session.rollback()
            print(e)
            return make_response({"err": "Something went wrong!!"})

    def put(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('theater_id', type=str, help="ID of the theater")
            parser.add_argument('name', type=str, help="Name of the theater")
            parser.add_argument('place', type=str, help="Place of the theater")
            parser.add_argument('city', type=str, help="City of the theater")
            parser.add_argument('capacity', type=int, help="Capacity of the theater")
            args = parser.parse_args()
            print(args)
            theater = db.first_or_404(Theater.query.filter_by(id=args['theater_id']))
            user  = db.first_or_404(User.query.filter_by(id=getUser(request.authorization)))
            if user is None:
                return make_response({"err": "User does not exist"}, 404)
            if theater.user_id == user.id:
                if args['name'] is not None:
                    theater.name = args['name']
                if args['place'] is not None:
                    theater.place = args['place']
                if args['city'] is not None:
                    theater.city = args['city']
                if args['capacity'] is not None:
                    theater.capacity = args['capacity']
                db.session.commit()
                return {'message': 'Theater updated'}, 200
            else:
                return make_response({"err": "You do not have permission to update this theater"}, 401)
        except Exception as e:
            db.session.rollback()
            print(e)
            return make_response({"err": "Something went wrong!!"}, 500)
        
    def delete(self):
        try:
            auth = request.authorization
            parser = reqparse.RequestParser()
            parser.add_argument('theater_id', type=str, help="ID of the theater")
            args = parser.parse_args()
            user = User.query.filter_by(id=getUser(auth)).first()
            theater = Theater.query.filter_by(id=args['theater_id']).first()
            if user is None:
                return make_response({"err": "User does not exist"}, 404)
            if theater is None:
                return make_response({"err": "Theater does not exist"}, 404)
            if user.role_id != 2:
                return make_response({"err": "You do not have permission to delete theater"}, 401)
            db.session.delete(theater)
            db.session.commit()
            return {'message': 'Theater deleted'}, 200
        except Exception as e:
            db.session.rollback()
            print(e)
            return make_response({"err": "Something went wrong!!"})


class AdminTheater(Resource):
    method_decorators = {'get': [auth_req]}

    def get(self):
        try:
            auth = request.authorization
            user = User.query.filter_by(id=getUser(auth)).first()
            theaters = Theater.query.filter_by(user_id = getUser(auth)).all()
            if user is None:
                return make_response({"err": "User does not exist"}, 404)
            if theaters is None:
                return make_response({"err": "No theaters created yet"}, 404)
            
            return [theater.serialize() for theater in theaters]
        except Exception as e:
            print(e)
            return make_response({"err": "Something went wrong!!"})

class Cities(Resource):
    def get(self):
        cities = City.query.all()
        return [city.serialize() for city in cities]

class LocationTheater(Resource):
    method_decorators = {'get': [auth_req]}

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('city', type=str, help="City of the theater")
        args = parser.parse_args()
        theaters = Theater.query.filter_by(city=args['city']).all()
        return [theater.serialize() for theater in theaters]
    
class TheaterEvents(Resource):

    method_decorators = {'get': [auth_req]}

    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('theater_id', type=str, help="ID of the theater")
            args = parser.parse_args()
            theater = Theater.query.filter_by(id=args['theater_id']).first()
            if theater is None:
                return make_response({"err": "Theater does not exist"}, 404)
            events = [event.serialize() for event in theater.events]
            return {"message": events}
        except Exception as e:
            print(e)
            return make_response({"err": "Something went wrong!!"})