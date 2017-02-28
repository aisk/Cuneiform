from flask import render_template, request
from app import app
from helpers import validate_form_data
from models import Post


@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
def error_page(e):
	return render_template("errors/%i.html" % e.code), e.code


@app.route("/")
def front_page():
	return render_template("index.html")


@app.route("/posts/")
def post_list():
	posts = Post.query.add_ascending('createdAt').limit(10).find()
	return render_template("post_list.html", posts=posts)


@app.route("/posts/<string:post_id>")
def post(post_id):
	post = Post.query.get(post_id)
	return render_template("post.html", post=post)


@app.route("/login")
def login_form():
	return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
	pass


@app.route("/logout")
def logout():
	pass


@app.route("/posts/new")
def post_editor():
	return render_template("post_editor.html")


@app.route("/posts/new", methods=["POST"])
def create_post():
	print(validate_form_data(request.form))
	return render_template("post_editor.html")


@app.route("/posts/<string:post_id>", methods=["POST"])
def update_post(post_id):
	return render_template("post_editor.html")


@app.route("/posts/<string:post_id>/delete")
def delete_post(post_id):
	return render_template("post.html")
