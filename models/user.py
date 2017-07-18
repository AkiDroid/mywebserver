from models import Model
import hashlib
from models.todo import Todo
import utils


class User(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    @classmethod
    def sha256(cls, ascii_str):
        return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()

    def salted_password(self, password, salt='$!@><?>HUI&DWQa`'):
        hash1 = self.sha256(password)
        hash2 = self.sha256(hash1 + salt)
        return hash2

    def validate_register(self):
        pwd = self.password
        self.password = self.salted_password(pwd)
        if User.find_one(username=self.username) is None:
            self.save()
            return self
        else:
            return None

    def validate_login(self):
        u = User.find_one(username=self.username)
        if u is not None:
            return u.password == self.salted_password(self.password)
        else:
            return False

    def todos(self):
        ts = []
        for t in Todo.all():
            if t.user_id == self.id:
                ts.append(t)
        return ts

    @classmethod
    def is_authenticated(cls, request):
        if utils.current_user(request) is None:
            return False
        else:
            return True
