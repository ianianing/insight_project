# create a blueprints which only contains users and authentication routes
from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
from flaskblog import db, bcrypt
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
								   		RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required



users = Blueprint('users', __name__)


@users.route("/register", methods=['GET','POST'])  # create subpage for registration  http://localhost:5000/about
# use methods to accept both get and post request so that people can register
def register():
	# if already logged, redirect to home page. Page login and register won't show up then
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegistrationForm()
	if form.validate_on_submit(): # check if submission valid and pass one time alert
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created! You are now able to log in','success')
		return redirect(url_for('users.login')) # redirect user to homepage after
	return render_template('register.html', title='Register',form=form)

@users.route("/login", methods=['GET','POST']) # create subpage for login  http://localhost:5000/about
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = LoginForm()
	if form.validate_on_submit(): # check if submission valid and pass one time alert
		# check whether user wants to login have right credential
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next') # get argument if next key exist, that is make sure user go to page they are currently at after login. Not just homepage
			return redirect(next_page) if next_page else redirect(url_for('main.home'))
		else:
			flash('Login Unsuccessful. Please check email and password','danger') # if alert is danger, it's shown in red
	return render_template('login.html', title='Login',form=form)

# create a logout route for after login
@users.route("/logout") # create subpage for logout
def logout():
	logout_user()
	return redirect(url_for('main.home'))



# create an account route, user can only see this route if logged in
@users.route("/account",methods=['GET','POST'])
@login_required # to make sure can only see logged in page, right now account page
def account():
	# set image file, 头像
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)  # static directory, under profile_pics folder
	# update current info form
	form = UpdateAccountForm()
	# validate if new username and email is same as current username and email
	if form.validate_on_submit():
		# save new picture as profile picture if exist
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your account has been updated!', 'success')
		return redirect(url_for('users.account'))
	# make current username and email showup
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	return render_template('account.html', title='Account', image_file=image_file, form = form)



# create a route for each user showing all posts from this user
@users.route("/user/<string:username>")
def user_posts(username):
	user = User.query.filter_by(username=username).first_or_404() # get this users' first post or 404
	page = request.args.get('page',1, type=int)  #get current page number, the default is 1
	posts = Post.query.filter_by(author=user)\
			.order_by(Post.date_posted.desc()).paginate(per_page=5,page=page) # get current page's post, 5 posts per page, order be post date in descending order, newest post show up first
	return render_template('user_posts.html',posts=posts,user=user) #uses home.html in templates, here I didn't pass title, so default in else


# route for request password request
@users.route("/reset_password", methods=['GET','POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('main.home')) # if already logged in, redirect to homepage
	form = RequestResetForm()
	if form.validate_on_submit(): # send email to user after user submit request
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('An email has been sent with instructions to reset your password.','info')
		return	redirect(url_for('users.login'))
	return render_template('reset_request.html', title='Reset Password', form=form)

# route for user to reset password
@users.route("/reset_password/<token>", methods=['GET','POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.home')) # if already logged in, redirect to homepage
	user = User.verify_reset_token(token)
	if user is None:
		flash('That is an invalid or expired token','warning')
		return redirect(url_for('users.reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit(): # check if submission valid and pass one time alert
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password # change current user's password in the database
		db.session.commit()
		flash('Your password has been updated! You are now able to log in','success')
		return redirect(url_for('users.login')) # redirect user to homepage after
	return render_template('reset_token.html', title='Reset Password', form=form)