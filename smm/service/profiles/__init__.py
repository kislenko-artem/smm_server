from typing import NewType, List

from smm.database import get_connection

ProfileType = NewType("ProfileType", int)

InstagramGroup: ProfileType(1)
VKGroup: ProfileType(2)


class Profiles(object):
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

    async def list(self) -> List["Profiles"]:
        p_list: List["Profiles"] = []

        DB = await get_connection()
        profiles = await DB.profile_list()

        for d in profiles:
            p_list.append(Profiles(
                id=d.get("id"),
                name=d.get("name"),
                profile_type=d.get("profile_type"),
                ident=d.get("ident"),
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
