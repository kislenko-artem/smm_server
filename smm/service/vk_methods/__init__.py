import asyncio
from typing import Dict

import aiohttp
from sanic.log import logger

from smm.database import get_connection


class VKMethods(object):
    __slots__ = ("token",)

    def __init__(self, token: str):
        self.token = token

    def get_url(self, method: str) -> str:
        return f'https://api.vk.com/method/{method}?access_token={self.token}&v=5.130'

    async def send_request(self,
                           method: str,
                           params: Dict[
                               str, str]) -> dict:
        url = self.get_url(method)
        for key in params:
            url = f'{url}&{key}={params[key]}'
        async with aiohttp.ClientSession() as session:
            r = await session.get(url)
            data = await r.json()
        return data

    async def get_groups_list(self,
                              query: str,
                              max_result: int = 200) -> list:
        offset = 0
        limit = 200
        r_data = []
        while True:
            data = await self.send_request("search.getHints", {
                "q": query,
                "filters": "publics,groups",
                "search_global": "1",
                "limit": str(limit),
                "offset": str(offset)
            })
            print(data)
            if len(data["response"]["items"]) == 0:
                break
            for d in data["response"]["items"]:
                if d.get("type") == "profile":
                    continue
                r_data.append(d.get("group"))
            if data["response"]["count"] < limit:
                break
            await asyncio.sleep(1)
            offset += limit

            if len(r_data) > max_result:
                break

        return r_data

    async def add_group(self, group_id: str):

        data = await self.send_request("groups.getById", {
            "group_id": group_id,
        })
        if len(data.get("response")) == 0:
            return
        DB = await get_connection()
        r = data.get("response")[0]
        await DB.group_create(name=r.get("name"),
                              ident=r.get("id"),
                              screen_name=r.get("screen_name"),
                              photo_50=r.get("photo_50"),
                              )

    async def list_group(self) -> list:

        DB = await get_connection()
        data = await DB.groups_list()
        return data

    async def delete_group(self, group_id: str):

        DB = await get_connection()
        await DB.group_delete(int(group_id))

    async def group_members(self, group_id: str) -> list:
        offset = 0
        limit = 1000
        r_data = []
        while True:
            data = await self.send_request("groups.getMembers", {
                "group_id": group_id,
                "fields":
                    "sex,bdate,city,country,photo_max_orig,domain,has_mobile",
                "count": str(limit),
                "offset": str(offset)
            })
            if len(data["response"]["items"]) == 0:
                break
            for d in data["response"]["items"]:
                r_data.append(d)
            logger.info(
                f"group_members: group_id {group_id} len {len(r_data)}, limit {limit}, total {data['response']['count']}")
            if data["response"]["count"] < limit:
                break
            await asyncio.sleep(1)
            offset += limit
        return r_data

    async def group_wall(self, group_id: str) -> list:
        offset = 0
        limit = 100
        r_data = []
        while True:
            data = await self.send_request("wall.get", {
                "domain": group_id,
                "fields":
                    "post_type,date,from_id,owner_id,id,text,attachments,comments,likes,reposts,views",
                "count": str(limit),
                "offset": str(offset)
            })
            if "response" not in data:
                print("error data", data)
                break
            if len(data["response"]["items"]) == 0:
                break
            for d in data["response"]["items"]:
                r_data.append(d)
            logger.info(
                f"group_wall: group_id {group_id} len {len(r_data)}, limit {limit}, total {data['response']['count']}")
            if data["response"]["count"] < limit:
                break
            await asyncio.sleep(1)
            offset += limit
        return r_data
