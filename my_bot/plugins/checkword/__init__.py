from nonebot.adapters.cqhttp import Bot, Event
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.plugin import on_startswith
from .data_source import CWDBH

checkword_handle = on_startswith('校验码',priority=50)
@checkword_handle.handle()
async def checkword(bot: Bot, event: Event, state: T_State,matcher: Matcher):
    msg = str(event.message).strip()
    msg = msg.split(" ")
    if len(msg) != 2 or len(msg[1])<5 or len(msg[1])>8 or not msg[1].isalnum():
        await checkword_handle.finish()
    else:
        CWDBH.push_checkword(event.get_user_id(),msg[1])
        await checkword_handle.finish()