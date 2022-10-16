from nonebot import require, get_bot
from ..dailynews.dailynews import dailynews
from ..reminder.remind import reminder

from nonebot.adapters.cqhttp import Bot, Event
from nonebot.matcher import Matcher
from nonebot.typing import T_State
from nonebot import on_command
from utils.timerhandler import TMH as tmr
from utils.permissionhandler import PMH as perm
import time

viewtimer = on_command("查询定时",priority=35)
@viewtimer.handle()
@perm.checker(name="查询定时",usage="查询定时",intro="查询每个人注册的定时任务，只返回其本人的,[superuser] 可以通过 查询定时 QQ号 查询")
async def viewtime(bot: Bot, event: Event, state: T_State,matcher: Matcher):
    msg = str(event.message).strip()
    usid = event.get_user_id()
    if msg != "":
        if usid not in bot.config.superusers:
            await viewtimer.finish("非超级用户无法使用QQ号查询！")
        else:
            assert msg.isdigit()
            await viewtimer.finish(tmr.viewUsage(msg))
    else:
        await viewtimer.finish(tmr.viewUsage(usid))

removetimer = on_command("删除定时",priority=35)
@removetimer.handle()
@perm.checker(name="删除定时",usage="删除定时 <一个或者多个定时id>",intro="删除自己不需要的定时任务，定时id可以从查询定时命令得到")
async def removetime(bot: Bot, event: Event, state: T_State,matcher: Matcher):
    msg = str(event.message).strip()
    usid = event.get_user_id()
    print(msg.split(" "))
    idlis = [i.isdigit() for i in msg.split(" ")]
    assert False not in idlis
    try:
        for ids in msg.split(" "):
            assert tmr.RemoveUsage(usid,ids)
    except:
        await removetimer.finish("部分id不存在或不属于你，无法删除，请检查后重试")
    await removetimer.finish(f"id为{msg.split(' ')}的定时任务已经被删除")

sche = require("nonebot_plugin_apscheduler").scheduler
@sche.scheduled_job("cron", hour="*",minute="*")
async def sche_():
    bot = get_bot()
    await dailynews(bot)
    await reminder(bot)