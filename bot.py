import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot
import os
nonebot.init(_env_file='.env',set_on=True,root=os.path.split(os.path.realpath(__file__))[0]+"/")
nonebot.init(apscheduler_autostart=True)
nonebot.init(apscheduler_config={
    "apscheduler.timezone": "Asia/Shanghai"
})
driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)
nonebot.load_builtin_plugins()
nonebot.load_plugins("my_bot/plugins")
# conf = driver.config

if __name__ == "__main__":
    if not os.path.exists(os.path.split(os.path.realpath(__file__))[0]+"/tmp/"):
        os.makedirs(os.path.split(os.path.realpath(__file__))[0]+"/tmp/images/")
    nonebot.run(lifespan="on")