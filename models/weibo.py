from models import Model
from models.user import User
from utils import current_user


class Weibo(Model):
    def __init__(self, form, user_id=-1):
        self.id = form.get('id', None)
        self.content = form.get('content', '')
        self.user_id = form.get('user_id', user_id)

    def comments(self):
        return Comment.find_all(weibo_id=self.id)

    @classmethod
    def new(cls, form, request):
        t = cls(form)
        t.user_id = current_user(request).id
        t.save()
        return t

    @classmethod
    def update(cls, form):
        id = int(form.get('id', ''))
        w = cls.find(id)
        w.content = form.get('content')
        w.save()
        return w


class Comment(Model):
    @classmethod
    def new(cls, form, request):
        t = cls(form)
        t.user_id = current_user(request).id
        t.save()
        return t

    def __init__(self, form, user_id=-1):
        self.id = form.get('id', None)
        self.content = form.get('content', '')
        self.user_id = form.get('user_id', user_id)
        self.weibo_id = int(form.get('weibo_id', -1))

    def user(self):
        u = User.find_one(id=self.user_id)
        return u
