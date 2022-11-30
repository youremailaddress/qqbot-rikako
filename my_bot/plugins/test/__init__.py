from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.matcher import Matcher
from nonebot.typing import T_State
from nonebot import on_command,on_notice
from utils.funchandler import FunH
from utils.rolehandler import is_on,is_poke
from nonebot.rule import Rule
from utils.multimediahandler import makePic,makeCardImage
test = on_command("测试超管",priority=1)
@test.handle()
@FunH.checker(name="测试超管",usage="测试",intro="测试")
async def _(bot: Bot, event: Event,state: T_State,matcher: Matcher):
    # await matcher.send(makePic("https://cdn.statically.io/gh/pkupersonalities/Keji/main/output/img/news_2022_10_11.jpg",type="show"))
    await test.send(makeCardImage("https://i.pixiv.re/img-original/img/2018/12/10/19/31/15/72055179_p0.jpg"))
