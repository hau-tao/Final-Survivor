from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from config import config
from results import task_results


bootstrap = Bootstrap()
db = SQLAlchemy()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)

    from main import main as main_blueprint

    @main_blueprint.app_template_filter('participant')
    def participant(s):
        from .models import Participant
        s = Participant.query.filter_by(id=int(s)).first()
        if s:
            return s
        else:
            return None

    app.register_blueprint(main_blueprint)

    @app.context_processor
    def inject_players():
        from .models import Player
        players = Player.query.order_by(Player.name.desc()).all()
        return dict(players=players)

    @app.context_processor
    def inject_results():
        return dict(task_results=task_results)


    return app
