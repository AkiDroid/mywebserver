from utils import (
    template,
    http_response,
)


def index(request):
    body = template('todo_index.html')
    return http_response(body)


route_dict = {
    '/todo/index': index,
}
