from jinja2 import Environment, FileSystemLoader
import os.path
import time
import json
import random
from routes.session import session
from models.user import User


def log(*args, **kwargs):
    formats = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(formats, value)
    with open('log.gua.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


path = '{}/templates/'.format(os.path.dirname(__file__))
loader = FileSystemLoader(path)
env = Environment(loader=loader)


def template(path, **kwargs):
    t = env.get_template(path)
    return t.render(**kwargs)


def response_headers(headers, status_code=200):
    header = 'HTTP/1.1 {} OK\r\n'.format(status_code)
    header += ''.join(['{}: {}\r\n'.format(k, v) for k, v in headers.items()])
    return header


def redirect(location):
    headers = {
        'Content-Type': 'text/html',
        'Location': location
    }
    header = response_headers(headers, 302)
    r = header + '\r\n' + ''
    return r.encode(encoding='utf-8')


def error(request, code=404):
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def http_response(body, headers=None):
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    if headers is not None:
        header += ''.join(['{}: {}\r\n'.format(k, v) for k, v in headers.items()])
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def json_response(data):
    header = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n'
    body = json.dumps(data, ensure_ascii=False, indent=2)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def current_user(request):
    session_id = request.cookies.get('user', '')
    print('session id', session_id)
    user_id = session.get(session_id, -1)
    print('user id', user_id)
    user = User.find(user_id)
    return user


def random_str():
    seed = 'abcdefjsad89234hdsfkljasdkjghigaksldf89weru'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


# 是否登录
def login_required(route_function):
    def func(request):
        user = current_user(request)
        print(user)
        if user is None:
            # 没登录重定向到 /login
            return redirect('/login')
        else:
            # 登录
            return route_function(request)
    return func
