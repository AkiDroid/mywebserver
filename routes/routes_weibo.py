from models.user import User
from models.weibo import Weibo
from models.weibo import Comment
from routes.session import session
from utils import (
    template,
    response_headers,
    redirect,
    http_response,
    current_user,
    login_required
)


@login_required
def index(request):
    user_id = request.query.get('user_id', -1)
    user_id = int(user_id)
    user = User.find(user_id)
    weibos = Weibo.find_all(user_id=user_id)
    body = template('weibo_index.html', weibos=weibos, user=user)
    return http_response(body)

route_dict = {
    '/weibo/index': index,
}
