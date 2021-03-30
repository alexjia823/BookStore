from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_required
from MyBookStore import db
from MyBookStore.models import BlogPost
from MyBookStore.blog_posts.forms import BlogPostForm
from MyBookStore.helper.constants import HTTP_FORBIDDEN, BLOG_POST_CREATE, FILENAME_CREATE_POST, FILENAME_BLOG_POST, \
BLOG_POST_UPDATED, BLOG_POST_DELETED, HTTP_METHOD_GET, BLOG_POST_UPDATE_TITLE


blog_posts = Blueprint('blog_posts', __name__)


@blog_posts.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():
        blog_post = BlogPost(title=form.title.data,
                             text=form.text.data,
                             user_id=current_user.id
                             )
        db.session.add(blog_post)
        db.session.commit()
        flash(BLOG_POST_CREATE)
        return redirect(url_for('core.index'))

    return render_template(FILENAME_CREATE_POST, form=form)


# int：确保blog_post_id以整数形式传递
# 而不是字符串，以便稍后查找。
@blog_posts.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    # 按ID号获取请求的博客帖子或返回404
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    return render_template(FILENAME_BLOG_POST, title=blog_post.title,
                           date=blog_post.date, post=blog_post
                           )


@blog_posts.route("/<int:blog_post_id>/update", methods=['GET', 'POST'])
@login_required
def update(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        # 禁止访问
        abort(HTTP_FORBIDDEN)

    form = BlogPostForm()
    if form.validate_on_submit():
        blog_post.title = form.title.data
        blog_post.text = form.text.data
        db.session.commit()
        flash(BLOG_POST_UPDATED)
        return redirect(url_for('blog_posts.blog_post', blog_post_id=blog_post.id))
    # 回传旧的博客文章信息，以便我们进行编辑
    # 旧的文字和标题。
    elif request.method == HTTP_METHOD_GET:
        form.title.data = blog_post.title
        form.text.data = blog_post.text
    return render_template(FILENAME_CREATE_POST, title=BLOG_POST_UPDATE_TITLE,
                           form=form)


@blog_posts.route("/<int:blog_post_id>/delete", methods=['POST'])
@login_required
def delete_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(HTTP_FORBIDDEN)
    db.session.delete(blog_post)
    db.session.commit()
    flash(BLOG_POST_DELETED)
    return redirect(url_for('core.index'))
