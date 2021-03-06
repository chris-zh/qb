import os
import bleach
from flask import jsonify
from flask import abort
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import make_response
from flask_login import current_app
from flask_login import current_user
from flask_login import login_required

from . import main
from .forms import BookmarkForm
from .forms import CommentForm
from .forms import EditProfileAdminForm
from .forms import EditProfileForm
from .forms import MailForm
from .forms import PostForm

from .. import db
from ..decorators import admin_required
from ..decorators import permission_required
from ..email import send_email_cust
from ..fileProcess import make_thumb
from ..models import Bookmark
from ..models import Comment
from ..models import Role
from ..models import Permission
from ..models import Post
from ..models import User
from ..orcl_models import Overtime
from markdown import markdown


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)


@main.route('/edit-profile', methods=['POST', 'GET'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.location.data
        save_image(form.image.data)
        db.session.add(current_user)
        flash('你的个人资料已修改成功.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['POST', 'GET'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        save_image(form.image.data)
        db.session.add(user)
        flash('你的个人资料已修改成功.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.row_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/', methods=['POST', 'GET'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config[
        'FLASKY_POSTS_PER_PAGE'],
                                                                     error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts, pagination=pagination)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash('发布成功.')
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)


def test_admin(username, permission):
    user = User.query.filter_by(username=username).first()
    new_permission = Permission.ADMINISTER
    if permission:
        new_permission = permission
    user.role.permissions = new_permission
    db.session.add(user)
    db.session.commit()


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('非法用户.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followers of",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('非法用户.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('你已经关注了这个用户.')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    flash('你正在关注 %s.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/followed-by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('非法用户.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('非法用户.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('你没有关注这个用户.')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    flash('你将不再关注 %s .' % username)
    return redirect(url_for('.user', username=username))


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        flash('评论已发布.')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
               current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('moderate.html', comments=comments,
                           pagination=pagination, page=page)


@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))


@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']


# 保存用户头像
def save_image(file):
    try:
        filename = file.filename
        user = current_user._get_current_object()
        tmp_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(tmp_file_path)
        small_image = make_thumb(tmp_file_path, 'small', current_app.config['SMALL_IMAGE_SIZE'])
        big_image = make_thumb(tmp_file_path, 'big', current_app.config['BIG_IMAGE_SIZE'])
        user.small_image = small_image
        user.big_image = big_image
        db.session.add(user)
        os.remove(tmp_file_path)
        return True
    except IOError:
        return False


@main.route('/tool-index')
def tool_index():
    return render_template('tool_index.html')


@main.route('/tool-bookmark', methods=['POST', 'GET'])
def tool_bookmark():
    form = BookmarkForm()
    bookmarks = Bookmark.query.all()
    if form.validate_on_submit():
        new_bookmark = Bookmark(name=form.name.data, url=form.url.data)
        db.session.add(new_bookmark)
        return redirect(url_for('.tool_bookmark'))
    return render_template('tool_bookmark.html', bookmarks=bookmarks, form=form)


@main.route('/tool-mail', methods=['POST', 'GET'])
def tool_mail():
    form = MailForm()
    if form.validate_on_submit():
        receivers = form.receiver.data
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        body_html = bleach.linkify(
            bleach.clean(markdown(form.context.data, ouput_format='html'), tags=allowed_tags, strip=True))
        send_email_cust(form.sender.data, receivers, form.subject.data, body_html)
        print(markdown(form.context.data, ouput_format='html'))
        print(body_html)
        return redirect(url_for('.tool_mail'))
    return render_template('tool_mail.html', form=form)


@main.route('/tool-overtime', methods=['POST', 'GET'])
def tool_overtime():
    current_version = '375'
    week_number = '1'
    if request.method == 'POST':
        data = request.form.to_dict()
        is_exist = Overtime.query.filter_by(apply_name=data['apply_name'], week_number=data['week_number']).first()
        if not is_exist:
            new_overtime = Overtime(apply_name=data['apply_name'], apply_reason=data['apply_reason'],
                                    current_version=data['current_version'],
                                    week_number=data['week_number'])
            db.session.add(new_overtime)
        return redirect(url_for(".tool_overtime"))
        # data = request.get_json(force=True)
        # print(data)
        # print(data['apply_name'])

        # new_dict = {}
        # otstr = '{'
        # for new_ot in new_overtimes:
        #     otstr = otstr + new_ot.apply_name + ':' + new_ot.apply_reason + ','
        # otstr = otstr[: len(otstr) - 1] + '}'
        # print(jsonify(otstr))
        # new_data = {"new_overtimes": otstr}
        # return jsonify(new_data)
        # # return make_response(new_overtime=new_overtime)
    overtimes = Overtime.query.filter_by(current_version=current_version, week_number=week_number).all()
    return render_template('tool_overtime.html', overtimes=overtimes, current_version=current_version,
                           week_number=week_number)
