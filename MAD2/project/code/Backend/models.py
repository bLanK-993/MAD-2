from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from datetime import datetime
import pytz

utc=pytz.UTC
db = SQLAlchemy()

event_label = db.Table('event_label',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key = True),
    db.Column('label_id', db.Integer, db.ForeignKey('label.id'), primary_key = True)
)

class TimeException(Exception):
    pass



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    username = db.Column(db.String(80), unique=False)
    password_hash = db.Column(db.String(120))
    tickets = db.relationship('Ticket', backref='user_tickets', lazy=True)
    events = db.relationship('Event', backref='user_events', lazy=True)
    theaters = db.relationship('Theater', backref='user_theaters', lazy=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), unique=False, nullable=False)
    def __repr__(self):
        return '<User %r>' % self.username
    
    def serialize(self):
        return {
            'id': self.id, 
            'username': self.username
        }


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    users = db.relationship('User', backref='user_role', lazy=True)
    def __repr__(self):
        return '<Role %r>' % self.name

    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name
        }

class Theater(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    place = db.Column(db.String, unique=False, nullable=False)
    city = db.Column(db.String, db.ForeignKey('city.name'), unique=False, nullable=False)
    capacity = db.Column(db.Integer, unique=False, nullable=False)
    shows = db.relationship('Show', backref='show_theater', lazy="dynamic", cascade="all, delete-orphan")
    events = db.relationship('Event', backref='event_theater', lazy=True, cascade="all, delete-orphan")
    tickets = db.relationship('Ticket', backref='ticket_theater', lazy=True, cascade="all, delete-orphan")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=False, nullable=False)
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'place': self.place,
            'city': self.city,
            'capacity': self.capacity,
            'events': [event.serialize() for event in self.events]
        }
    
    def exportCSV(self):
        return {
            'id': self.id,
            'name': self.name,
            'place': self.place,
            'city': self.city,
            'capacity': self.capacity,
            'events': [event.serialize()["name"] for event in self.events]
        }

    def ticketDeets(self):
        return {
            'name': self.name,
            'place': self.place,
            'city': self.city,
        }


class Label(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    events = db.relationship('Event', secondary=event_label, back_populates="labels")
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name
        }
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    ratings = db.Column(db.Integer, unique=False, nullable=False)
    rating_count = db.Column(db.Integer, unique=False, default=1)
    price = db.Column(db.Integer, unique=False, nullable=False)
    shows = db.relationship('Show', backref='show_event', lazy=True, cascade="all, delete-orphan")
    labels = db.relationship('Label', secondary=event_label, back_populates="events")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=False, nullable=False)
    theater_id = db.Column(db.Integer, db.ForeignKey('theater.id', ondelete="CASCADE"), unique=False, nullable=False)
    tickets = db.relationship('Ticket', backref='ticket_event', lazy=True, cascade="all, delete-orphan")
    
    def __init__(self, **kwargs):
        super(Event, self).__init__(**kwargs)
        if self.ratings < 0 or self.ratings > 5:
            raise Exception("Ratings should be between 0 and 5")
        if self.price < 0:
            raise Exception("Price cannot be negative")
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'ratings': self.ratings,
            'price': self.price,
            'labels': [label.serialize() for label in self.labels],
            'shows': [show.serialize() for show in self.shows]
        }
    def ticketDeets(self):
        return {
            'id': self.id,
            'name': self.name,
            'ratings': self.ratings,
            'price': self.price,
            'labels': [label.serialize() for label in self.labels],
        }

class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.ForeignKey('event.id', ondelete="CASCADE"), unique=False, nullable=False)
    theater_id = db.Column(db.ForeignKey('theater.id', ondelete="CASCADE"), unique=False, nullable=False)
    start_time = db.Column(db.DateTime, unique=False, nullable=False)
    date = db.Column(db.DateTime, unique=False, nullable=False)
    end_time = db.Column(db.DateTime, unique=False, nullable=False)
    available_seats = db.Column(db.Integer, unique=False, nullable=False)
    tickets = db.relationship('Ticket', backref='show_ticket', lazy=True, cascade="all, delete-orphan")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=False, nullable=False)
    def __init__(self, **kwargs):
        super(Show, self).__init__(**kwargs)
        theater = Theater.query.filter_by(id = self.theater_id).first()
        today = datetime.now()
        if theater is None:
            raise Exception("Theater does not exist")
        if theater.capacity < self.available_seats:
            raise Exception("Available seats cannot be greater than capacity")
        if self.start_time < today:
            raise TimeException("Start time cannot be in the past")
        if self.end_time < self.start_time:
            raise TimeException("End time cannot be before start time")
        if self.date < today:
            raise TimeException("Date cannot be in the past")
        if self.date > self.start_time:
            raise TimeException("Date cannot be before start time")
        shows = [s for s in theater.shows if self.date.date() == s.date.date() and self.event_id == s.event_id]
        start = self.start_time
        end = self.end_time
        for show in shows:
            start_time = show.start_time.replace(tzinfo=utc)
            end_time = show.end_time.replace(tzinfo=utc)
            if start_time <= start <= end_time or start_time <= end <= end_time:
                raise TimeException("Time conflict")
    def serialize(self):
        return{
            'id': self.id,
            'event': self.event_id,
            'theater': self.theater_id,
            'start_time': str(self.start_time),
            'end_time': str(self.end_time),
            'date': str(self.date),
            'available_seats': self.available_seats,
            'tickets': [ticket.serialize() for ticket in self.tickets]

        }
    def ticketDeets(self):
        return{
            'start_time': str(self.start_time),
            'end_time': str(self.end_time)
        }


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    show_id = db.Column(db.Integer ,db.ForeignKey('show.id', ondelete="CASCADE"), nullable = False)
    user_id = db.Column(db.Integer ,db.ForeignKey('user.id'), nullable=False)
    theater = db.Column(db.Integer ,db.ForeignKey('theater.id', ondelete="CASCADE"), nullable=False)
    event_id = db.Column(db.Integer ,db.ForeignKey('event.id', ondelete="CASCADE"), nullable=False)
    seats = db.Column(db.Integer, unique=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    def __init__(self, **kwargs):
        super(Ticket, self).__init__(**kwargs)
        show = Show.query.filter_by(id = self.show_id).first()
        
        print(show)
        if show.available_seats == 0:
            raise Exception("No seats available")
        if show.available_seats < self.seats:
            raise Exception("Not enough seats available")
        show.available_seats -= self.seats
        today = datetime.now()
        if show.end_time < today:
            raise TimeException("The show is already running or has already run")
        
        db.session.commit()
    def serialize(self):
        theater = Theater.query.filter_by(id = self.theater).first()
        event = Event.query.filter_by(id = self.event_id).first()
        show = Show.query.filter_by(id = self.show_id).first()
        return{
            'id': self.id,
            'show': show.ticketDeets(),
            'user': self.user_id,
            'theater': theater.ticketDeets(),
            'event': event.ticketDeets(),
            'seats': self.seats
        }

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    theaters = db.relationship('Theater', backref='theater_city', lazy=True)
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name
        }