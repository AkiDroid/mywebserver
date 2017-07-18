def route_static(request):
    """
    静态资源路由
    """
    filename = request.query.get('file', )
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\n\r\n'
        img = header + f.read()
        return img



