from nonebot import require, get_bot
from .dailynews import news
from .bililive import handleblive
import datetime

sche = require("nonebot_plugin_apscheduler").scheduler
@sche.scheduled_job("cron", hour="*",minute="*")
async def sche_():
    bot = get_bot()
    group_id=[744129478]
    if datetime.datetime.now().hour == 9 and datetime.datetime.now().minute == 50:
        for gi in group_id:
            await news(bot,gi)
        await handleblive(bot)


