import inspect
from webob import Request #, Response
from parse import parse
import requests
import wsgiadapter
from jinja2 import Environment, FileSystemLoader
from whitenoise import WhiteNoise
import os
from .middleware import Middleware
from .response import CustomResponse as Response


class YoloApp:
    def __init__(self, template_dir='templates', static_dir='static'):
        self.routes = dict()
        self.exception_handler = None
        
        self.template_env = Environment(
            loader=FileSystemLoader(os.path.abspath(template_dir)),
        )
        self.whitenoise_app = WhiteNoise(self.wsgi_app, root=static_dir, prefix='/static/')
        self.middleware = Middleware(self)
        

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        if path.startswith('/static/'):
            return self.whitenoise_app(environ, start_response)
        return self.middleware(environ, start_response)
    
    def wsgi_app(self, environ, start_response):
        """ WSGI application callable."""
        request = Request(environ)
        response = self.request_handle(request)
        return response(environ, start_response)


    def request_handle(self, request):
        """ Handle the request and return a response."""
        response = Response()
        handler_data, kwargs = self.find_handler(request)
       
        if handler_data is not None:
            handler = handler_data.get('handler', None)
            allowed_methods = handler_data.get('allowed_methods', [])

            if inspect.isclass(handler):
                handler = getattr(handler(), request.method.lower(), None)
                if handler is None:
                    return self.method_not_allowed(response)
            else:
                if request.method not in allowed_methods:
                    return self.method_not_allowed(response)
            try:
                handler(request, response, **kwargs)
            except Exception as e:
                if self.exception_handler is not None:
                    self.exception_handler(request, response, e)
                else:
                    raise e
        else:
            self.not_found(request, response)
        return response
    
    def method_not_allowed(self, response):
        """ Handle 405 Method Not Allowed errors."""
        response.status = '405'
        response.text = 'Method Not Allowed'
        return response
    
    def find_handler(self, request):
        """ Find the handler for the given request."""
        for path, handler_data in self.routes.items():
            parsed_result = parse(path, request.path)
            if parsed_result is not None:
                return handler_data, parsed_result.named
        return None, {}

    def not_found(self, request, response):
        """ Handle 404 Not Found errors."""
        response.status = '404 Not Found'
        response.text = '404 Not Found'
        return response    
    
    def add_rote(self, path, handler, allowed_methods=None):
        assert path not in self.routes, f"Path '{path}' is already registered."
        
        if allowed_methods is None:
            allowed_methods = ['GET']

        if not isinstance(allowed_methods, list):
            raise TypeError("allowed_methods must be a list")    

        self.routes[path] = {'handler': handler, 'allowed_methods': allowed_methods}

    def route(self, path, allowed_methods=None):
        """ Decorator to register a route with the application."""
        def wrapper(handler):
            """ Register the handler for the given path."""
            self.add_rote(path, handler, allowed_methods)
            return handler
        return wrapper

    def test_session(self):
        session = requests.Session()
        session.mount('http://testserver', wsgiadapter.WSGIAdapter(self))
        return session
    
    def template(self, template_name: str, context: dict=None):
        if context is None:
            context = {}
        return self.template_env.get_template(template_name).render(**context)
    
    def add_exception_handler(self, handler):
        """ Register an exception handler."""
        self.exception_handler = handler

    def add_middleware(self, middleware):
        self.middleware.add_middleware(middleware)
