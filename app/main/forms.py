from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import Required, Length, Email, Regexp, ValidationError
from ..models import Role, User
from flask_pagedown.fields import PageDownField
from wtforms import FileField


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


class EditProfileForm(Form):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    image = FileField('头像')
    submit = SubmitField('Submit')


class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, '
                                                                         'numbers, dots or underscores'
                                          )
    ])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    image = FileField('头像')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered. ')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use. ')


class PostForm(Form):
    body = PageDownField("What's on your mind? ", validators=[Required()])
    submit = SubmitField('Submit')


class CommentForm(Form):
    body = StringField('', validators=[Required()])
    submit = SubmitField('Submit')


class BookmarkForm(Form):
    name = StringField('书签名', validators=[Required()])
    url = StringField('URL', validators=[Required()])
    submit = SubmitField('提交')


class MailForm(Form):
    sender = StringField('发件人', validators=[Required()])
    receiver = StringField('收件人', validators=[Required()])
    subject = StringField('标题', validators=[Required()])
    context = TextAreaField('内容(支持markdown格式)', validators=[Required()])
    submit = SubmitField('发送')
