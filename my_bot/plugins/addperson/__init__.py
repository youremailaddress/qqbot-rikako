from nonebot import get_driver
from utils.permissionhandler import PermissionHandler
from datetime import datetime
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.plugin import on_request
from utils.rolehandler import is_add_friend
from .data_source import FriendsDB
notice = on_request(rule=is_add_friend,priority=11)
notice_perm = PermissionHandler("addperson","when notice requests for friends","自动接受好友申请(每日有上限)")
dbh = FriendsDB()
@notice.handle()
async def addperson(bot: Bot, event: Event):
    updatetime = datetime.now().strftime('%Y%m%d')
    user_id = event.get_user_id()
    if dbh.checknum(updatetime):
        dbh.push_person(user_id,updatetime)
        await bot.send_private_msg(user_id=bot.config.dict()["super"],message=f"成功添加好友{user_id}")
        await event.approve(bot)
    else:
        await bot.send_private_msg(user_id=bot.config.dict()["super"],message=f"因为人数限制，未能成功添加好友{user_id}")
