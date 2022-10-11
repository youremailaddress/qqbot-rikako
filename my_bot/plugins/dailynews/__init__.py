from nonebot.adapters.cqhttp import Bot, Event
from nonebot.matcher import Matcher
from nonebot.typing import T_State
from nonebot import on_command
from utils.timerhandler import TMH as tmr
from utils.permissionhandler import PMH as perm
import time

handledailynews = on_command("订阅日报",priority=50)
@handledailynews.handle()
@perm.checker(name="订阅日报",usage="订阅日报 xx:xx[时间,几时几分,24小时制] [群聊/私聊](可选 默认群聊) [一次/永久](可选 默认永久)",intro="易即今日日报订阅，时间是24小时制，建议是9:15之后,那时之前可能因为没有更新而失败,群聊为本群，私聊为发起人(需要加好友)")
async def DailyNewsHandler(bot: Bot, event: Event, state: T_State,matcher: Matcher):
    msg = str(event.message).strip()
    usid = event.get_user_id()
    groupid = None
    if len(event.get_session_id().split("_"))>1:
        groupid = event.get_session_id().split("_")[1]
    isgroup = True
    ispermanent = True
    if "私聊" in msg:
        isgroup = False
    if "一次" in msg:
        ispermanent = False
    tims = msg.split(" ")[0].split(":")
    assert len(tims) == 2
    try:
        hour = int(tims[0])
        minute = int(tims[1])
    except:
        await handledailynews.finish("格式不正确，请看介绍")
    start = int(time.time()) -int(time.time()-time.timezone)%86400 + hour*3600+minute*60 
    if ispermanent:
        tim = f"{start}_{86400}"
    else:
        tim = f"{start}_{0}"
    if isgroup:
        if groupid == None:
            await handledailynews.finish("私聊中无法指定群聊订阅，请指定私聊订阅或者在群聊中订阅")
        else:
            uid = "*"
            gid = groupid
    else:
        uid = usid
        gid = "@"
    res = tmr.addTime("dailynews",tim,uid,gid,usid)
    if res == False:
        await handledailynews.finish("无法添加定时任务，这有可能是因为定时任务数目超过上限导致的，请使用命令查看并删除无用定时任务")
    else:
        await handledailynews.finish("添加定时任务成功，将于下次指定时间触发")