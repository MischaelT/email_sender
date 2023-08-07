import os

from blueprints.sender.views import RunSendingView, SendingView
from flask import Blueprint

template_folder = os.path.join(os.getcwd(), 'app', 'templates', 'sender')

sender_blueprint = Blueprint('sender', __name__, template_folder=template_folder)

sender_blueprint.add_url_rule("/run", view_func=RunSendingView.as_view("run_sending"))
sender_blueprint.add_url_rule("/run/sending", view_func=SendingView.as_view("sending"))
