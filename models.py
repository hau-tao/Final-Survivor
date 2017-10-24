from app import db
from sqlalchemy import Column, Integer, Text, String, Boolean, \
DateTime

from datetime import datetime

class Participant(db.Model):
    """ Table name 'participant' is automatically set with Flask-SQLAlchemy """

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    age = db.Column(db.Integer)
    major = db.Column(db.String(120))
    college_name = db.Column(db.String(120))
    academic_year = db.Column(db.Integer)
    photo = db.Column(db.Text)
    score = db.Column(db.Integer)
    eliminated = db.Column(db.Boolean)

    def __init__(self, first_name, last_name, age, major, college_name,
        academic_year):

        self.first_name = first_name
        self.timestamp = datetime.utcnow()
        self.last_name = last_name
        self.age = age
        self.major = major
        self.college_name = college_name
        self.academic_year = academic_year

class Player():
    def __init__(self, name, photo_url, rank, score, status):
        self.name = name
        self.photo_url = photo_url
        self.rank = rank
        self.score = score
        self.status = status
