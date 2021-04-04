import asyncio
from typing import Dict, List

import aiohttp


class VKMethods(object):
    __slots__ = ("token", )

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
                              max_result: int = 200) -> List[str]:
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
            for d in data["response"]["items"]:
                if d.get("type") == "profile":
                    continue
                group_data = d.get("group")
                r_data.append("https://vk.com/{}".format(
                    group_data.get("screen_name")))
            if data["response"]["count"] < limit:
                break
            await asyncio.sleep(1)
            offset += limit

            if len(r_data) > max_result:
                break

        return r_data
