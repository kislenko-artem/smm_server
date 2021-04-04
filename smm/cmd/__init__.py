import sanic

from smm.cmd.instagram import watch_profile_followers

__all__ = ["Cmd"]


class Cmd(object):
    __slots__ = ["is_run"]

    def __init__(self):
        self.is_run = True

    def init(self, app: sanic.Sanic):
        app.add_task(lambda : watch_profile_followers(self))

    def stop(self, *args, **kwargs):
        self.is_run = False
