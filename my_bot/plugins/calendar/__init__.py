from nonebot.adapters.cqhttp import Bot, Event
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from utils.permissionhandler import PMH as perm
from nonebot.plugin import on_command
import json,time,datetime
from nonebot import get_driver
driver = get_driver()
global_config = get_driver().config

def calendarhandler(strtime):
    print(strtime)
    with open(global_config.root+"my_bot/plugins/calendar/final.json") as f:
        txt = f.read()
    a = json.loads(txt)
    gotit = False
    nextlis = []
    res = strtime+"\n"
    for item in a["data"]:
        if item["time"] == strtime:
            gotit = True
            res += f"农历{item['lunar']}\n{item['week']}\n"
            if item["festival"] != []:
                res += f"今天是{'、'.join(item['festival'])}\n"
        if gotit == True and len(nextlis)>5:
            break
        if gotit == True and len(nextlis)<=5 and item["festival"] != []:
            nextlis.append((item["time"],item["festival"]))
    res += "最近的节日:\n"
    for itms in nextlis:
        res += f"{itms[0]} {'、'.join(itms[1])}\n"
    return res[:-1]

calen = on_command('日历',priority=50)
@calen.handle()
@perm.checker(name="日历",usage="日历 (xxxx-xx-xx)[可选]",intro="查询某日（默认本日）附近日历")
async def calender(bot: Bot, event: Event, state: T_State,matcher: Matcher):
    msg = str(event.message).strip()
    if msg == "":
        tmstr = time.strftime("%Y-%m-%d")
    else:
        try:
            tmstr = time.strftime("%Y-%m-%d",time.strptime(msg,"%Y-%m-%d"))
        except:
            return
    await calen.finish(calendarhandler(tmstr))

countdown = on_command("倒计时",priority=55)
@countdown.handle()
@perm.checker(name="倒计时",usage="倒计时 (高考/考研)",intro="查询距离高考/考研剩余天数")
async def countdown_(bot: Bot, event: Event, state: T_State,matcher: Matcher):
    msg = str(event.message).strip()
    time_now = datetime.datetime.now()
    if msg not in ["高考","考研"]:
        return
    else:
        if msg == "高考":
            gaokao_time = datetime.datetime(2023, 6, 7)
            await countdown.finish(f"距2023年高考还有{(gaokao_time-time_now).days}天")
        if msg == "考研":
            kaoyan_time = datetime.datetime(2022,12,25)
            await countdown.finish(f"距2022年考研初试还有{(kaoyan_time-time_now).days}天")