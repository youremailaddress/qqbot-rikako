from nonebot import get_driver
global_config = get_driver().config
from nonebot.plugin import on_startswith
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.typing import T_State
from nonebot.permission import SUPERUSER
from utils.permissionhandler import PermissionHandler
from .data_source import *

bilifocus = on_startswith(msg="B站直播关注",priority=20)
bilifocus_perm = PermissionHandler("bilifocus","B站直播关注 UID","当被关注的主播开启直播时进行私聊推送")
@bilifocus.handle()
async def bilifocus_(bot: Bot, event: Event,state: T_State):
    if not bilifocus_perm.async_checker(bot,event):
        return
    bilidb = BiliLiveDBHandler()
    msg = str(event.message).strip()
    msg = msg.split(" ")
    if len(msg) != 2:
        await bilifocus.finish("参数不正确。用法:B站直播关注 UID")
    else:
        biliid = msg[1]
        if not biliid.isdigit():
           await bilifocus.finish("UID必须为数字") 
        uid = event.get_user_id()
        groupid = 0
        if len(event.get_session_id().split("_"))>1:
            groupid = event.get_session_id().split("_")[1]
        resp = bilidb.push_blive(uid,groupid,biliid)
        bilidb.freedbhandler()
        if resp == False:
            await bilifocus.finish("发生了一些错误，可能是因为您已经超过了关注10人的限制或者您已经关注过该主播")
        else:
            await bilifocus.finish(f"关注{biliid}主播成功！")

bililiveingroup = on_startswith(msg="开启群发直播关注",priority=10,permission=SUPERUSER)
bililiveingroup_perm = PermissionHandler("bililiveingroup","开启群发直播关注 user group biliid","当被关注的主播开启直播时进行群聊推送（只有超级用户可以设置）")
@bililiveingroup.handle()
async def bililiveingroup_(bot: Bot, event: Event,state: T_State):
    msg = str(event.message).strip()
    msg = msg.split(" ")
    if len(msg) != 4:
        await bililiveingroup.finish("参数不正确。用法:开启群发直播关注 user group biliid")
    bilidb = BiliLiveDBHandler()
    bilidb.show_in_group(msg[1],msg[2],msg[3])
    bilidb.freedbhandler()
    await bililiveingroup.finish("开启群发直播关注成功！")

biliunfocus = on_startswith(msg="B站直播取关",priority=20)
biliunfocus_perm = PermissionHandler("biliunfocus","B站直播取关 UID","解除直播私聊推送功能")
@biliunfocus.handle()
async def biliunfocus_(bot: Bot, event: Event,state: T_State):
    if not biliunfocus_perm.async_checker(bot,event):
        return
    msg = str(event.message).strip()
    msg = msg.split(" ")
    if len(msg) != 2:
        await biliunfocus.finish("参数不正确。用法:B站直播取关 UID")
    else:
        biliid = msg[1]
        uid = event.get_user_id()
        bilidb = BiliLiveDBHandler()
        bilidb.remove_blive(uid,biliid)
        bilidb.freedbhandler()
        await biliunfocus.finish(f"取关{biliid}主播成功！")