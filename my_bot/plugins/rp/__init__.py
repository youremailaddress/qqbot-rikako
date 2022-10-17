import random
from datetime import datetime
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from utils.permissionhandler import PMH as perm
from nonebot.plugin import on_command
from .data_source import RPH as rphdle
from utils.multimediahandler import makeAt
import math

def gen_rp():
    rp = random.randint(0,114520)
    if rp > 114500:
        return 114514
    else:
        rp = rp%101
        return round(math.sqrt(rp)*10)

rpcomment = {
    0:["","？","诸事不宜","啊这，真的不是10分满分制吗？"],
    10:["","有倒霉蛋，但我不说他是谁","啧啧，这也太惨了","-.-!!"],
    20:["","好家伙","希望出金的间隔抽数是今天的rp"],
    30:["","怎么会是呢","今天rp有点低，要小心哇"],
    40:["0.0","","patpat"],
    50:["","有点惨，摸摸","再坚持一下就及格了，加油！"],
    60:["","嘛，还好及格了","就那样吧","某种意义上很幸运~"],
    70:["","好好珍惜，会是很有意义的一天！","不要辜负别人的期待，相信自己可以做的更好~"],
    80:["","人品不错，记得多吃点好吃的奖励自己一下","还不错嘛","一般般啦~"],
    90:["低调低调","","是锦鲤！贴贴！","吸吸欧气"],
    100:["","哇！金色传说！","今日rp风向标找到了!","虽然但是，建议你去买彩票"],
    114510:["哼哼啊啊啊啊啊啊","好臭的人品啊啊啊","这是一个一个什么rp啊？","这么臭的彩蛋真的有存在的必要吗（掩鼻"]
}

rp_pro = on_command('今日人品',aliases={"rp","人品"},priority=50)
@rp_pro.handle()
@perm.checker(name="人品",usage="今日人品/人品/rp *",intro="查询今日人品")
async def rp_(bot: Bot, event: Event, state: T_State,matcher: Matcher):
    user_id = event.get_user_id()
    updatetime = datetime.now().strftime('%Y%m%d')
    if rphdle.get_rp(user_id, updatetime):
        rp,comment = rphdle.get_rp(user_id, updatetime)
        await rp_pro.finish("["+makeAt(user_id)+f"]今日rp:{rp}\n{comment}")
    rawrp = gen_rp()
    comment = random.choice(rpcomment[(rawrp//10)*10])
    rphdle.push_rp(user_id,rawrp,comment,updatetime)
    await rp_pro.finish("["+makeAt(user_id)+f"今日rp:{rawrp}\n{comment}")