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
@admin_view.route('/post_list')
def post_list():
    return render_template('admin/post_list.html', active="post_list")


@admin_view.route('/post')
def post():
    return render_template('admin/post.html', active="post_list")


@admin_view.route('/post', methods=['POST'])
def post_submit(post=None):
    if not post:
        return "creating new post"
    elif post and isinstance(post, Post):
        return "editing a post"
    else:
        return "fuck you"


@admin_view.route('/image_list')
def image_list():
    return render_template('admin/image_list.html', active="image_list")


@admin_view.route('/image')
def image():
    return render_template('admin/image.html', active="image_list")


@admin_view.route('/image', methods=['POST'])
def image_submit(attachment=None):
    if not attachment:
        return "uploading new image"
    elif attachment and isinstance(attachment, Attachment):
        return "editing image metadata"
    else:
        return "fuck you"


@admin_view.route('/tag_list')
def tag_list():
    return render_template('admin/tag_list.html', active="tag_list")


@admin_view.route('/tag')
def tag():
    return render_template('admin/tag.html', active="tag_list")


@admin_view.route('/tag', methods=['POST'])
def tag_submit(tag=None):
    if not tag:
        return "creating new tag"
    elif tag and isinstance(tag, Tag):
        return "modifying a tag"
    else:
        return "fuck you"
