import time
from models import Model


class Todo(Model):
    @classmethod
    def new(cls, form):
        t = cls(form)
        t.save()
        return t

    @classmethod
    def update(cls, id, form):
        t = cls.find(id)
        t.title = form.get('title')
        t.save()
        return t

    @classmethod
    def complete(cls, id, completed=True):
        t = cls.find(id)
        t.completed = completed
        t.save()
        return t

    def __init__(self, form):
        self.id = None
        self.title = form.get('title', '')
        self.completed = False
        # created_time  updated_time
        self.ct = int(time.time())
        self.ut = self.ct
