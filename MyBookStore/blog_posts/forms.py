from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from MyBookStore.helper.constants import FORM_FIELD_TITLE, FORM_FIELD_TEXTAREA, FORM_FIELD_BLOGPOST

class BlogPostForm(FlaskForm):
    #不能有空标题或文字
    title = StringField(FORM_FIELD_TITLE, validators = [DataRequired()])
    text = TextAreaField(FORM_FIELD_TEXTAREA, validators = [DataRequired()])
    submit = SubmitField(FORM_FIELD_BLOGPOST)
