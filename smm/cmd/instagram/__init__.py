import asyncio
from typing import TYPE_CHECKING
import aiohttp

from smm import config
from smm.service.profiles import Profiles, InstagramGroup

if TYPE_CHECKING:
    from smm.cmd import Cmd

HOUR = 3600


async def watch_profile_followers(cmd: "Cmd"):
    cfg = config.init()
    while cmd.is_run:
        profiles = await Profiles().list()
        for p in profiles:
            if p.profile_type != InstagramGroup:
                continue
            async with aiohttp.ClientSession(headers={
                "Cookie": cfg.insta_cookie,
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0"
            }) as session:
                url = "https://www.instagram.com/{}/?__a=1".format(p.name)
                r = await session.get(url)
                data = await r.json()
                count = data["graphql"]["user"]["edge_followed_by"]["count"]
                await p.set_count(count)
        await asyncio.sleep(HOUR)
