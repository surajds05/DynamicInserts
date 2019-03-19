from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField, SelectField
from wtforms.validators import DataRequired, NumberRange
from datetime import date, timedelta


class InputsForm(FlaskForm):
    domain = SelectField(label='Domains', choices=[('deveng','deveng'),('t18bx','t18bx')])
    parentTableName = StringField('Parent Table Name', validators=[DataRequired()])
    recordCnt = IntegerField('Number of records to insert', validators=[DataRequired(), NumberRange(min=1, max=10)])
    varcharPrefix = StringField('Prefix for the varchar fields')
    beginDttm = DateField('Begin date', default=date.today() - timedelta(days=10))
    fetchChildTables = SubmitField('Fetch Child Tables')