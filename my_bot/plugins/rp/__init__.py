# import nonebot
from nonebot import get_driver
import random,math
from datetime import datetime
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.plugin import on_message, on_command
from nonebot.adapters.cqhttp import MessageSegment
conf = get_driver().config
from utils.permissionhandler import PermissionHandler
from .data_source import *

rpcomment = {
    "0":["0.0","诸事不宜","有倒霉蛋，但我不说他是谁","","啊这","好家伙","啧啧，这也太惨了"],
    "10":["0.0","","啊这","有倒霉蛋，但我不说他是谁","好家伙","啧啧，这也太惨了"],
    "20":["","0.0","啊这","好家伙","今天rp有点低，要小心哇"],
    "30":["","0.0","啊这","好家伙","今天rp有点低，要小心哇"],
    "40":["","好家伙","patpat","今天rp有点低，要小心哇"],
    "50":["","有点惨，摸摸","就那样吧"],
    "60":["","嘛，还好及格了","就那样吧"],
    "70":["","还不错嘛","人品不错，记得多好吃的奖励自己一下","一般般啦~"],
    "80":["","人品不错，记得多好吃的奖励自己一下","一般般啦~"],
    "90":["低调低调","","是锦鲤！贴贴！","一般般啦~"],
    "100":["","哇！金色传说！","吸吸欧气","今日rp风向标找到了!","是锦鲤！贴贴！"],
    "114510":["","哼哼啊啊啊啊啊啊","好臭的人品啊啊啊","虽然但是，建议你去买彩票"]
}

rpdb = RPDBHandler()
rp_pro = on_command('今日人品',aliases={"rp","人品"},priority=50)
rp_pro_perm =  PermissionHandler("rp","rp *","查询今日人品")
@rp_pro.handle()
async def rp_(bot: Bot, event: Event):
    if not rp_pro_perm.async_checker(bot, event):
        return
    user_id = event.get_user_id()
    updatetime = datetime.now().strftime('%Y%m%d')
    if rpdb.get_rp(user_id, updatetime):
        rp,comment = rpdb.get_rp(user_id, updatetime)
        if comment!="":
            await rp_pro.finish("["+MessageSegment.at(user_id=int(user_id))+f"]今日rp:{rp}\n{comment}")
        else:
            await rp_pro.finish("["+MessageSegment.at(user_id=int(user_id))+f"]今日rp:{rp}\n{comment}")
    rp = random.randint(0,114520)
    if rp == 114514:
        comment = random.choice(rpcomment["114510"])
        rpdb.push_rp(user_id, rp, comment, updatetime)
        await rp_pro.finish("["+MessageSegment.at(user_id=int(user_id))+f"]今日rp:{rp}\n{comment}")
    else:
        rp_raw = rp%101
        rp_raw = int(math.sqrt(rp_raw)*10)
        rp = str(int((rp%101)/10)*10)
        comment = random.choice(rpcomment[rp])
        rpdb.push_rp(user_id, rp_raw, comment, updatetime)
        await rp_pro.finish("["+MessageSegment.at(user_id=int(user_id))+f"]今日rp:{rp_raw}\n{comment}")


        