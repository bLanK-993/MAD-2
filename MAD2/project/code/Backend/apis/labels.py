from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from models import db, Label, event_label
from auth import auth_req
from sqlalchemy.exc import IntegrityError

class Labels(Resource):

    def get(self):
        labels = Label.query.all()
        return {"message":[label.serialize() for label in labels]}
    
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, help="New unique label name")
            args = parser.parse_args()
            new_label = Label(name=args['name'])
            db.session.add(new_label)
            db.session.commit()
            return make_response({"message":"New Label {} has been created".format(args['name'])}, 200)
        except IntegrityError as e:
            db.session.rollback()
            return make_response({"err": "Label Already Exists"})
        except Exception as e:
            db.session.rollback()
            return make_response({"err": str(e)})
        

class EventsLabels(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('label_id', type=str, help="Label Id")
        args = parser.parse_args()
        labels = str(args['label_id']).split(",")
        events = []
        for label_id in labels:
            label = Label.query.filter_by(id=label_id).first()
            if label is None:
                return make_response({"err": "Label does not exist"}, 404)
            events.extend([event.serialize() for event in label.events])
        return {"message": events}