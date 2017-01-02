# coding: utf-8

from leancloud import ACL
from flask import Blueprint
from flask import url_for
from flask import redirect
from flask import render_template

from models import Post
from models import Tag
from models import TagPostMap
from models import Attachment
from models import User

admin_view = Blueprint('admin', __name__, template_folder='template')


@admin_view.route('')
@admin_view.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard.html')


@admin_view.route('/post_list')
def library():
    return render_template('admin/post_list.html')


@admin_view.route('/post')
def editor():
    return render_template('admin/post.html')


@admin_view.route('/post', methods=['POST'])
def submit_post(post=None):
    if not post:
        return "creating new post"
    elif post and isinstance(post, Post):
        return "editing a post"
    else:
        return "fuck you"


@admin_view.route('/image_list')
def images():
    return render_template('admin/image_list.html')


@admin_view.route('/image')
def image_uploader():
    return render_template('admin/image.html')


@admin_view.route('/image', methods=['POST'])
def submit_image(attachment=None):
    if not attachment:
        return "uploading new image"
    elif attachment and isinstance(attachment, Attachment):
        return "editing image metadata"
    else:
        return "fuck you"


@admin_view.route('/tag_list')
def tags():
    return render_template('admin/tag_list.html')


@admin_view.route('/tag')
def tag():
    return render_template('admin/tag.html')


@admin_view.route('/tag', methods=['POST'])
def submit_tag(tag=None):
    if not tag:
        return "creating new tag"
    elif tag and isinstance(tag, Tag):
        return "modifying a tag"
    else:
        return "fuck you"
