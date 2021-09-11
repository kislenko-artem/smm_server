from typing import NewType, List
from dataclasses import dataclass
from datetime import datetime

from smm.database import get_connection

ProfileType = NewType("ProfileType", int)

InstagramGroup: ProfileType = ProfileType(1)
VKGroup: ProfileType = ProfileType(2)


@dataclass(frozen=True)
class Count:
    count: int
    date: datetime


class Profile(object):
    id: int
    name: str
    profile_type: ProfileType
    ident: str

    def __init__(self,
                 id: int = None,
                 name: str = None,
                 profile_type: ProfileType = None,
                 ident: str = None):
        self.id = id
        self.name = name
        self.profile_type = profile_type
        self.ident = ident

    async def list(self) -> List["Profile"]:
        p_list: List["Profile"] = []

        DB = await get_connection()
        profiles = await DB.profile_list()

        for d in profiles:
            p_list.append(Profile(
                id=d.get("id"),
                name=d.get("name"),
                profile_type=d.get("profile_type"),
                ident=d.get("ident"),
            ))
        return p_list

    async def counts(self, profile_id: int) -> List[Count]:
        p_list: List[Count] = []

        DB = await get_connection()
        data = await DB.profile_count(profile_id)

        for d in data:
            p_list.append(Count(
                count=d.get("count"),
                date=d.get("dt_create"),
            ))
        return p_list

    async def create(self):
        DB = await get_connection()

        await DB.profile_create(self.name, self.profile_type, self.ident)

    async def update(self):
        DB = await get_connection()
        await DB.profile_update(self.name,
                                self.profile_type,
                                self.ident,
                                self.id)

    async def delete(self):
        DB = await get_connection()
        await DB.profile_delete(self.id)

    async def set_count(self, count: int):
        DB = await get_connection()
        await DB.profile_set_count(count, self.id)
