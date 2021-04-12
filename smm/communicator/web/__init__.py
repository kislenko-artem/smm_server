import sanic

from smm.communicator.web.v0 import Profiles, VKFeed, VKGroups, VKStatGroups, Count


class WebRouter(object):
    def __init__(self, app: sanic.Sanic):
        app.add_route(Profiles.as_view(), "/v0/profiles/<id>")
        app.add_route(VKFeed.as_view(), "/v0/vk/profiles")
        app.add_route(VKGroups.as_view(), "/v0/vk/groups/<id>")
        app.add_route(VKStatGroups.as_view(), "/v0/vk/stat/groups/<id>")
        app.add_route(Count.as_view(), "/v0/count/profiles/<id>")
