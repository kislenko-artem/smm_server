from sanic.response import empty
from sanic.views import HTTPMethodView


class Base(HTTPMethodView):

    def options(self, request, id):
        return empty()
