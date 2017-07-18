import json

from utils import (
    current_user,
    json_response,
)
from models.todo import Todo
from models.weibo import Weibo
from models.weibo import Comment


def todo_all(request):
    todos = Todo.all_json()
    return json_response(todos)


def todo_add(request):
    form = request.json()
    t = Todo.new(form)
    return json_response(t.json())


def todo_delete(request):
    """
    /delete?id=1
    """
    todo_id = int(request.query.get('id'))
    t = Todo.delete(todo_id)
    return json_response(t.json())


def todo_update(request):
    form = request.json()
    todo_id = int(form.get('id'))
    t = Todo.update(todo_id, form)
    return json_response(t.json())


def weibo_delete(request):
    id = int(request.query.get('id'))
    w = Weibo.delete(id)
    return json_response('{}')


def comment_add(request):
    form = request.json()
    c = Comment.new(form, request)
    c.username = current_user(request).username
    return json_response(c.json())


def weibo_add(request):
    form = request.json()
    w = Weibo.new(form, request)
    w.username = current_user(request).username
    return json_response(w.json())


def weibo_update(request):
    form = request.json()
    print('weibo update', form)
    w = Weibo.update(form)
    w.username = current_user(request).username
    print('w.json()', w.json())
    return json_response(w.json())


def comment_delete(request):
    comment_id = int(request.query.get('id'))
    print('delet comment id ', comment_id)
    c = Comment.delete(comment_id)
    return json_response(c.json())


route_dict = {
    '/api/todo/all': todo_all,
    '/api/todo/add': todo_add,
    '/api/todo/delete': todo_delete,
    '/api/todo/update': todo_update,
    '/api/weibo/add': weibo_add,
    '/api/weibo/delete': weibo_delete,
    '/api/comment/add': comment_add,
    '/api/weibo/update': weibo_update,
    '/api/comment/delete': comment_delete,
}
