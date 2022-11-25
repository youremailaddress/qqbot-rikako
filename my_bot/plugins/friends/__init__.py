from datetime import datetime
import nonebot
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from utils.rolehandler import is_add_friend
from nonebot.plugin import on_request
from utils.permissionhandler import PMH as perm
from .data_source import FRDBH as friends
from .data_source import FRIH
driver = nonebot.get_driver()
notice = on_request(rule=is_add_friend,priority=11)
@notice.handle()
@perm.register(name="添加好友",usage="当有好友请求时自动执行",intro="自动接受好友申请(每日有上限5个)")
async def addperson(bot: Bot, event: Event, state: T_State,matcher: Matcher):
    updatetime = datetime.now().strftime('%Y%m%d')
    user_id = event.get_user_id()
    if friends.checknum(updatetime):
        friends.push_person(user_id,updatetime)
        await bot.send_private_msg(user_id=bot.config.dict()["super"],message=f"成功添加好友{user_id}")
        await event.approve(bot)
        await bot.send_private_msg(user_id=user_id,message="hi~，我是rikako，终于等到你啦！现在我功能还不够完备，欢迎长期关注哦")
    else:
        await bot.send_private_msg(user_id=bot.config.dict()["super"],message=f"因为人数限制，未能成功添加好友{user_id}")

@driver.on_bot_connect
async def updateFriendsData(bot: Bot):
    FRIH.importdata()
    friends = await bot.get_friend_list()
    FRIH.handle_data_friends(friends)
    groups = await bot.get_group_list()
    gids = [i["group_id"] for i in groups]
    FRIH.handle_data_group(groups)
    dic = {}
    for gid in gids:
        dic[gid] = await bot.get_group_member_list(group_id=gid)
    FRIH.handle_data_frigro(dic)
    FRIH.exportdata()

