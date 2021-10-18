from nonebot import get_driver
from nonebot.rule import Rule
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.adapters.cqhttp.event import MessageEvent, PokeNotifyEvent, PrivateMessageEvent
from nonebot.adapters.cqhttp import GroupRequestEvent,GroupMessageEvent,FriendRequestEvent
from .config import Config
import os.path
conf = get_driver().config

def acceptMessage():#在处理群里且是poke且poke rikako自己且该功能开启
    async def _check_group(bot: Bot, event: Event, state: T_State) -> bool:
        if isinstance(event,PokeNotifyEvent):
            for i in conf.group_list:
                if i == event.get_session_id().split("_")[1] and event.target_id==2707881642:
                    return True
        return False
    
    async def _check_open(bot: Bot, event: Event, state: T_State) -> bool:
        if not await _check_group(bot, event, state):
            return False
        groupid = event.get_session_id().split("_")[1]
        try:
            pluginname=os.path.realpath(__file__).split("\\")[-2]
        except:
            pluginname=os.path.realpath(__file__).split("/")[-2]
        lis = []
        for k,v in conf.disabled_settings.items():
            for m in v:
                lis.append((k,m))
        if (pluginname,groupid) in lis:
            return False
        else:
            return True
    # async def _check_poke(bot: Bot, event: Event, state: T_State) -> bool:
    #     print(await _check_open(bot, event, state))
    #     if isinstance(event,PokeNotifyEvent) and await _check_open(bot, event, state):
    #         print(event.target_id)
    #         return True
    #     else:
    #         return False

    return Rule(_check_open)
