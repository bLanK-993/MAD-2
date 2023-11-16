from flask import request, make_response
from flask_restful import Resource
from models import db, Ticket, Show, User
from flask_restful import reqparse
from auth import auth_req
import jwt
from flask import current_app as app
def getUser(auth):
    obj = jwt.decode(str(auth).split(" ")[1], app.config['SECRET_KEY'], algorithms=["HS256"])
    user_id = obj["user"]
    return user_id

class Tickets(Resource):
    method_decorators = {'get': [auth_req], 'post': [auth_req]}

    def get(self):
        user_id = getUser(request.authorization)
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            return make_response({"err": "User does not exist"}, 404)
        tickets = Ticket.query.filter_by(user_id=user_id).all()
        return [ticket.serialize() for ticket in tickets]
    
    def post(self):
        try:
            user_id = getUser(request.authorization)
            parser = reqparse.RequestParser()
            parser.add_argument('show_id', type=int, help="ID of the show")
            parser.add_argument('theater_id', type=int, help="ID of the theater")
            parser.add_argument('event_id', type=int, help="ID of the event")
            parser.add_argument('seats', type=int, help="Number of seats")
            args = parser.parse_args()
            show = Show.query.filter_by(id=args['show_id']).first()
            if show is None:
                return make_response({"err": "Show does not exist"}, 404)
            
            new_ticket = Ticket(show_id=args['show_id'], user_id=user_id, theater= args['theater_id'], event_id=args['event_id'], seats=args['seats'] )
            db.session.add(new_ticket)
            db.session.commit()
            return {'message': 'Ticket created'}, 200
        except Exception as e:
            print(e)
            return {'err': 'Ticket creation failed'}, 400