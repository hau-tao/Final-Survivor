from flask import Flask, render_template, redirect, url_for
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy

from forms import ParticipantForm, SecondRoundForm, EliminationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'be the love you want to find'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + '/tmp/survivor.db '
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

#postgres://ituakzqmjbmznp:eFvtMtJEl1UtfAq6p0gD-a4e5G@ec2-54-221-234-118.compute-1.amazonaws.com:5432/d6lbbjl7ggnlpr

manager = Manager(app)
bootstrap = Bootstrap(app)

db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/participant', methods=['GET', 'POST'])
def participant():
    form = ParticipantForm()
    if form.validate_on_submit():
        return redirect(url_for('photo'))
    return render_template('participant.html', form=form)

@app.route('/photo', methods=['GET', 'POST'])
def photo():
    return render_template('photo.html')

@app.route('/upload', methods=['POST'])
def upload():
    return '<h1>Uploading...</h1>'

@app.route('/staging')
def staging():
    return render_template('staging.html')

@app.route('/elimination')
def elimination():
    form = EliminationForm()
    return render_template('elimination.html', form=form)

@app.route('/firstround')
def first_round():
    return render_template('firstround/task.html')

@app.route('/firstround/scores')
def first_round_scores():
    return render_template('firstround/scores.html')

@app.route('/secondround')
def second_round():
    form = SecondRoundForm()
    return render_template('secondround/task.html', form=form)

@app.route('/secondround/scores')
def second_round_scores():
    return render_template('secondround/scores.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    manager.run()
