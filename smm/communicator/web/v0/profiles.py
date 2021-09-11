from http import HTTPStatus

from sanic.exceptions import InvalidUsage
from sanic.response import json
from sanic.views import HTTPMethodView

from smm.service import profiles


class Profiles(HTTPMethodView):

    async def get(self, request, id):
        if id != "":
            raise InvalidUsage("wrong router",
                               status_code=HTTPStatus.BAD_REQUEST)
        g = await profiles.Profile().list()
        profile_list = []
        for d in g:
            profile_list.append(d.__dict__)
        data = {
            "results": profile_list
        }
        return json(data, HTTPStatus.OK)

    async def post(self, request, id):
        if id != "":
            raise InvalidUsage("wrong router",
                               status_code=HTTPStatus.BAD_REQUEST)

        await profiles.Profile(name=request.json.get("name"),
                               ident=request.json.get("ident"),
                               profile_type=request.json.get("profile_type"),
                               ).create()
        return json({"success": True}, HTTPStatus.OK)

    async def put(self, request, id):
        if id == "":
            raise InvalidUsage("wrong paramter",
                               status_code=HTTPStatus.BAD_REQUEST)

        await profiles.Profile(name=request.json.get("name"),
                               ident=request.json.get("ident"),
                               profile_type=request.json.get("profile_type"),
                               id=int(id)).update()
        return json({"success": True}, HTTPStatus.OK)

    async def delete(self, request, id):
        if id == "":
            raise InvalidUsage("wrong paramter",
                               status_code=HTTPStatus.BAD_REQUEST)

        await profiles.Profile(id=int(id)).delete()
        return json({"success": True}, HTTPStatus.OK)


class Count(HTTPMethodView):
    async def get(self, request, id: str):
        g = await profiles.Profile().counts(int(id))
        counts = []
        for d in g:
            counts.append(d.__dict__)
        data = {
            "results": counts
        }
        return json(data, HTTPStatus.OK)
