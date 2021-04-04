import time

from smm.database.abstract import profile


class Profiles(profile.Profiles):

    async def profile_list(self) -> list:
        data = await self.select(
            "SELECT id, name, profile_type, ident FROM profiles",
            ["id", "name", "profile_type", "ident"])
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
