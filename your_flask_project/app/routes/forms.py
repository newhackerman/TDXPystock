# app/routes/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp, Optional

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Regexp(r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class StockCodeForm(FlaskForm):
    stock_code = StringField('Stock Code (e.g., sh600000 or 000001)',
                             validators=[DataRequired(), Length(min=6, max=10)])
    submit = SubmitField('Scan Risk')

class FundDataSelectionForm(FlaskForm):
    indicator_choices = [
        ("今日", "今日 (Today)"),
        ("3日", "3日 (3-Day)"),
        ("5日", "5日 (5-Day)"),
        ("10日", "10日 (10-Day)")
    ]
    indicator = SelectField('Ranking Period (指标)', choices=indicator_choices, default="今日")
    min_main_force_percent = FloatField('Min Main Force Net Inflow % (最小主力净流入占比)',
                                        validators=[Optional()],
                                        description="Optional: e.g., 5 for 5%")
    submit = SubmitField('Find Stocks')
