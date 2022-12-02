import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot
import os
from utils.functions import baseDir
from utils.core.tools.jsonconf import Jsonify
nonebot.init(_env_file='.env',set_on=True,root=baseDir()+"/")
nonebot.init(apscheduler_autostart=True)
nonebot.init(apscheduler_config={
    "apscheduler.timezone": "Asia/Shanghai"
})
from my_bot.handlers.interacthandler import BH
driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)
nonebot.load_plugin("my_bot.plugins.test")
nonebot.load_plugin("my_bot.plugins.timer")
# conf = driver.config

if __name__ == "__main__":
    if not os.path.exists(os.path.split(os.path.realpath(__file__))[0]+"/tmp/"):
        os.makedirs(os.path.split(os.path.realpath(__file__))[0]+"/tmp/images/")
    nonebot.run(lifespan="on")