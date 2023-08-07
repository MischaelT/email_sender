import datetime

from blueprints.account.forms import DateForm
from extensions import manager
from flask.templating import render_template
from flask.views import MethodView


class ChangeTodayView(MethodView):
    def get(self):
        form = DateForm()
        return render_template('account/change_today.html', form=form)

    def post(self):
        form = DateForm()
        if form.validate_on_submit():
            date = form.data['dt']
            manager.set_up_today(datetime.datetime.strftime(date, '%Y-%m-%d'))

        return render_template('account/change_today.html', form=form)
