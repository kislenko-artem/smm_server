from sanic import Sanic

from smm import database
from smm import config
from smm.communicator import WebRouter
from smm.cmd import Cmd


if __name__ == "__main__":
    app = Sanic("smmhelp")
    cfg = config.init()
    WebRouter(app)
    cmd = Cmd()
    app.before_server_start(database.set_connection)
    app.before_server_stop(database.close_connection)
    app.before_server_stop(cmd.stop)
    cmd.init(app)
    app.run(cfg.app_host, cfg.app_port)