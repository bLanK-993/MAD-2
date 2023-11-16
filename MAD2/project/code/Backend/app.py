from flask import Flask
from models import db, User, Theater, Role
from config import DevelopmentConfig
from flask_cors import CORS
from flask_mail import Mail, Message
from flask_restful import Api
from celery.utils.log import get_task_logger
from celery import Celery
from flask_restful import Api
from apis.events import Events, EventRatings
from apis.labels import Labels,EventsLabels
from apis.theater import Theaters, LocationTheater, TheaterEvents, Cities, AdminTheater
from apis.others import Login, Signup, Roles, AdminLogin
from apis.user import Users
from apis.shows import Shows
from apis.tickets import Tickets
from celery.schedules import crontab, timedelta
from datetime import datetime
from jinja2 import Environment, BaseLoader
from werkzeug.security import generate_password_hash
from flask_caching import Cache
import pandas as pd
import os
basedir = os.path.abspath(os.path.dirname(__file__))
# from apis.mail import Mailer
logger = get_task_logger(__name__)
app = None
api = Api()
mail = Mail()
celery = None
celery = Celery(
    __name__,
    backend='redis://localhost:6379/0',
    broker='redis://localhost:6379/0',
    
)

cache = Cache(config={
    'CACHE_TYPE': 'RedisCache',
    'CACHE_REDIS_HOST': 'localhost',
    'CACHE_REDIS_PORT': 6379,
    'CACHE_REDIS_URL':'redis://localhost:6379/0',
    'CACHE_KEY_PREFIX': 'ticket'
    })
basedir = os.path.abspath(os.path.dirname(__file__))
def create_db(app):
    if not os.path.exists(os.path.join(basedir, 'instance/database.sqlite3')):
        print("creating")
        with app.app_context():
            db.create_all()
            user_role = Role(name="user")
            admin_role = Role(name="admin")
            db.session.add(user_role)
            db.session.add(admin_role)
            db.session.commit()
            user = User(username="Admin", email="admin@gmail.com", password_hash=generate_password_hash("Admin@123"), role_id=2)
            db.session.add(user)
            db.session.commit()


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    mail.init_app(app)
    CORS(app)
    cache.init_app(app)
    celery.conf.update(app.config)
    api.add_resource(Login, '/login')
    api.add_resource(Signup, '/signup')
    api.add_resource(Users, '/update')
    api.add_resource(Roles, '/role')
    api.add_resource(Events, '/event')
    api.add_resource(Labels, '/label')
    api.add_resource(Theaters, '/theater')
    api.add_resource(Shows, '/show')
    api.add_resource(Tickets, '/ticket')
    api.add_resource(EventsLabels, '/event/labels')
    api.add_resource(LocationTheater, '/theater/location')
    api.add_resource(TheaterEvents, '/theater/events')
    api.add_resource(AdminLogin, '/admin/login')
    api.add_resource(Cities, '/city')
    api.add_resource(AdminTheater, '/admin/theater')
    api.add_resource(EventRatings, '/event/ratings')
    api.init_app(app)
    create_db(app)
    app.config["CELERY_TIMEZONE"] = "UTC"
    app.app_context().push()
    return app,api

app,api= create_app()

@app.route("/get/theater")
@cache.cached(timeout=50)
def getTheater():
    theaters = Theater.query.all()
    return [theater.serialize() for theater in theaters]




@celery.task(name='send_mail')
def send_mail():
    with app.app_context():
        users = User.query.all()
        with mail.connect() as conn:
            for user in users:
                # if len(user.tickets) < 2:
                #     print("Sending mail")
                #     msg = Message("Hello", recipients=[user.email], body="Hello "+user.username+" This is a test mail")
                #     conn.send(msg)
                for ticket in user.tickets:
                    if ticket.created_at < datetime.now() - timedelta(days=1):
                        print("Sending mail")
                        msg = Message("Hello", recipients=[user.email], body="Hello "+user.username+" We miss you :( Come back to our website to book movies and haffun with your life")
                        conn.send(msg)
template = """
            <div style="text-align: left;display:flex; flex-direction:column; justify-content:center; align-items:center">
                    <h1>Monthly Report</h1>
                    <p>Hello user, this your monthly report from the ticket booking app. </p>
                    <h3>Number of tickets booked : {{ticketnumber}}</h3>
                    {% if movie_len > 0 %}
                        <div style="display: flex;">
                            <h3>List of movies:</h3>
                            <ul style="list-style: disc;width:max-content;text-align:left">
                                {% for movie in movies %}
                                <li>{{movie["name"]}} - {{movie["ratings"]}} </li>
                                {% endfor %}
                            </ul>
                        </div>
                    {% endif %}
                    {% if theater_len > 0 %}
                    <div style="display: flex;">
                        <h3>List of theatres:</h3>
                        <ul style="list-style: disc;width:max-content;text-align:left">
                            {% for theater in theaters %}
                            <li>{{theater}}</li>
                            {% endfor %}
                        </ul>
                    </div>
                    {% endif %}
                </div>"""
@celery.task(name='send_monthly_mail')
def send_monthly_mail():
    with app.app_context():
        users = User.query.all()
        with mail.connect() as conn:
            for user in users:
                # if len(user.tickets) < 2:
                #     print("Sending mail")
                #     msg = Message("Hello", recipients=[user.email], body="Hello "+user.username+" This is a test mail")
                #     conn.send(msg)
                print("Sending mail")
                ticketnumber = len(user.tickets)
                theaters = [ticket.serialize()["theater"]["name"] for ticket in user.tickets]
                movies = [ticket.serialize()["event"] for ticket in user.tickets]
                movie_len = len(movies)
                theater_len = len(theaters)
                print(theaters)
                msg = Message("Hello", 
                              recipients=[user.email], 
                              body="Hello "+user.username+" This is your monthly report", 
                              html=Environment(loader=BaseLoader).from_string(template).render(ticketnumber=ticketnumber, movies=movies, theaters=theaters, movie_len= movie_len, theater_len=theater_len))
                conn.send(msg)

@celery.task(name='export')
def exportCSV(id):
    with app.app_context():
        theater = Theater.query.filter_by(id=id).first()
        user = User.query.filter_by(id=theater.user_id).first()
        event_list = []
        for event in theater.events:
            event_dict = {}
            event_dict["id"] =  event.id
            event_dict["name"] = event.name
            event_dict["ratings"] = event.ratings
            event_dict["price"] = event.price
            event_dict["shows"] = len(event.shows)
            event_list.append(event_dict)
        df = pd.DataFrame(event_list)
        df.to_csv(os.path.join(basedir, f'{theater.name}.csv'), index=False)
        msg = Message(recipients=[user.email], body="Hello "+user.username+", This is your exported CSV")
        msg.attach(filename=f'{theater.name}.csv', content_type='text/csv', data=open(os.path.join(basedir, f'{theater.name}.csv'), 'rb').read())
        mail.send(msg)

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(crontab(minute="*", hour="*"), send_mail, name='add every 1min')
    sender.add_periodic_task(crontab(day_of_month=1, month_of_year="*"), send_monthly_mail, name='add montlhy mail every 1min')

@app.route("/export/<int:id>")
def export(id):
    try:
        exportCSV.delay(id)
        return {"mesage":"Exported CSV"}, 200
    except:
        return {"message":"Error"}, 500





if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
