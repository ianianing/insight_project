# create a blueprints which only contains main routes
from flask import Blueprint, render_template, request
from flaskblog.models import Post

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
 #http://localhost:5000/home and http://localhost:5000/ are same now
def home():
	# display post data posted by users at homepage
	# make paginate query, seperate post into different pages
	page = request.args.get('page',1, type=int)  #get current page number, the default is 1
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5,page=page) # get current page's post, 5 posts per page, order be post date in descending order, newest post show up first
	return render_template('home.html',posts=posts) #uses home.html in templates, here I didn't pass title, so default in else

@main.route("/about") # create subpage http://localhost:5000/about
def about():
	return render_template('about.html', title='About') #uses about.html in templates, Here I passed a title, should return if title result
	# title is the content shown on the tab

@main.route("/ml_models")
def ml_models():
	return render_template('ml_models.html', title='ML Model')

@main.route("/htmls")
def htmls():
	return render_template('html_practice.html', title='HTML_practice')