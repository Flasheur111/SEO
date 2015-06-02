from flask import Blueprint, render_template

home = Blueprint('home', __name__, url_prefix='/home')

@home.route('/', methods=['GET'])
def index():
    return render_template('/home/welcome.html')