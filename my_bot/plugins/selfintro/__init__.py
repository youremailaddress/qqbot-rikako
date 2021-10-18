# import nonebot
from nonebot import get_driver

from .config import Config
from nonebot.exception import FinishedException
from nonebot.matcher import StopPropagation,Matcher
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import MessageEvent,MessageSegment
from nonebot.adapters.cqhttp import Bot, Event
global_config = get_driver().config
# config = Config(**global_config.dict())
from .utils import acceptMessage
from nonebot.plugin import on_message, on_command,on_shell_command
from nonebot.rule import ArgumentParser

intro_arg = ArgumentParser()
intro_arg.add_argument("-全部","--all",action="store_true")
intro_arg.add_argument("-缩略","--part",action="store_true")
intro_arg.add_argument("-收集表","--table",action="store_true")
intro_arg.add_argument("-任务单","--todo",action="store_true")
intro_arg.add_argument("-时间线","--timeline",action="store_true")
intro_arg.add_argument("-项目地址","--github",action="store_true")
intro_arg.add_argument("-功能","--func",action="store_true")
intro_arg.add_argument('names', nargs='*')
intro_reply = on_shell_command("介绍",aliases={"selfintroduction","intro"},rule=acceptMessage(),priority=10,parser=intro_arg)
@intro_reply.handle()
async def intro_(bot: Bot, event: Event,state:T_State):
    args = state['args']
    superadmin = MessageSegment.at(user_id=int(list(global_config.superusers)[0]))
    dic = {
        "part":"Hello,我是Rikako,一个基于Nonebot2架构的还在慢慢成长的QQ群机器人。我还有一个名字叫奶茶(我妈起的nickname)，我爸是"+superadmin,
        "part2":"我生日是1月6号，现在还不到一岁哦~中间的大半年里我被封存起来了，最近才开始进群跟大家见面！嘿嘿，大家多多关照喔。",
        "table":"这里是我的收集表https://docs.qq.com/form/page/DUEFlaHdKQ3RKSWlk,刚出来见世面总有一些做的不好的地方，还希望大家能多提一点建议！感谢（鞠躬）",
        "todo":"这是我的任务单https://docs.qq.com/doc/DUHl0RGtrZnZsbEZi，大家可以看看已经在加强的工作，提需求的时候可以先看看是不是有类似要求了哈，我爸也很忙的，大家理解一下(wink~)",
        "timeline":"这是我爸给我做的我从小到大的大事件嘿嘿https://coal-society-cd6.notion.site/de29b7a1c0634e1dbf47fe81343cc749?v=2a47581d0e794ad29a657827e1a83428，可以看看我经历了什么变化！什么？没更新？我这就去催我爸（bs",
        "github":"现在还没有项目地址咧，不过我爸想等我长大成熟一点之后就开源，可以期待一下喔！",
        "func":"目前我的功能还不是很多，开放给大家的只有很少的几个模块，大家可以通过命令 都有啥功能 查看模块的详细用法，注意别太过火把我玩坏了QWQ"
        }
    if args.all:
        msg = ""
        for v in dic.values():
            msg += v+"\n"
        await intro_reply.finish(msg)
    if args.part:
        await intro_reply.send(dic["part"])
    if args.table:
        await intro_reply.send(dic["table"])
    if args.todo:
        await intro_reply.send(dic["todo"])
    if args.timeline:
        await intro_reply.send(dic["timeline"])
    if args.github:
        await intro_reply.send(dic["github"])
    if args.func:
        await intro_reply.send(dic["func"])
    await intro_reply.finish()

func_reply = on_command("都有啥功能",aliases={"功能列表"},rule=acceptMessage(),priority=11)
@func_reply.handle()
async def func_(bot: Bot, event: Event,state:T_State):
    await func_reply.finish("目前上线的功能:\n关键词(keywords),适用范围:所有群员.用法:\n\t1.添加(或者增加)关键词 关键词===回复\n\t2.删除(或者去掉)关键词 关键词===回复\n\t3.查询(或者查看)关键词\n主控(admin),适用范围:SUPERUSER.用法:\n\t1.开机\n\t2.关机\n\t3.启用(禁用) -[强制] 包名\n自我介绍(selfintro),适用范围:所有群员.用法:\n\t1.介绍 -[全部/缩略/收集表/任务单/时间线/项目地址/功能](可多选)\n\t2.都有啥功能(或者功能列表)\n今日人品(rp),适用范围:所有群员.用法:\n\t1.群里输入rp\n一言(liuhua),适用范围:所有群员.用法:\n\t1.群里戳一戳rikako")