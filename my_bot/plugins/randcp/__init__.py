# import nonebot
from nonebot import get_driver
import random,math
from datetime import datetime
from .config import Config
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.typing import T_State
from nonebot.plugin import on_message, on_command,on_shell_command
from nonebot.adapters.cqhttp import MessageSegment
conf = get_driver().config
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp.permission import GROUP_ADMIN,GROUP_MEMBER,PRIVATE_FRIEND,GROUP_OWNER
from .utils import acceptMessage
from .data_source import *
from nonebot.rule import ArgumentParser
import os.path

import sqlite3
db_1=os.path.split(os.path.realpath(__file__))[0]+"/test.db",
print(db_1)
conn = sqlite3.connect(db_1[0])
cus = conn.cursor()


session,dic = init(conf.group_list)
cp_parser = ArgumentParser()
cp_parser.add_argument('names', nargs='*')
cp_pro = on_shell_command('随机cp',aliases={"cp","磕"},parser=cp_parser,priority=50,permission=SUPERUSER|GROUP_MEMBER|GROUP_ADMIN|GROUP_OWNER,rule=acceptMessage())
@cp_pro.handle()
async def cp_(bot: Bot, event: Event,state: T_State):
    group_id = event.get_session_id().split("_")[1]
    user_id = event.get_session_id().split("_")[2]
    updatetime = datetime.now().strftime('%Y%m%d')
    _group_user_list = await bot.get_group_member_list(group_id=group_id)
    print(_group_user_list)
    args = state['args']
    gong = None
    shou = None
    try:
        if len(args.names)>2:
            await cp_pro.finish("磕一群人的cp不是好文明(什么")
        else:
            if len(args.names)==1 and random.randint(0,1):
                gong = args.names[0][10:-1]
            elif len(args.names)==1:
                shou = args.names[0][10:-1]
            elif len(args.names)==2:
                gong = args.names[0][10:-1]
                shou = args.names[1][10:-1]
        if gong == "all" or shou == "all":
            await cp_pro.finish("磕一群人的cp不是好文明(什么")
    except:
        await cp_pro.finish("有点看不懂你在磕谁，要在群里@要磕的人才可以喔")
    if gong == None:
        gong = random.choice(_group_user_list)['nickname']
    else:
        idlis = [i['user_id'] for i in _group_user_list]
        ind = idlis.index(int(gong))
        gong = _group_user_list[ind]['nickname']
    if shou == None:
        shou = random.choice(_group_user_list)['nickname']
    else:
        idlis = [i['user_id'] for i in _group_user_list]
        ind = idlis.index(int(shou))
        shou = _group_user_list[ind]['nickname']
    if check_can(session, dic[group_id], user_id, updatetime):
        cus.execute("select CONTENT from DB where id=?",(random.randint(0,212),))
        await cp_pro.finish(cus.fetchone()[0].replace("<攻>",gong).replace("<受>",shou))
    else:
        await cp_pro.finish("今天的cp就磕到这儿了，吃太多糖对身体不好喔~")
        