from business_logic.const import FIRST, FOURTH, INITIAL, SECOND, THIRD

from extensions import executor, manager
from flask import redirect, url_for
from flask.templating import render_template
from flask.views import MethodView


class RunSendingView(MethodView):

    def dispatch_request(self, *args, **kwargs):
        if manager.send_manager.is_active:
            return redirect(url_for('sender.sending'))
        else:
            return super().dispatch_request(*args, **kwargs)

    def get(self):
        todays_data = manager.data_manager.initialize_email_data()
        initial_list = todays_data[INITIAL]
        first_follow_up = todays_data[FIRST]
        second_follow_up = todays_data[SECOND]
        third_follow_up = todays_data[THIRD]
        fourth_follow_up = todays_data[FOURTH]

        return render_template('sender/run_sending.html', initial_list=initial_list,
                               second_follow_up=second_follow_up, first_follow_up=first_follow_up,
                               third_follow_up=third_follow_up, fourth_follow_up=fourth_follow_up)

    def post(self):
        if not manager.send_manager.is_active:
            executor.submit(manager.send_manager.run_sending)
        return redirect(url_for('sender.sending'))


class SendingView(MethodView):
    def get(self):
        if manager.send_manager.is_active:
            current_website = manager.send_manager.current_website_info
            return render_template('sender/sending.html', current_website=current_website)

        if manager.send_manager.is_finished:
            if not manager.send_manager.sending_errors:
                action = 'finished sending process'
                return render_template('succesfully.html', action=action)
            else:
                return render_template('sender/errors_during_sending.html', errored_websites=manager.send_manager.sending_errors)

        return redirect(url_for('sender.run_sending'))
