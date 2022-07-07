from nonebot import get_driver
driver = get_driver()
global_config = get_driver().config
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.adapters.cqhttp.event import PokeNotifyEvent,FriendRequestEvent

def is_on(bot:Bot,event:Event,_):
    '''
    bot开机
    '''
    return global_config.set_on

def is_poke(bot:Bot,event:Event,_):
    '''
    bot 被 戳一戳
    '''
    if isinstance(event,PokeNotifyEvent):
        if event.target_id==bot.config.dict()['self']:
            return True
    return False

def is_add_friend(bot:Bot,event:Event,_):
    return isinstance(event,FriendRequestEvent)