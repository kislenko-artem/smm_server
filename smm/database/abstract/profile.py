from smm.database.abstract import Methods


class Profiles(Methods):

    @staticmethod
    async def profile_list() -> list:
        raise NotImplemented("")

    @staticmethod
    async def profile_create(name: str,
                     profile_type: int,
                     ident: str):
        raise NotImplemented("")

    @staticmethod
    async def profile_update(name: str,
                     profile_type: int,
                     ident: str,
                     id: int):
        raise NotImplemented("")

    @staticmethod
    async def profile_delete(id: int):
        raise NotImplemented("")

    @staticmethod
    async def profile_set_count(count: int, id: int):
        raise NotImplemented("")
