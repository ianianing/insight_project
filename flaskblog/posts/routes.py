# create a blueprints which only contains posts routes
from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm
from flask_login import current_user, login_required


posts = Blueprint('posts', __name__)


# routes for new posts that require user to login
@posts.route("/post/new", methods=['GET','POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		# save post into database and display it
		post = Post(title=form.title.data, content=form.content.data, author= current_user)
		db.session.add(post)
		db.session.commit()
		flash('Your post has been created!', 'success')
		return redirect(url_for('main.home'))
	return render_template('create_post.html', title='New Post', form=form, legend='New Post')

# create route take up to a specific page for single page, use int: here because we expect post_id we use is an integer
@posts.route("/post/<int:post_id>")
def post(post_id):
	post = Post.query.get_or_404(post_id) # give me a post with this id, if it doesn't exist, then return a 404 page
	return render_template('post.html', title=post.title, post=post)

# create route to update post
@posts.route("/post/<int:post_id>/update", methods=['GET','POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	# if author is not current user, can't update
	if post.author != current_user:
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit() # don't need add here because we are just updating, post is already existed in the database
		flash('Your post has been updated!', 'success')
		return  redirect(url_for('posts.post', post_id=post.id))
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
	return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

# create route to delete post
@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	# if author is not current user, can't update
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Your post has been deleted!', 'success')
	return redirect(url_for('main.home'))

