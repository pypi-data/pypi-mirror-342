from webob import Request

class Middleware:
    def __init__(self, app):
        self.app = app

    def add_middleware(self, middleware):
        self.app = middleware(self.app)

    def process_request(self, request):
        pass

    def process_response(self, request, response):
        pass

    def request_handle(self, request):
        self.process_request(request)
        response = self.app.request_handle(request)
        self.process_response(request, response)
        return response

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.app.request_handle(request)
        return response(environ, start_response)
