from utils.rolehandler import is_poke
import httpx
from nonebot.plugin import on_notice
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from my_bot.handlers.interacthandler import BH

notice = on_notice(rule=is_poke,priority=11)
@notice.handle()
@BH.checker(name="一言",usage="戳一戳bot",intro="随机回复一个句子")
async def yy(bot: Bot, event: Event,state: T_State,matcher: Matcher):
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.get('https://v1.hitokoto.cn/?encode=text&charset=utf-8')
    await notice.finish(resp.text)