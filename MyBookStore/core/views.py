from flask import render_template,request,Blueprint
from MyBookStore.models import BlogPost

core = Blueprint('core',__name__)

@core.route('/')
def index():
    '''
    这是主页视图，暂时将posts放于此。
    '''
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=10)
    return render_template('index.html',blog_posts=blog_posts)

@core.route('/info')
def info():
    '''
    关于页面，然后会加书架页面，支付页面，联系方式页面及其它。
    '''
    return render_template('info.html')
