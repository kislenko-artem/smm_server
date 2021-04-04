from http import HTTPStatus

from sanic.response import json
from sanic.views import HTTPMethodView

from smm import config
from smm.service import vk_methods


class VKFeed(HTTPMethodView):

    async def get(self, request):
        cfg = config.init()
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
