import asyncio
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


stat_cache = {}


class VKStatGroups(HTTPMethodView):

    async def get(self, request, id: str):
        if stat_cache.get(id) is None:
            return json([], HTTPStatus.OK)
        if request.args.get("age"):
            data = []
            classifacator = {}
            for d in stat_cache.get(id):
                groupKey = d.get('bdate')
                if groupKey is not None and len(d.get('bdate').split(".")) == 3:
                    groupKey = d.get('bdate').split(".")[2]
                if groupKey not in classifacator:
                    classifacator[groupKey] = 1
                    continue
                classifacator[groupKey] += 1
            for key in classifacator:
                data.append({"name": key, "value": classifacator[key]})

            data.sort(key=lambda x: x["value"], reverse=True)
            return json(data, HTTPStatus.OK)
        if request.args.get("geography"):
            data = []
            classifacator = {}
            for d in stat_cache.get(id):
                groupKey = d.get('city')
                if groupKey is not None:
                    groupKey = d.get('city').get('title')
                if groupKey not in classifacator:
                    classifacator[groupKey] = 1
                    continue
                classifacator[groupKey] += 1
            for key in classifacator:
                data.append({"name": key, "value": classifacator[key]})

            data.sort(key=lambda x: x["value"], reverse=True)
            return json(data, HTTPStatus.OK)
        return json(stat_cache.get(id), HTTPStatus.OK)

    async def waiter(self, id: str):
        data = await vk_methods.VKMethods(cfg.vk_token).group_members(id)
        stat_cache[id] = data

    async def post(self, request, id: str):
        asyncio.create_task(self.waiter(id))
        return json({"success": True}, HTTPStatus.OK)


class VKWall(HTTPMethodView):

    async def get(self, request, id: str):
        data = await vk_methods.VKMethods(cfg.vk_token).group_wall(id)
        return json(data, HTTPStatus.OK)
