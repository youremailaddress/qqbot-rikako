import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot
import os
from utils.functions import baseDir
nonebot.init(_env_file='.env',set_on=True,root=baseDir()+"/")
nonebot.init(apscheduler_autostart=True)
nonebot.init(apscheduler_config={
    "apscheduler.timezone": "Asia/Shanghai"
})
from utils.funchandler import FunH
driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)
nonebot.load_plugin("my_bot.plugins.test")
nonebot.load_plugin("my_bot.plugins.timer")
# conf = driver.config

if __name__ == "__main__":
    print(FunH._add_perm("测试超管","*_3497511332",isblack=True))
    if not os.path.exists(os.path.split(os.path.realpath(__file__))[0]+"/tmp/"):
        os.makedirs(os.path.split(os.path.realpath(__file__))[0]+"/tmp/images/")
    nonebot.run(lifespan="on")