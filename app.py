# coding: utf-8

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import abort
from markdown import markdown

from leancloud import Engine
from leancloud import LeanEngineError
from leancloud import ACL
from leancloud import LeanCloudError

from models import Post
from models import Tag
from models import TagPostMap
from models import Attachment
from models import User
from models import PostPage
from models import TagPage
from utils import parse_tag_names
from utils import allowed_file
from views.admin import admin_view


app = Flask(__name__)

# Required for LeanEngine
engine = Engine(app)


app.register_blueprint(admin_view, url_prefix='/admin')


@app.route('/')
def index(post_per_page=10):
    current_page = 1
    if 'page' in request.args.keys():
        current_page = int(request.args.get('page'))
    try:
        page = PostPage(post_per_page, current_page)
        posts = page.posts()
        next = page.has_next
    except LeanCloudError as e:
        if e.code == 101:
            posts, more = None, False
        else:
            raise e
    return render_template('post_list.html', posts=posts, next=next, page=current_page)


@app.route('/post/new')
def post_form():
    current_user = User.get_current()
    if not current_user:
        flash('info', 'You have to login to see the good stuff.')
        return redirect(url_for('login'))
    current_user.fetch()
    return render_template('editor.html', current_user=current_user)


@app.route('/post/new', methods=['POST'])
def new_post():
    author = User.get_current()
    title, content = request.form['title'], request.form['content']
    tag_names = parse_tag_names(request.form['tags'])

    f = request.files['featured_image']
    if f.filename == '':
        featured_image = None
    else:
        featured_image = Attachment(f.filename, data=f.stream)
    if featured_image and not allowed_file(featured_image.extension):
        flash('warning', 'Upload a proper image.')
        return redirect(url_for('post_form'))

    post = Post()
    post.set({
        'title': title,
        'content': content,
        'marked_content': markdown(content),
        'author': author
    })
    if featured_image:
        post.set('featured_image', featured_image)

    acl = ACL()
    acl.set_public_read_access(True)
    acl.set_write_access(author.id, True)
    post.set_acl(acl)

    post.save()

    tags = []
    for name in tag_names:
        tag = Tag.get_by_name(name)
        if not tag:
            tag = Tag()
            tag.name = name
        tags.append(tag)
    for tag in tags:
        m = TagPostMap()
        m.set({'tag': tag, 'post': post})
        m.save()
        tag.increment('post_count')
    Tag.save_all(tags)

    return redirect(url_for('show_post', post_id=post.id))


@app.route('/post/<post_id>')
def show_post(post_id):
    try:
        post = Post.query.include('author').get(post_id)
    except LeanCloudError as e:
        if e.code == 101:
            abort(404)
        else:
            raise e
    tags = TagPostMap.get_tags_by_post(post)
    return render_template('post.html', post=post, tags=tags)


@app.route('/tag/<tag_name>')
def tag_index(tag_name, post_per_page=10):
    current_page = 1
    if 'page' in request.args.keys():
        current_page = int(request.args.get('page'))
    try:
        tag = Tag.get_by_name(tag_name)
        page = TagPage(post_per_page, current_page, tag)
        posts = page.posts()
        next = page.has_next
    except LeanCloudError as e:
        if e.code == 101:
            tag, posts, more = None, None, False
        else:
            raise e
    return render_template('post_list.html', tag=tag, posts=posts, next=next, page=current_page)


@app.route('/user/login')
def login_form():
    return render_template('login.html')


@app.route('/user/login', methods=['POST'])
def login():
    username, password = request.form['username'], request.form['password']
    user = User()
    user.login(username, password)
    if 'next' in request.args.keys():
        return redirect(request.args.get('next'))
    else:
        return redirect('index')


@app.route('/user/logout')
def logout():
    current_user = User.get_current()
    current_user.logout()
    flash('info', 'Logged out.')
    return redirect(url_for('index'))
