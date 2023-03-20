#comentario inutil
def hello_world(request):
    request_args = request.args
    if request_args and 'name' in request_args:
        name = request_args['name']
    else:
        name = 'World'
    return f'Hello {name}'