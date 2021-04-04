import asyncio
from typing import TYPE_CHECKING
import aiohttp

from smm.service.profiles import Profiles

if TYPE_CHECKING:
    from smm.cmd import Cmd

HOUR = 3600


async def watch_profile_followers(cmd: "Cmd"):
    while cmd.is_run:
        await asyncio.sleep(HOUR)
        profiles = await Profiles().list()
        for p in profiles:
            async with aiohttp.ClientSession() as session:
                r = await session.get(
                    "https://www.instagram.com/{}/?__a=1".format(p.name))
                data = await r.json()
                count = data["graphql"]["user"]["edge_followed_by"]["count"]
                await p.set_count(count)
