from utils import (
    current_user,
    random_str,
    log,
    response_headers,
    template,
    http_response,
    login_required
)
from models.user import User
from routes.session import session


def route_index(request):
    if User.is_authenticated(request):
        user = current_user(request)
        username = user.username
        user_id = user.id
    else:
        username = 'Stranger'
        user_id = 'None'
    body = template('index.html', username=username, user_id=user_id)
    return http_response(body)


def route_login(request):
    headers = {}
    username = ''
    if request.method == 'POST':
        form = request.form()
        user = User(form)
        if user.validate_login():
            username = user.username
            user = User.find_one(username=username)
            session_id = random_str()
            session[session_id] = user.id
            print('session', session)
            headers['Set-Cookie'] = 'user={}'.format(session_id)
            result = '登录成功'
        else:
            result = '用户名或者密码错误'
    else:
        result = ''
    body = template('login.html', result=result, username=username)
    return http_response(body, headers=headers)


def route_register(request):
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_register():
            u.save()
            result = '注册成功'
        else:
            result = '用户名或者密码长度必须大于2'
    else:
        result = ''
    body = template('register.html', result=result)
    return http_response(body)


def route_profile(request):
    session_id = request.cookies.get('user', '')
    user_id = session.get(session_id, -1)
    user = ''
    if user_id != -1:
        user = User.find_one(id=int(user_id))
    body = template('profile.html', user=str(user))
    return http_response(body)


route_dict = {
    '/': route_index,
    '/login': route_login,
    '/register': route_register,
    '/profile': route_profile,
}
