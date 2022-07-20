from nonebot import require, get_bot
from .dailynews import news
import datetime

sche = require("nonebot_plugin_apscheduler").scheduler
@sche.scheduled_job("cron", hour="*",minute="*")
async def sche_():
    bot = get_bot()
    group_id=[744129478]
    if datetime.datetime.now().hour == 0 and datetime.datetime.now().minute == 20:
        for gi in group_id:
            news(bot,gi)


