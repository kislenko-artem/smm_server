from smm.database.abstract import group


class Groups(group.Groups):

    async def groups_list(self) -> list:
        data = await self.select(
            "SELECT id, name, ident, screen_name, photo_50 FROM vk_groups",
            ["id", "name", "ident", "screen_name", "photo_50"])
        return data

    async def group_create(self,
                           name: str,
                           ident: int,
                           screen_name: str,
                           photo_50: str):
        await self.execute(
            '''INSERT INTO vk_groups (name, ident, screen_name, photo_50) 
                                     VALUES ($1, $2, $3, $4)''',
            (name, ident, screen_name, photo_50))

    async def group_delete(self, id: int):
        await self.execute(
            "DELETE FROM vk_groups WHERE id = $1 OR ident = $1", (id,))
