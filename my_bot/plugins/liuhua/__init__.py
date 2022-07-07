# import nonebot
from nonebot import get_driver
from utils.rolehandler import is_poke

global_config = get_driver().config
import httpx

from nonebot.plugin import on_notice
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.typing import T_State
from utils.permissionhandler import PermissionHandler

notice = on_notice(rule=is_poke,priority=11)
notice_perm =  PermissionHandler("hitokoto","poke the bot","随机回复一个句子")
@notice.handle()
async def yy(bot: Bot, event: Event,state: T_State):
    if not notice_perm.async_checker(bot,event):
        return
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.get('https://v1.hitokoto.cn/?encode=text&charset=utf-8')
    await notice.finish(resp.text)