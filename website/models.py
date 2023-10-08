from . import db #import database
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime
import pytz

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000)) #this is a note user can input
    date = db.Column(db.DateTime(timezone=True), default=datetime.now(pytz.timezone('US/Pacific')))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #assign the note to correct user_id

    def formatted_date(self):
        pacific_timezone = pytz.timezone('US/Pacific')
        pacific_time = self.date.astimezone(pacific_timezone)

        return pacific_time.strftime('%Y-%m-%d | %I:%M %p')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) #db.Integer is difined id is an integer
    email = db.Column(db.String(150), unique=True) #db.String(150) is a length of string
    password = db.Column(db.String(150))  
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note') #this is a list will store the note of the user
    