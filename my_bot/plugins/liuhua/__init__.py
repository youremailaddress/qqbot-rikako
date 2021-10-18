# import nonebot
from nonebot import get_driver

from .config import Config

global_config = get_driver().config
import httpx
# import asyncio

from .utils import acceptMessage
from nonebot.plugin import on_notice
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.typing import T_State

notice = on_notice(rule=acceptMessage(),priority=11)
@notice.handle()
async def yy(bot: Bot, event: Event,state: T_State):
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.get('https://v1.hitokoto.cn/?encode=text&charset=utf-8')
    await notice.finish(resp.text)