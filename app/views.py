import config

from flask.templating import render_template
from flask.views import MethodView

from models import Users, db


class IndexView(MethodView):

    def get(self):

        user = Users.get_user_by_name(db.session, config.SHORT_NAME)
        money_maked = round(int(user.websites_processed) * 0.12 + int(user.emails_sent) * 0.12 + int(user.replied) * 0.6, 2)
        in_usd = round(0.73 * money_maked + money_maked * 0.05, 2)
        return render_template('index.html', name=user.user_name, websites_contacted=user.websites_processed,
                               folow_ups_sent=user.emails_sent, money=money_maked, in_usd=in_usd)

    def post(self):
        user = Users.get_user_by_name(db.session, config.SHORT_NAME)
        money_maked = round(int(user.websites_processed) * 0.12 + int(user.emails_sent) * 0.12 + int(user.replied) * 0.6, 2)
        in_usd = round(0.73 * money_maked + money_maked * 0.05, 2)

        return render_template('index.html', name=user.user_name, websites_contacted=user.websites_processed,
                               folow_ups_sent=user.emails_sent, money=money_maked, in_usd=in_usd)
