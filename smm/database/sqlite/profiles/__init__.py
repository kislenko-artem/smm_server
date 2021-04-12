import time
from datetime import datetime

from smm.database.abstract import profile


class Profiles(profile.Profiles):

    async def profile_list(self) -> list:
        data = await self.select(
            "SELECT id, name, profile_type, ident FROM profiles",
            ["id", "name", "profile_type", "ident"])
        return data

    async def profile_count(self, profile_id: int) -> list:
        r_data = []
        data = await self.select(
            "SELECT dt_create, count FROM profile_count WHERE profile_id = $1 ORDER BY dt_create",
            ["dt_create", "count"], (profile_id,))
        for d in r_data:
            r_data.append({"dt_create": datetime.utcfromtimestamp(d["dt_create"]),
                           "count": d["count"]})
        return data

    async def profile_create(self,
                             name: str,
                             profile_type: int,
                             ident: str):
        await self.execute(
            "INSERT INTO profiles (name, profile_type, ident) VALUES ($1, $2, $3)",
            (name, profile_type, ident))

    async def profile_update(self,
                             name: str,
                             profile_type: int,
                             ident: str,
                             id: int):
        await self.execute(
            "UPDATE profiles SET name=$1, profile_type=$2, ident=$3 WHERE id = $4",
            (name, profile_type, ident, id,))

    async def profile_delete(self, id: int):
        await self.execute(
            "DELETE FROM profiles WHERE id = $1", (id,))

    async def profile_set_count(self, count: int, id: int):
        await self.execute(
            '''INSERT INTO profile_count (profile_id, count, dt_create) 
            VALUES ($1, $2, $3)''',
            (id, count, time.time()))
