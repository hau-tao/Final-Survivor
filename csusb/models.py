from flask import current_app
from csusb import db
from sqlalchemy import Column, Integer, Text, String, Boolean, \
DateTime

from datetime import datetime

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    fairness = db.Column(db.String(120))
    relevance = db.Column(db.String(120))
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    age = db.Column(db.Integer)
    major = db.Column(db.String(120))
    college_name = db.Column(db.String(120))
    academic_year = db.Column(db.Integer)
    photo = db.Column(db.Text)
    score = db.Column(db.Integer)
    eliminated = db.Column(db.Boolean)
    first_round_answers = db.Column(db.Text)
    first_elimination_vote = db.Column(db.Text)
    second_round_answers = db.Column(db.Text)
    second_elimination_vote = db.Column(db.Text)

    def __init__(self, timestamp, fairness, relevance, first_name, last_name, age, major, college_name,
        academic_year, photo="", score=0, eliminated=False):

        self.timestamp = timestamp
        self.fairness = fairness
        self.relevance = relevance
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.major = major
        self.college_name = college_name
        self.academic_year = academic_year
        self.photo = photo
        self.score = score
        self.eliminated = eliminated

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    photo_url = db.Column(db.String(120))
    rank = db.Column(db.Integer)
    score = db.Column(db.Integer)
    eliminated = db.Column(db.Boolean)

    def __init__(self, name, photo_url, rank=0, score=0, eliminated=False):
        self.name = name
        self.photo_url = photo_url
        self.rank = rank
        self.score = score
        self.eliminated = eliminated


class Version(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    type = db.Column(db.Text)
    rank = db.Column(db.Text)
    round = db.Column(db.Integer)
    eliminated_player = db.Column(db.Text)
    player_comments = db.Column(db.Text)

    def __init__(self, number, type, rank, round, eliminated_player, player_comments):
        self.number = number
        self.type = type
        self.rank = rank
        self.round = round
        self.eliminated_player = eliminated_player
        self.player_comments = player_comments
