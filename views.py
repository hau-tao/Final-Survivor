from flask import Flask, render_template, redirect, flash, request
from survivor import app, db
from forms import ParticipantForm
from models import Participant

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
            title = 'Start Survivor')

@app.route('/participant', methods=['GET', 'POST'])
def participant():
    form = ParticipantForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            participant = Participant(
                    form.first_name.data,
                    form.last_name.data,
                    form.age.data,
                    form.major.data,
                    form.college_name.data,
                    form.academic_year.data
            )
            db.session.add(participant)
            db.session.commit()
            return redirect('/photo')
    return render_template('participant.html',
            title = 'Participant Registration',
            form  = form)

@app.route('/photo', methods=['GET', 'POST'])
def photo():
    return render_template('photo.html',
            title = 'Take Photo')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        rec = Photo(filename=filename, user=g.user.id)
        rec.store()
        flash("Photo submitted.")
        return redirect('/firstround')
    return render_template('/photo')

@app.route('/staging')
def staging():
    return render_template('staging.html', title = 'Preparing the Round...')

@app.route('/firstround', methods=['GET', 'POST'])
def firstround():
    return render_template('firstround/task.html',
            title = 'First Round')

@app.route('/secondround', methods=['GET', 'POST'])
def secondround():
    return render_template('secondround/task.html',
            title = 'Second Round')

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    return render_template('vote.html', title = 'Vote')

@app.route('/elimination', methods=['GET', 'POST'])
def elimination():
    return render_template('elimination.html',
            title = 'Elimination')

@app.route('/robots.txt')
@app.route('/favicon.ico')
def static_from_root():
    return app.send_static_file(request.path[1:])
