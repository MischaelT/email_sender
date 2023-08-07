from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields import FieldList, FormField, IntegerField
from wtforms.fields.datetime import DateField
from wtforms.fields.simple import EmailField, HiddenField, StringField
from wtforms.validators import InputRequired


class EmailsDataForm(FlaskForm):
    email_id = HiddenField(label='id')
    email = EmailField('')
    # email = EmailField('', validators = [validators.DataRequired()])


class MultipleEmailsForm(FlaskForm):
    website_name = StringField('Website Name')
    emails = FieldList(FormField(EmailsDataForm), min_entries=1, max_entries=20)
    submit = SubmitField('Update Database', render_kw={'type': 'submit'})


class SubmitForm(FlaskForm):
    submit = SubmitField('submit', render_kw={'type': 'submit', 'value': 'submit'})


class NewWebsiteForm(FlaskForm):
    website_name = StringField('Website Name')
    emails = FieldList(FormField(EmailsDataForm), min_entries=3, max_entries=3)
    dt = DateField('DatePicker', validators=([InputRequired()]))
    submit = SubmitField('Add website', render_kw={'type': 'submit'})


class PostponeForm(FlaskForm):
    days = IntegerField()
    postpone = SubmitField('postpone', render_kw={'type': 'submit', 'value': 'postpone'})


class AddToWorkForm(FlaskForm):
    add = SubmitField('add', render_kw={'type': 'submit'})
