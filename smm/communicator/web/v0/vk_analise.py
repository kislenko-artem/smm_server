from http import HTTPStatus

from sanic.exceptions import InvalidUsage
from sanic.response import json
from sanic.views import HTTPMethodView

from smm import config
from smm.service import vk_methods

cfg = config.init()


class VKFeed(HTTPMethodView):

    async def get(self, request):
        max_result: int = 200
        q = request.args.get("q")
        if request.args.get("max_count"):
            max_result = request.args.get("max_count")
        list_link = await vk_methods.VKMethods(
            cfg.vk_token).get_groups_list(q, max_result=max_result)
        data = {
            "results": list_link
        }
        return json(data, HTTPStatus.OK)


class VKGroups(HTTPMethodView):

    async def get(self, request, id):
        if id != "":
            raise InvalidUsage("wrong router",
                               status_code=HTTPStatus.BAD_REQUEST)
        data = await vk_methods.VKMethods(cfg.vk_token).list_group()
        return json(data, HTTPStatus.OK)

    async def post(self, request, id):
        if id != "":
            raise InvalidUsage("wrong router",
                               status_code=HTTPStatus.BAD_REQUEST)
        await vk_methods.VKMethods(
            cfg.vk_token).add_group(request.json.get("ident"))
        data = {
            "success": True
        }
        return json(data, HTTPStatus.OK)

    async def delete(self, request, id):
        await vk_methods.VKMethods(cfg.vk_token).delete_group(id)
        data = {
            "success": True
        }
        return json(data, HTTPStatus.OK)
