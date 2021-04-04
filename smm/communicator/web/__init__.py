import sanic

from smm.communicator.web.v0 import Profiles, VKFeed


class WebRouter(object):
    def __init__(self, app: sanic.Sanic):
        app.add_route(Profiles.as_view(), "/v0/profiles/<id>")
        app.add_route(VKFeed.as_view(), "/v0/vk/profiles")
