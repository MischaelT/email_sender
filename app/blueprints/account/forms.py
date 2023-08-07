from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields.datetime import DateField
from wtforms.validators import InputRequired


class DateForm(FlaskForm):
    dt = DateField('DatePicker', validators=([InputRequired()]))
    submit_date = SubmitField('Set up', render_kw={'type': 'submit'})


class SubmitForm(FlaskForm):
    submit = SubmitField('submit', render_kw={'type': 'submit', 'value': 'submit'})
