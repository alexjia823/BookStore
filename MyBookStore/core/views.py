from flask import render_template, request, Blueprint
from MyBookStore.models import BlogPost
from MyBookStore.helper.constants import HOME_STARTPAGE, HOME_NUM_PERPAGE, REQUEST_ARGS_TYPE, FILENAME_HOMEPAGE, \
    FILENAME_ABOUTUS

core = Blueprint('core', __name__)

@core.route('/')
def index():
    '''
    这是主页视图，暂时将posts放于此。
    '''
    page = request.args.get(REQUEST_ARGS_TYPE, HOME_STARTPAGE, type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=HOME_NUM_PERPAGE)
    return render_template(FILENAME_HOMEPAGE, blog_posts=blog_posts)


@core.route('/info')
def info():
    '''
    关于页面，然后会加书架页面，支付页面，联系方式页面及其它。
    '''
    return render_template(FILENAME_ABOUTUS)
