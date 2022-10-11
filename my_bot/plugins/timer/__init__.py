from nonebot import require, get_bot
from ..dailynews.dailynews import dailynews

sche = require("nonebot_plugin_apscheduler").scheduler
@sche.scheduled_job("cron", hour="*",minute="*")
async def sche_():
    bot = get_bot()
    await dailynews(bot)