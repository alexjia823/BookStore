from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from MyBookStore import db
from werkzeug.security import generate_password_hash, check_password_hash
from MyBookStore.helper.constants import *
from MyBookStore.models import User, BlogPost
from MyBookStore.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from MyBookStore.users.picture_handler import add_profile_pic

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash(FORM_LOGIN_SUCCESS)
        return redirect(url_for('users.login'))
    return render_template(FILENAME_REGISTER, form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # 通过Email来得到User
        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:
            # 成功登录

            login_user(user)
            flash(FORM_LOGIN_SUCCESS)

            next = request.args.get('next')

            if next == None or not next[0] == '/':
                next = url_for('core.index')

            return redirect(next)
    return render_template(FILENAME_LOGIN, form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('core.index'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateUserForm()

    if form.validate_on_submit():
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(FORM_PROFILE_UPDATE_SUCCESS)
        return redirect(url_for('users.account'))

    elif request.method == HTTP_METHOD_GET:
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template(FILENAME_ACCOUNT, profile_image=profile_image, form=form)


@users.route("/<username>")
def user_posts(username):
    page = request.args.get(REQUEST_ARGS_TYPE, USER_STARTPAGE, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=USER_NUM_PERPAGE)
    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)
