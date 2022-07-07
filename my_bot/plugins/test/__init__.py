from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp import Bot, Event,GroupMessageEvent
from nonebot import on_command
from utils.permissionhandler import PermissionHandler
matcher = on_command("测试超管",priority=1, permission=SUPERUSER)

@matcher.handle()
async def _(bot: Bot, event: Event):
    await matcher.send("超管命令测试成功")

a = PermissionHandler("test","None","测试")
test = on_command("赫赫",priority=2)
@test.handle()
async def __(bot: Bot, event: Event):
    # a.dbh.push("func_table",a.cfg["func_table"],"insert into func_table(func_name) values (?);",("test",))
    if a.async_checker(bot,event):
        await matcher.send("hh\nhehe")