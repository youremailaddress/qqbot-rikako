from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.matcher import Matcher
from nonebot.typing import T_State
from nonebot import on_command,on_notice
from utils.permissionhandler import PMH as perm
from utils.rolehandler import is_on,is_poke
from nonebot.rule import Rule
from utils.timerhandler import TMH as tmr
from utils.multimediahandler import makePic,makeCardImage
matcher = on_command("测试超管",priority=1, permission=SUPERUSER)

@matcher.handle()
async def _(bot: Bot, event: Event):
    # await matcher.send(makePic("https://cdn.statically.io/gh/pkupersonalities/Keji/main/output/img/news_2022_10_11.jpg",type="show"))
    await matcher.send(makeCardImage("https://cdn.jsdelivr.net/npm/chenyfan-happypic@0.0.3/12.jpg"))
