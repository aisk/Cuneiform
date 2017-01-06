from leancloud import Object
from leancloud import File
from leancloud import Query
from leancloud import LeanCloudError

from datetime import datetime


class Post(Object):

    pass


class Tag(Object):

    def get_post_count(self):
        if self.get('post_count'):
            return self.get('post_count')
        else:
            return 0

    @classmethod
    def get_by_name(cls, name):
        reg = '^' + name + '$'
        try:
            return cls.query.matched('name', reg).first()
        except LeanCloudError as e:
            if e.code == 101:
                return None
            else:
                raise e


class TagPostMap(Object):

    @classmethod
    def get_tags_by_post(cls, post):
        tags = [x.get('tag') for x in cls.query.equal_to('post', post).include('tag').find()]
        if len(tags) == 0:
            return None
        return tags


class User(Object):

    pass


class Attachment(File):

    pass


def get_posts(post_per_page, current_page):
    has_more = False
    query = Query(Post)
    query.add_descending('createdAt')
    query.include('author')
    query.limit(post_per_page + 1)
    query.skip((current_page - 1) * post_per_page)
    items = query.find()
    if len(items) - post_per_page == 1:
        has_more = True
        items = items[:-1]
    return dict(items=items, has_more=has_more)


def get_posts_by_tag(post_per_page, current_page, tag=None):
    has_more = False
    query = Query(TagPostMap)
    query.add_descending('createdAt')
    query.equal_to('tag', tag)
    query.include('post')
    query.limit(post_per_page + 1)
    query.skip((current_page - 1) * post_per_page)
    items = [x.get('post') for x in query.find()]
    if len(items) - post_per_page == 1:
        has_more = True
        items = items[:-1]
    return dict(items=items, has_more=has_more)
