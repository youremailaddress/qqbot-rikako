from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp import Bot, Event,GroupMessageEvent
from nonebot.matcher import Matcher
from nonebot.typing import T_State
from nonebot import on_command,on_notice
from utils.permissionhandler import PMH as perm
from utils.rolehandler import is_on,is_poke
from nonebot.rule import Rule
from utils.timerhandler import TMH as tmr
import time
matcher = on_command("测试超管",priority=1, permission=SUPERUSER)

@matcher.handle()
async def _(bot: Bot, event: Event):
    await matcher.send("超管命令测试成功")

test = on_notice(priority=2,rule=is_poke)
@test.handle()
@perm.checker(name="测试",usage="test",intro="test")
async def __(bot: Bot, event: Event,state: T_State,matcher: Matcher):
    await test.send("heheh")

# testtime = on_command("提醒",priority=1, permission=SUPERUSER)
# @testtime.handle()
# @perm.register(name="提醒",usage="testtime",intro="testtime")
# async def _tim_(bot: Bot, event: Event,state: T_State,matcher: Matcher):
#     msg = str(event.message).strip()
#     a = msg.split(" ")[0]
#     b = msg.split(" ")[1]
#     tmr.addTime("reminder",f"{int(time.time()+100)}_{0}",a,"@",b=b)
#     await testtime.send(msg)