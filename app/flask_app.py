import os

from extensions import executor, manager
from flask import Flask
from models import Website, db
from settings import BASEDIR, TODAY_DATE
from views import IndexView

from blueprints.account import init_app as account_init
from blueprints.database import init_app as database_init
from blueprints.sender import init_app as sender_init


def add_rules(app: Flask):
    app.add_url_rule("/", view_func=IndexView.as_view("index"))


def initialise_extensions(app: Flask):

    db.init_app(app)
    executor.init_app(app)

    manager.set_up_today(TODAY_DATE)


def initialise_blueprints(app: Flask):
    blueprints_inits = [
        account_init,
        database_init,
        sender_init,
    ]

    [init_function(app) for init_function in blueprints_inits]


def create_app():

    app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'app', 'templates'))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASEDIR, 'websites.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.secret_key = 'secretKey'

    app.config['EXECUTOR_PROPAGATE_EXCEPTIONS'] = True

    @app.context_processor
    def set_global_html_variable_values():
        websites_for_today = Website.websites_by_isActive_nextEmailDate(db.session, int(False), manager.today).count()
        template_config = {'today': manager.today,
                           'websites_for_today': websites_for_today}

        return template_config

    add_rules(app)
    initialise_extensions(app)
    initialise_blueprints(app)

    return app
