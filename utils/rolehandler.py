from nonebot import get_driver
driver = get_driver()
global_config = get_driver().config
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.adapters.cqhttp.event import PokeNotifyEvent,FriendRequestEvent
from nonebot.rule import Rule

async def is_on(bot:Bot,event:Event,_):
    '''
    bot开机
    '''
    return global_config.set_on

async def _is_poke(bot:Bot,event:Event,_):
    '''
    bot 被 戳一戳
    '''
    if isinstance(event,PokeNotifyEvent):
        if event.target_id==bot.config.dict()['self']:
            return True
    return False

async def is_poke(bot:Bot,event:Event,_):
    return Rule(is_on,_is_poke)

async def _is_add_friend(bot:Bot,event:Event,_):
    return isinstance(event,FriendRequestEvent)

async def is_add_friend(bot:Bot,event:Event,_):
    return Rule(is_on,_is_add_friend)