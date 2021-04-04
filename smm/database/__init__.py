from typing import Optional

from smm.database.sqlite import Methods


class DB(Methods):
    pass


_con: Optional[DB] = None


async def set_connection(*args, **kwargs):
    global _con
    _con = DB()
    await _con.init(*args, **kwargs)


async def close_connection(*args, **kwargs):
    global _con

    if _con is None:
        return

    await _con.close()


async def get_connection() -> DB:
    global _con

    if _con is None:
        raise Exception("не установлено соединение")

    return _con
