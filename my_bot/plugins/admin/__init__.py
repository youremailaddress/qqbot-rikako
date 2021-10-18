# import nonebot
from nonebot import get_driver
from .config import Config
driver = get_driver()
global_config = get_driver().config

from .data_source import *

from nonebot.matcher import StopPropagation,Matcher
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event,GroupMessageEvent
from nonebot.plugin import on_message, on_command,on_shell_command,get_loaded_plugins
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp.permission import PRIVATE_FRIEND,GROUP_ADMIN
from nonebot.utils import run_sync
from nonebot.rule import ArgumentParser

session = init()

admin = on_command('关机',priority=1,permission=SUPERUSER)
@admin.handle()
async def reply_handle(bot: Bot, event: Event):
    global_config.set_on = False
    await admin.send("Rikako已经关闭啦.")
    

adon = on_command('开机',priority=1,permission=SUPERUSER)
@adon.handle()
async def reply_handle(bot: Bot, event: Event):
    if global_config.set_on ==  False:
        await admin.send("芜湖开机")
        global_config.set_on =  True
    else:
        await admin.send("已经开机了啦")



adplugin_parser = ArgumentParser()
adplugin_parser.add_argument("-强制","--force",action='store_true')
adplugin_parser.add_argument('names', nargs='*')
adplugin = on_shell_command('禁用',parser=adplugin_parser,priority=3,permission=SUPERUSER)
@adplugin.handle()
async def reply_handle(bot: Bot, event: Event,state: T_State):
    if not isinstance(event,GroupMessageEvent):
        await adplugin.finish("请在要禁用的群里发此消息！")
    groupid = event.get_session_id().split("_")[1]
    args = state['args']
    if args.names == []:
        await adplugin.finish(f"参数太多或者太少，给我整不会了")
    if args.names[0] not in [i.name for i in get_loaded_plugins()]:
        await adplugin.finish(f"您要禁用的插件{args.names[0]}不存在，您禁用了个寂寞")
    if len(args.names)!=1:
        await adplugin.finish(f"参数太多或者太少，给我整不会了")

    if args.names[0] == "admin":
        await adplugin.finish("关闭admin插件会让俺无法正常运行，爱Rikako人士表示强烈谴责！")
    else:
        if pushone(session, (args.names[0],groupid)):
            if args.force:
                try:
                    global_config.disabled_settings[args.names[0]].append(groupid)
                except KeyError:
                    global_config.disabled_settings[args.names[0]] = [groupid]
                await adplugin.finish(f"已经在{groupid}关闭了{args.names[0]}功能，即刻执行")
            else:
                await adplugin.finish(f"下次硬启动将在{groupid}关闭{args.names[0]}功能")
        else:
            await adplugin.finish(f"{args.names[0]}插件已经在{groupid}中处于关闭状态")


adpluginon_parser = ArgumentParser()
adpluginon_parser.add_argument("-强制","--force",action='store_true')
adpluginon_parser.add_argument('names', nargs='*')
adpluginon = on_shell_command('启用',parser=adpluginon_parser,priority=4,permission=SUPERUSER)
@adpluginon.handle()
async def reply_handle(bot: Bot, event: Event,state: T_State):
    if not isinstance(event,GroupMessageEvent):
        await adpluginon.finish("请在要启用的群里发此消息！")
    groupid = event.get_session_id().split("_")[1]
    print(groupid)
    args = state['args']
    if args.names == []:
        await adpluginon.finish(f"参数太多或者太少，给我整不会了")
    if args.names[0] not in [i.name for i in get_loaded_plugins()]:
        await adpluginon.finish(f"您要启用的插件{args.names[0]}不存在，您启用了个寂寞")
    if len(args.names)!=1:
        await adpluginon.finish(f"参数太多或者太少，给我整不会了")
    else:
        if pullone(session, (args.names[0],groupid)):
            if args.force:
                try:
                    global_config.disabled_settings[args.names[0]].remove(groupid)
                except ValueError as e:
                    print(str(e))
                    await adpluginon.finish(f"{args.names[0]}插件已经在{groupid}中处于开启状态")
                await adpluginon.finish(f"已经在{groupid}启用了{args.names[0]}功能，即刻执行")
            else:
                await adpluginon.finish(f"下次硬启动将在{groupid}开启{args.names[0]}功能")
        else:
            await adpluginon.finish(f"{args.names[0]}插件已经在{groupid}中处于开启状态")

handleall = on_message(priority=2,block=False)
@handleall.handle()
async def reply_handle(bot: Bot, event: Event,matcher: Matcher):
    if not global_config.set_on:
        matcher.stop_propagation()

@driver.on_startup
async def start():
    run_sync(func=fetch(session))

@driver.on_shutdown
async def shutdown():
    run_sync(func=push(session, global_config.disabled_settings))


# 开关机
# 插件在某群是否响应 暂时还是永远 永远的取消方法
# 消息自动收集
