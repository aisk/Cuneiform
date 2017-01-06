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


class TagPage(Query):

    def __init__(self, post_per_page, current_page, tag=None):
        super(TagPage, self).__init__(TagPostMap)
        if not tag:
            raise TypeError('No tag found')
        if not isinstance(tag, Tag):
            raise TypeError('Tag should be instance of Tag')
        self._tag = tag
        self._post_per_page = post_per_page
        self._current_page = current_page

    def posts(self):
        self.has_next = False
        self.add_descending('createdAt')
        self.equal_to('tag', self._tag)
        self.include('post')
        self.limit(self._post_per_page + 1)
        self.skip((self._current_page - 1) * self._post_per_page)
        items = [x.get('post') for x in self.find()]
        if len(items) - self._post_per_page == 1:
            self.has_next = True
            items = items[:-1]
        return items


class PostPage(Query):

    def __init__(self, post_per_page, current_page):
        super(PostPage, self).__init__(Post)
        self._post_per_page = post_per_page
        self._current_page = current_page

    def posts(self):
        self.has_next = False
        self.add_descending('createdAt')
        self.limit(self._post_per_page + 1)
        self.skip((self._current_page - 1) * self._post_per_page)
        items = self.find()
        if len(items) - self._post_per_page == 1:
            self.has_next = True
            items = items[:-1]
        return items
