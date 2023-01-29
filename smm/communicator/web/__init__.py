import sanic

from smm.communicator.web.v0 import (Profiles, Count, VKFeed, VKGroups, VKStatGroups, VKWall, Categories, Clients,
                                     SubCategories, Incomes, Offices)


class WebRouter(object):
    def __init__(self, app: sanic.Sanic):
        app.add_route(Profiles.as_view(), "/v0/profiles/<id>")
        app.add_route(Count.as_view(), "/v0/count/profiles/<id>")

        app.add_route(VKFeed.as_view(), "/v0/vk/profiles")
        app.add_route(VKGroups.as_view(), "/v0/vk/groups/<id>")
        app.add_route(VKStatGroups.as_view(), "/v0/vk/stat/groups/<id>")
        app.add_route(VKWall.as_view(), "/v0/vk/wall/<id>")

        app.add_route(SubCategories.as_view(), "/v0/business/subcategories/<id>")
        app.add_route(Categories.as_view(), "/v0/business/categories/<id>")
        app.add_route(Offices.as_view(), "/v0/business/offices/<id>")
        app.add_route(Clients.as_view(), "/v0/business/clients/<id>")
        app.add_route(Incomes.as_view(), "/v0/business/incomes/<id>")
