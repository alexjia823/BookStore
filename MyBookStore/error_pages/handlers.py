from flask import Blueprint,render_template
from MyBookStore.helper.constants import HTTP_FORBIDDEN,HTTP_NOTFOUND,FILENAME_403,FILENAME_404

error_pages = Blueprint('error_pages',__name__)

@error_pages.app_errorhandler(HTTP_NOTFOUND)
def error_404(error):
    '''
    404找不到页面。
    '''
    return render_template(FILENAME_404), HTTP_NOTFOUND

@error_pages.app_errorhandler(HTTP_FORBIDDEN)
def error_403(error):
    '''
    403禁止页面。
    '''
    return render_template(FILENAME_403), HTTP_FORBIDDEN
