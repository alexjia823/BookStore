from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from MyBookStore.helper.constants import *
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from MyBookStore.models import User


class LoginForm(FlaskForm):
    email = StringField(FORM_FIELD_EMAIL, validators=[DataRequired(), Email()])
    password = PasswordField(FORM_FIELD_PASS, validators=[DataRequired()])
    submit = SubmitField(FORM_FIELD_LOGIN)


class RegistrationForm(FlaskForm):
    email = StringField(FORM_FIELD_EMAIL, validators=[DataRequired(), Email()])
    username = StringField(FORM_FIELD_USERNAME, validators=[DataRequired()])
    password = PasswordField(FORM_FIELD_PASS,
                             validators=[DataRequired(), EqualTo(FORM_FILED_PASS_CONFIRM, message=FORM_PASS_MATCH)])
    pass_confirm = PasswordField(FORM_FILED_PASS_CONFIRM, validators=[DataRequired()])
    submit = SubmitField(FORM_FIELD_REGISTER)

    def check_email(self, field):
        # 检查邮箱是否注册过
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(FORM_DUP_EMAIL)

    def check_username(self, field):
        # 检查用户名是否用过
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(FORM_DUP_USERNAME)

class UpdateUserForm(FlaskForm):
    email = StringField(FORM_FIELD_EMAIL, validators=[DataRequired(), Email()])
    username = StringField(FORM_FIELD_USERNAME, validators=[DataRequired()])
    picture = FileField(FORM_FIELD_UPDATE_PROFILE_PIC, validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField(FORM_FIELD_UPDATE)

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(FORM_DUP_EMAIL)

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(FORM_DUP_USERNAME)
