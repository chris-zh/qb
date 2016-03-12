from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import Required, Length, Email, Regexp, ValidationError
from ..models import Role, User
from flask_pagedown.fields import PageDownField
from wtforms import FileField


class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('发布')


class EditProfileForm(Form):
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('位置', validators=[Length(0, 64)])
    about_me = TextAreaField('关于我')
    image = FileField('头像')
    submit = SubmitField('保存')


class EditProfileAdminForm(Form):
    email = StringField('邮箱', validators=[Required(), Length(1, 64), Email()])
    username = StringField('用户名', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, '用户名只能包含字母，数字，英文句点和下划线'

                                          )
    ])
    confirmed = BooleanField('Confirmed')
    role = SelectField('角色', coerce=int)
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('位置', validators=[Length(0, 64)])
    about_me = TextAreaField('关于我')
    image = FileField('头像')
    submit = SubmitField('保存')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已注册. ')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已注册. ')


class PostForm(Form):
    body = PageDownField("有什么新鲜事想告诉大家? ", validators=[Required()])
    submit = SubmitField('发布')


class CommentForm(Form):
    body = StringField('', validators=[Required()])
    submit = SubmitField('发布')


class BookmarkForm(Form):
    name = StringField('书签名', validators=[Required()])
    url = StringField('URL', validators=[Required()])
    submit = SubmitField('保存')


class MailForm(Form):
    sender = StringField('发件人', validators=[Required()])
    receiver = StringField('收件人', validators=[Required()])
    subject = StringField('标题', validators=[Required()])
    context = TextAreaField('内容(支持markdown格式)', validators=[Required()])
    submit = SubmitField('发送')
