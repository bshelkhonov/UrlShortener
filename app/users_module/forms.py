from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, EqualTo

# from .models import User
#
#
# class LoginForm(FlaskForm):
#     username = StringField("Username", validators=[DataRequired()])
#     password = PasswordField("Password", validators=[DataRequired()])
#     submit = SubmitField("Login")
#
#
# class RegisterForm(FlaskForm):
#     username = StringField("Username", validators=[DataRequired()])
#     password = PasswordField("Password", validators=[DataRequired()])
#     submit = SubmitField("Register")
#
#     def validate_username(self, username):
#         user = User.query.filter_by(username=username.data).first()
#         if user is not None:
#             raise ValidationError("Please use a different username")
