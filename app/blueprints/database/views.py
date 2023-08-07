from settings import TODAY_DATE
from blueprints.database.forms import (AddToWorkForm, MultipleEmailsForm,
                                       PostponeForm, SubmitForm)
from business_logic.const import HISTORY, WORK
from business_logic.data.validators import is_valid, the_same_emails
from business_logic.mics import date_by_adding_days
from extensions import executor, manager
from flask import redirect, request, session, url_for
from flask.templating import render_template
from flask.views import MethodView, View
from models import Prospect, Website, db


class SearchWebsitesView(MethodView):

    def get(self):
        return render_template('database/database.html')

    def post(self):
        website_address = request.form['website']
        website_name = website_address.split('.')[0].lower()

        database_type = request.form['option']

        if database_type == WORK:
            result = Website.get_website_by_Name_isActive(db.session, website_name, int(True))
        elif database_type == HISTORY:
            result = Website.get_website_by_Name_isActive(db.session, website_name, int(False))

        return render_template('database/database.html', data=result)

# TODO Implement the sawe websites deleting
class WebsiteDeleteView(MethodView):

    def get(self, website_id):
        try:
            website = Website.get_website_by_id(db.session, website_id)
        except IndexError:
            reason = 'there is no such website in database'
            return render_template('ooops.html', reason=reason)

        return render_template('database/delete_website.html', website_name=website.website_name, id_for_delete=website_id)

    def post(self, website_id):
        try:
            website = Website.get_website_by_id(db.session, website_id)
        except IndexError:
            reason = 'this website has already been deleted'
            return render_template('ooops.html', reason=reason)
        db.session.delete(website)
        db.session.commit()

        action = f'deleted website {website.website_name}'

        return render_template('succesfully.html', action=action)


# BUG If change one email than push back, change another ang press udate, the wrong word would be displayed
class WebsiteUpdateView(MethodView):

    def get(self, website_id):
        try:
            website = Website.get_website_by_id(db.session, website_id)
        except IndexError:
            reason = 'this website has already been deleted'
            return render_template('ooops.html', reason=reason)

        init_values = {'website_name': website.website_name, 'emails': website.emails}
        emails_form = MultipleEmailsForm(data=init_values)

        for email_form, email in zip(emails_form.emails, website.emails):
            email_form.email.data = email.email_address

        return render_template('database/update_website.html', website_name=website.website_name, form=emails_form)

# TODO Doesnt show updated emails
    def post(self, website_id):

        try:
            website = Website.get_website_by_id(db.session, website_id)
        except IndexError:
            reason = 'this website has already been deleted'
            return render_template('ooops.html', reason=reason)

        emails_form = MultipleEmailsForm()

        if not emails_form.validate_on_submit():
            return render_template('database/update_website.html', website_name=website.website_name, form=emails_form)

        emails_deleted = []
        emails_updated = []

        for field in emails_form.emails:

            email_address_form = field.email.data.strip()
            email_id_form = field.email_id.data

            try:
                email_from_db = Prospect.get_prospects_by_prospect_id(db.session, email_id_form)
            except IndexError:
                reason = f"this email {session['emails_deleted'][0]} does not exists in database"
                return render_template('ooops.html', reason=reason)

            if not email_address_form:
                emails_deleted.append(email_from_db.email_address)
                db.session.delete(email_from_db)
            else:
                if is_valid(email_address_form):
                    if not the_same_emails(email_address_form, email_from_db.email_address):
                        emails_updated.append(email_from_db.email_address)
                        email_from_db.email_address = email_address_form

        if len(emails_deleted) < len(emails_form.emails) or emails_updated:
            db.session.commit()

        if len(emails_deleted) == len(emails_form.emails):
            website.next_email_date = date_by_adding_days(from_date=str(TODAY_DATE), add_days=80)
            website.process_is_active = 0
            website.process_start_date = None
            website.stage = None
            db.session.commit()
            session['website_deleted'] = True
        else:
            db.session.commit()
            session['website_deleted'] = False

        db.session.commit()

        session['website_name'] = website.website_name
        session['emails_updated'] = emails_updated
        session['emails_deleted'] = emails_deleted

        return redirect(url_for('database.update_successful'))


class SuggestWebsitesView(MethodView):

    def get(self):
        move_to_work_form = AddToWorkForm()
        postpone_form = PostponeForm()
        submit = SubmitForm()
        websites = Website.websites_by_isActive_nextEmailDate(db.session, int(False), manager.today)
        return render_template('database/suggest_websites.html', websites=websites, postpone_form=postpone_form,
                               move_to_work_form=move_to_work_form, submit_form=submit, enumerat=enumerate)

    def post(self):
        move_to_work_form = AddToWorkForm()
        postpone_form = PostponeForm()
        submit = SubmitForm()

        if move_to_work_form.add.data and move_to_work_form.validate_on_submit():
            # TODO Check out how to do it correctly
            website_id = request.query_string.decode().split('=')[1]
            website = Website.get_website_by_id(db.session, website_id)
            website.process_is_active = int(True)
            website.stage = 0
            website.next_email_date = manager.today
            website.process_start_date = manager.today
        elif postpone_form.postpone.data and postpone_form.validate_on_submit():
            # TODO Check out how to do it correctly
            website_id = request.query_string.decode().split('=')[1]
            website = Website.get_website_by_id(db.session, website_id)
            add_days = postpone_form.days.data
            website.next_email_date = date_by_adding_days(from_date=str(manager.today), add_days=add_days)
        # TODO Implement functionality
        elif submit.is_submitted():
            manager.checker.date = manager.today
            executor.submit(manager.checker.fetch_info_from_list_to_database)
            redirect(url_for('checker_run'))

        db.session.commit()
        websites = Website.websites_by_isActive_nextEmailDate(db.session, int(False), manager.today)

        return render_template('database/suggest_websites.html', websites=websites, postpone_form=postpone_form,
                               move_to_work_form=move_to_work_form, submit_form=submit, enumerat=enumerate)


class SuccesfulUpdateView(View):
    def dispatch_request(self):
        website_name = session['website_name']
        emails_deleted = session['emails_deleted']
        website_deleted = session['website_deleted']
        return render_template('database/succesfull_update.html', website_name=website_name, emails_deleted=emails_deleted, website_deleted=website_deleted)
