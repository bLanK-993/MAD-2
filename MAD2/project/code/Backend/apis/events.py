from flask_restful import Resource, reqparse
from flask import make_response, request
from models import db, Event, User, Theater, Label
from auth import auth_req
import jwt
from flask import current_app as app


def getUser(auth):
    obj = jwt.decode(str(auth).split(" ")[1], app.config['SECRET_KEY'], algorithms=["HS256"])
    user_id = obj["user"]
    return user_id

class Events(Resource):
    method_decorators = {'get': [auth_req], 'post': [auth_req], 'put': [auth_req], 'delete': [auth_req]}

    def get(self):
        events = Event.query.all()
        return [event.serialize() for event in events]
    
    def post(self):
        try:
            auth = request.authorization
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, help="Name of the event")
            parser.add_argument('ratings', type=float, help="Ratings of the show" )
            parser.add_argument('theater_id', type=int, help="ID of the theater")
            parser.add_argument('price', type=int, help="Price of the event")
            parser.add_argument('labels', type=str, help="Labels of the event")
            args = parser.parse_args()
            user = User.query.filter_by(id=getUser(auth)).first()
            theater = Theater.query.filter_by(id=args['theater_id']).first()
            if user is None:
                return make_response({"err": "User does not exist"}, 404)
            if theater is None:
                return make_response({"err": "Theater does not exist"}, 404)
            if user.id != theater.user_id:
                return make_response({"err": "You do not have permission to create event in this theater"}, 401)
            if user.role_id != 2:
                return make_response({"err": "You do not have permission to create event"}, 401)
            if args['labels'] is not None:
                labels = str(args['labels']).split(",")
                new_labels = []
                for label in labels:
                    current_label = Label.query.filter_by(name=label.lower()).first()
                    if current_label is None:
                        current_label = Label(name=label)
                        db.session.add(current_label)
                        db.session.commit()
                        new_labels.append(current_label)
                    else:
                        new_labels.append(current_label)
            new_event = Event(name=args['name'], price=args['price'], ratings=args['ratings'], theater_id=args['theater_id'], user_id=getUser(auth), labels=new_labels)
            db.session.add(new_event)
            db.session.commit()
            return {'message': 'Event created'}, 200
            
        except Exception as e:
            db.session.rollback()
            print(e)
            return make_response({"err": "Something went wrong!!"}, 500)

    def put(self):
        try:
            auth = request.authorization
            parser = reqparse.RequestParser()
            parser.add_argument('event_id', type=str, help="ID of the event")
            parser.add_argument('name', type=str, help="Name of the event")
            parser.add_argument('labels', type=str, help="Labels of the event")
            args = parser.parse_args()
            print(getUser(auth))
            event = Event.query.filter_by(id=args['event_id']).first()
            user  = User.query.filter_by(id=getUser(auth)).first()
            if user is None:
                return make_response({"err": "User does not exist"}, 404)
            if user.role_id != 2:
                return make_response({"err": "You do not have permission to update event"}, 401)
            if event.user_id == user.id:
                if args['name'] is not None:
                    event.name = args['name']
                if args['labels'] is not None:
                    labels = args['labels']
                    for label in labels:
                        current_label = Label.query.filter_by(name=label).first()
                        if current_label is None:
                            current_label = Label(name=label)
                            db.session.add(current_label)
                            db.session.commit()
                        event.labels.append(current_label)
                db.session.commit()
                return {'message': 'Event updated'}, 200
            else:
                return make_response({"err": "You do not have permission to update this event"}, 401)
        except Exception as e:
            db.session.rollback()
            print(e)
            return make_response({"err": "Something went wrong!!"}, 500)

    def delete(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('event_id', type=str, help="ID of the event")
            args = parser.parse_args()
            event = Event.query.filter_by(id=args['event_id']).first()
            if event is None:
                return make_response({"err": "Event does not exist"}, 404)
            user  = User.query.filter_by(id=getUser(request.authorization)).first()
            if user is None:
                return make_response({"err": "User does not exist"}, 404)
            if user.role_id != 2:
                return make_response({"err": "You do not have permission to delete event"}, 401)
            db.session.delete(event)
            db.session.commit()
            return {'message': 'Event deleted'}, 200
        except Exception as e:
            db.session.rollback()
            print(e)
            return make_response({"err": "Something went wrong!!"})
        


class EventRatings(Resource):
    method_decorators = {'put': [auth_req]}

    def put(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('event_id', type=str, help="ID of the event")
            parser.add_argument('ratings', type=float, help="Ratings of the show" )
            args = parser.parse_args()
            event = Event.query.filter_by(id=args['event_id']).first()
            if event is None:
                return make_response({"err": "Event does not exist"}, 404)
            event.ratings = ((event.ratings*event.rating_count) + args['ratings']) / (event.rating_count + 1)
            event.rating_count += 1
            db.session.commit()
            return {'message': 'Ratings updated'}, 200
        except Exception as e:
            db.session.rollback()
            print(e)
            return make_response({"err": "Something went wrong!!"}, 500)