from flask import Blueprint

bp = Blueprint('amalgamation', __name__, url_prefix='/amalgamation')


@bp.route('/hello')
def hello():
    return 'hello'
