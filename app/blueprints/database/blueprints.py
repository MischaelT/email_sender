import os

from blueprints.database.views import (SearchWebsitesView, SuccesfulUpdateView,
                                       SuggestWebsitesView, WebsiteDeleteView,
                                       WebsiteUpdateView)
from flask import Blueprint

template_folder = os.path.join(os.getcwd(), 'app', 'templates', 'database')

db_blueprint = Blueprint('database', __name__, template_folder=template_folder)


db_blueprint.add_url_rule("/search", view_func=SearchWebsitesView.as_view("database"))
db_blueprint.add_url_rule("/delete_website/<int:website_id>", view_func=WebsiteDeleteView.as_view("delete_website"))
db_blueprint.add_url_rule("/update_website/<int:website_id>", view_func=WebsiteUpdateView.as_view("update_website"))
db_blueprint.add_url_rule("/update_website/success", view_func=SuccesfulUpdateView.as_view("update_successful"))
db_blueprint.add_url_rule("/suggest_websites", view_func=SuggestWebsitesView.as_view("suggest_websites"))
