from smm.database.abstract import Methods


class Groups(Methods):

    @staticmethod
    async def groups_list() -> list:
        raise NotImplemented("")

    @staticmethod
    async def groups_create(name: str,
                             profile_type: int,
                             ident: str):
        raise NotImplemented("")

    @staticmethod
    async def groups_update(name: str,
                             profile_type: int,
                             ident: str,
                             id: int):
        raise NotImplemented("")

    @staticmethod
    async def groups_delete(id: int):
        raise NotImplemented("")
