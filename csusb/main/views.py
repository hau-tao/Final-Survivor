from flask import render_template, request, redirect, url_for, \
        session, current_app, flash, jsonify, send_file, make_response
from . import main
from .. import db
from ..results import task_results
from .forms import ParticipantForm, SecondRoundForm, EliminationForm, ResearcherInfoForm
from ..models import Participant, Player
from werkzeug.utils import secure_filename
from config import config
import os
import random
from itertools import groupby
import csv
import StringIO
from base64 import decodestring

from datetime import datetime


@main.route('/', methods=['GET', 'POST'])
def index():
    session.pop('university', None)
    session.pop('researchers_first_name', None)
    session.pop('order', None)
    session.pop('participant_id', None)
    form = ResearcherInfoForm()
    if form.validate_on_submit():
        session['university'] = form.university.data
        session['researchers_first_name'] = form.researchers_first_name.data
        return redirect(url_for('main.setup'))
    return render_template('index.html', form=form)


@main.route('/setup')
def setup():
    return render_template('setup.html')


@main.route('/api/first_round_task/<order>', methods=['GET', 'POST'])
def api_first_round_task(order=None):
    session['order'] = {}
    for index, item in enumerate(order.split(",")):
        session['order'][item] = index + 1

    print session['order']
    return jsonify({'order': order})


@main.route('/participant', methods=['GET', 'POST'])
def participant():
    form = ParticipantForm()
    """Get a randomly selected type. And setup new test."""
    fairness_options = ['fair', 'unfair']
    relevance_options = ['relevant', 'irrelevant']
    if session.get('override_fairness', None):
        fairness = session['override_fairness']
    else:
        fairness = random.choice(fairness_options)
    if session.get('override_relevance', None):
        relevance = session['override_relevance']
    else:
        relevance = random.choice(relevance_options)

    #Reset session to remove the previous participant

    players = Player.query.order_by(Player.name.desc()).all()

    #Reset scores, rank, and elimination status
    for player in players:
        player.rank = None
        player.score = 0
        player.eliminated = False
        db.session.commit()

    if request.method == 'POST':
        if form.validate_on_submit():
            participant = Participant(
                    timestamp=datetime.now(),
                    fairness=fairness,
                    relevance=relevance,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    age=form.age.data,
                    major=form.major.data,
                    college_name=form.college_name.data,
                    academic_year=form.academic_year.data
            )

            db.session.add(participant)
            db.session.commit()

            session['participant_id'] = participant.id

            return redirect('/photo')
    return render_template('participant.html',
            title='Participant Registration',
            form=form)

@main.route('/photo', methods=['GET', 'POST'])
def photo():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'imgBase64' not in request.form:
            flash('No file part')
            return redirect(request.url)
        data_uri = request.form['imgBase64']
        data = decodestring(data_uri.split(',', 1)[-1])
        participant = Participant.query.filter_by(id=session['participant_id']).first()
        filename = participant.first_name + '_' + participant.last_name + '.jpg'
        path_to_photo = os.path.join(config['default'].UPLOAD_FOLDER, filename)
        with open(path_to_photo, 'wb') as f:
            f.write(data)
        participant.photo = filename
        db.session.commit()
        return redirect('/staging')
    return render_template('photo.html')

@main.route('/staging')
def staging():
    return render_template('staging.html')

@main.route('/firstround')
def first_round():
    return render_template('firstround/task.html')

@main.route('/firstround/reminder')
def first_round_reminder():
    return render_template('firstround/reminder.html')

@main.route('/firstround/scores')
def first_round_scores():

    rankings = []
    participant = Participant.query.filter_by(id=session['participant_id']).first()
    participant.score = task_results[participant.relevance][participant.fairness]['r1']['rankings']['Participant']
    db.session.commit()

    rankings.append([participant.first_name, participant.score])

    players = Player.query.order_by(Player.name.desc()).all()
    for player in players:
        player.score = task_results[participant.relevance][participant.fairness]['r1']['rankings'].get(player.name, 0)
        rankings.append([player.name, player.score])
        db.session.commit()

    rankings = sorted(rankings, key=lambda x: x[1], reverse=True)
    for rank, (_, grp) in enumerate(groupby(rankings, key=lambda xs: xs[1]), 1):
        for x in grp:
            x.append(rank)


    return render_template('firstround/scores.html', rankings=rankings)

@main.route('/secondround')
def second_round():
    form = SecondRoundForm()
    participant = Participant.query.filter_by(id=session['participant_id']).first()
    participant.score = 0
    db.session.commit()
    players = Player.query.order_by(Player.name.desc()).all()
    for player in players:
        player.score = 0
        db.session.commit()
    return render_template('secondround/task.html', form=form)

@main.route('/secondround/reminder')
def second_round_reminder():
    return render_template('secondround/reminder.html')

@main.route('/secondround/scores')
def second_round_scores():
    rankings = []
    participant = Participant.query.filter_by(id=session['participant_id']).first()
    participant.score = task_results[participant.relevance][participant.fairness]['r2']['rankings']['Participant']
    db.session.commit()
    rankings.append([participant.first_name, participant.score])

    players = Player.query.order_by(Player.name.desc()).all()
    for player in players:
        player.score = task_results[participant.relevance][participant.fairness]['r2']['rankings'].get(player.name, 0)
        if player.eliminated:
            pass
        else:
            rankings.append([player.name, player.score])
        db.session.commit()

    rankings = sorted(rankings, key=lambda x: x[1], reverse=True)
    for rank, (_, grp) in enumerate(groupby(rankings, key=lambda xs: xs[1]), 1):
        for x in grp:
            x.append(rank)

    return render_template('secondround/scores.html', rankings=rankings)

@main.route('/firstround/elimination', methods=['GET', 'POST'])
@main.route('/firstround/elimination/<modify>', methods=['GET', 'POST'])
def first_elimination(modify=None):
    participant = Participant.query.filter_by(id=session['participant_id']).first()
    form = EliminationForm()
    choices = task_results[participant.relevance][participant.fairness]['r1']['rankings']
    form.player.choices = [(key, key) for key, value in choices.items() if key != 'Participant']
    form.player.choices.insert(0, ('', ''))

    if form.validate_on_submit():
        participant = Participant.query.filter_by(id=session['participant_id']).first()
        participant.first_elimination_vote = form.player.data
        participant.first_round_answers = form.reason.data
        db.session.commit()

        eliminated_player = Player.query.filter_by(name=task_results[participant.relevance][participant.fairness]['r1']['player_voted_off']).first()
        eliminated_player.eliminated = True
        db.session.commit()

        return redirect(url_for('main.first_elimination', modify='results'))
    return render_template('elimination.html', form=form, modify=modify)

@main.route('/secondround/elimination', methods=['GET', 'POST'])
@main.route('/secondround/elimination/<modify>', methods=['GET', 'POST'])
def second_elimination(modify=None):
    participant = Participant.query.filter_by(id=session['participant_id']).first()
    form = EliminationForm()
    choices = task_results[participant.relevance][participant.fairness]['r2']['rankings']
    eliminated_player = task_results[participant.relevance][participant.fairness]['r2']['player_voted_off']

    form.player.choices = [(key, key) for key, value in choices.items() if key != 'Participant']
    form.player.choices.insert(0, ('', ''))
    if form.validate_on_submit():
        participant = Participant.query.filter_by(id=session['participant_id']).first()
        participant.second_elimination_vote = form.player.data
        participant.second_round_answers = form.reason.data
        if eliminated_player == 'Participant':
            participant.eliminated = True
        db.session.commit()
        return redirect(url_for('main.second_elimination', modify='second_results'))
    return render_template('elimination.html', form=form, modify=modify)


@main.route('/final-step', methods=['GET', 'POST'])
def final_step():
    return render_template('final_step.html')


@main.route('/change-fairness/<modify>', methods=['GET', 'POST'])
def change_fairness(modify=None):
    if modify == '001':
        session['override_fairness'] = 'unfair'
        session['override_relevance'] = 'relevant'
    elif modify == '002':
        session['override_fairness'] = 'fair'
        session['override_relevance'] = 'relevant'
    elif modify == '003':
        session['override_fairness'] = 'unfair'
        session['override_relevance'] = 'irrelevant'
    elif modify == '004':
        session['override_fairness'] = 'fair'
        session['override_relevance'] = 'irrelevant'
    elif modify == 'clear':
        session.pop('override_fairness', None)
        session.pop('override_relevance', None)
    return redirect(url_for('main.admin'))


@main.route('/admin/delete_all', methods=['GET', 'POST'])
@main.route('/admin/delete_one/<int:id>', methods=['GET', 'POST'])
def delete_all(id=None):
    if id:
        participant = Participant.query.filter_by(id=id).delete()
        db.session.commit()
        return redirect(url_for('main.admin'))
    Participant.query.delete()
    db.session.commit()
    return redirect(url_for('main.admin'))


@main.route('/admin/csv', methods=['GET', 'POST'])
def to_csv():
    participants = Participant.query.order_by(Participant.timestamp.desc()).all()

    si = StringIO.StringIO()
    cw = csv.writer(si)
    cw.writerow(('id',
                 'timestamp',
                 'fairness',
                 'relevance',
                 'first name',
                 'last name',
                 'age',
                 'major',
                 'college',
                 'academic year',
                 'eliminated',
                 'first round answers',
                 'second round answers',
                 'first round vote',
                 'second round vote'))
    for p in participants:
        cw.writerow((p.id,
                     p.timestamp,
                     p.fairness,
                     p.relevance,
                     p.first_name,
                     p.last_name,
                     p.age,
                     p.major,
                     p.college_name,
                     p.academic_year,
                     p.eliminated,
                     p.first_round_answers,
                     p.second_round_answers,
                     p.first_elimination_vote,
                     p.second_elimination_vote))

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output


@main.route('/admin', methods=['GET', 'POST'])
def admin():
    participants = Participant.query.order_by(Participant.timestamp.desc()).all()
    return render_template('admin.html', participants=participants)
