# import nonebot
from nonebot import on_command, on_startswith, require, get_bot
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp.message import Message
import nonebot.adapters.cqhttp
import _thread

import urllib3
import json

scheduler = require("nonebot_plugin_apscheduler").scheduler

@scheduler.scheduled_job("cron", hour="9",minute="50")
async def tm():
    bot = get_bot()
    group_id=744129478
    try:
        try:
            url = 'http://api.soyiji.com/news_jpg'
            r = urllib3.PoolManager().request('GET', url)
            hjson = json.loads(r.data.decode())
            img_url = hjson["url"]
            img_url = "http://www.zmrwh.xyz:82/1.php?id="+img_url
            cq = "[CQ:image,file="+img_url+",id=40000]"
            msg=Message(cq)
            await bot.send_group_msg(group_id=group_id, message=msg)
        except:
            msg="呜呜，获取日报失败了，快来修理我吧"
            await bot.send_group_msg(group_id=group_id, message=msg)

    except :
        msg="我已经很努力的向报社催了，可能今天的日报卡路上了吧"
        await bot.send_group_msg(group_id=group_id, message=msg)


