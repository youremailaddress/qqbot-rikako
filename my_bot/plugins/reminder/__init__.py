from curses.ascii import isdigit
from nonebot import on_command
from utils.permissionhandler import PMH as perm

from nonebot.adapters.cqhttp import Bot, Event
from nonebot.matcher import Matcher
from nonebot.typing import T_State

from utils.timerhandler import TMH as tmr
import time

testtime = on_command("添加提醒",priority=1)
@testtime.handle()
@perm.checker(name="添加提醒",usage="添加提醒 时间(格式xx:xx,24小时制) 提醒内容 群聊(默认)/私聊(需加好友) 时间间隔(不填为一次,以秒为单位)",intro="提醒做某事（写完代码才发现目前非重复性任务只能一天内提醒，有点鸡肋。。下个版本改），时间和提醒内容必填，默认在群聊中发一次,**提醒内容不能有空格**")
async def _tim_(bot: Bot, event: Event,state: T_State,matcher: Matcher):
    msg = str(event.message).strip()
    if len(msg.split(" ")) < 2:
        await testtime.finish("添加提醒格式错误！请查看介绍")
    tm = msg[0]
    assert len(tm.split(":")) == 2
    try:
        hour = int(tm.split(":")[0])
        minute = int(tm.split(":")[1])
    except:
        await testtime.finish("添加提醒格式错误！请查看介绍")
    start = int(time.time()) -int(time.time()-time.timezone)%86400 + hour*3600+minute*60 
    mindthings = msg[1]
    usid = event.get_user_id()
    groupid = None
    if len(event.get_session_id().split("_"))>1:
        groupid = event.get_session_id().split("_")[1]
    isgroup = True
    isonetime = True
    if "私聊" in msg[2:]:
        isgroup = False
    if isgroup == True and groupid == None:
        await testtime.finish("私聊添加提醒无法指定群聊，请重试")
    if msg[-1].isdigit():
        isonetime = False
    if isgroup:
        uid = "*"
        gid = groupid
    else:
        gid = "@"
        uid = usid
    if isonetime:
        interval = 0
    else:
        interval = msg[-1]
    res = tmr.addTime("reminder",f"{start}_{interval}",uid,gid,msg=mindthings,sender=usid,sendtime=int(time.time()))
    if res == False:
        await testtime.send("添加提醒失败，可能是因为您的定时任务超出配额，请删除无用的定时任务")
    else:
        await testtime.send("添加提醒成功！将会在指定时间提醒您")