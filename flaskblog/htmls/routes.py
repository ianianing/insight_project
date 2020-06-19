from flask import render_template
from flask import Blueprint

htmls = Blueprint('htmls', __name__)


@htmls.route('/htmls/selector')
def selector():
    return render_template('html_prs/selector.html')

@htmls.route('/htmls/visual')
def visual():
    return render_template('html_prs/visual.html')

@htmls.route('/htmls/display')
def display():
    return render_template('html_prs/display.html')

@htmls.route('/htmls/color')
def color():
    return render_template('html_prs/color.html')

@htmls.route('/htmls/typography')
def typography():
    return render_template('html_prs/typography.html')

@htmls.route('/htmls/box')
def box():
    return render_template('html_prs/box.html')

@htmls.route('/htmls/box2')
def box2():
    return render_template('html_prs/box2.html')

@htmls.route('/htmls/gridp1')
def grid_practice():
    return render_template('html_prs/grid.html')

@htmls.route('/htmls/gridp2')
def grid_practice2():
    return render_template('html_prs/gridp2.html')

@htmls.route('/htmls/table')
def table():
    return render_template('html_prs/table.html')

@htmls.route('/htmls/form')
def form():
    return render_template('html_prs/form.html')

@htmls.route('/htmls/form2')
def form2():
    return render_template('html_prs/form2.html')

@htmls.route('/htmls/submission', methods=['POST'])
def submssion():
    return render_template('html_prs/submission.html')

@htmls.route('/htmls/submission2', methods=['GET'])
def submssion2():
    return render_template('html_prs/submission2.html')

@htmls.route('/htmls/basic')
def basic():
    return render_template('html_prs/basic.html')

@htmls.route('/htmls/basic_about')
def basic_about():
    return render_template('html_prs/basic_about.html')

@htmls.route('/htmls/semantic')
def semantic():
    return render_template('html_prs/semantic.html')