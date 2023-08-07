import os

from blueprints.account.views import ChangeTodayView
from flask import Blueprint

template_folder = os.path.join(os.getcwd(), 'app', 'templates', 'account')

account_blueprint = Blueprint('account', __name__, template_folder=template_folder)

account_blueprint.add_url_rule("/change_today", view_func=ChangeTodayView.as_view("change_today"))
