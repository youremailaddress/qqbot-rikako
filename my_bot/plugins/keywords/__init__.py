# import nonebot
from nonebot import get_driver
from .config import Config
conf = get_driver().config

import re,random
from nonebot.exception import FinishedException
from nonebot.adapters.cqhttp.utils import escape,unescape
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.plugin import on_message, on_command,on
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp.permission import GROUP_ADMIN,GROUP_MEMBER,PRIVATE_FRIEND,GROUP_OWNER
from .data_source import *
from .utils import acceptMessage

session,dic = init(conf.group_list)

reply = on_message(priority=100,rule=acceptMessage())
@reply.handle()
async def reply_handle(bot: Bot, event: Event):
    group_id = event.get_session_id().split("_")[1]
    user_msg = (str(event.get_message()).strip())
    if "[CQ:image,file" in user_msg or "&#" in user_msg:
        await reply.finish()
    user_msg = escape(user_msg)
    try:
        for i in get_keyword_list(session, dic[group_id]):
            if re.findall(i, user_msg):
                await reply.send(get_random_reply(session, dic[group_id], i))
                break
    except Exception:
        await reply.finish()

#增填（更改）关键词，格式为“/add 关键词===回复”
add_kw = on_command('添加关键词',aliases={"增加关键词","addkeyword"},priority=50,permission=SUPERUSER|GROUP_MEMBER|GROUP_ADMIN|GROUP_OWNER,rule=acceptMessage())
@add_kw.handle()
async def add_kw_handle(bot: Bot, event: Event):
    group_id = event.get_session_id().split("_")[1]
    try:
        user_msg = str(event.get_message()).strip()
        keyword,replyword = user_msg.split('===')  #分割关键词和回复
        keyword = keyword.strip()
        keyword = escape(keyword)
    except:
        await add_kw.finish("用法不对哦~用法:添加关键词 关键词===回复,支持python风格的正则表达式-.-")
        raise FinishedException
    if pushwords(session, dic[group_id], keyword, replyword):
        await add_kw.finish(f'已成功添加或更改 {unescape(keyword)} => {replyword}')
    else:
        await add_kw.finish(f'关键词对{unescape(keyword)} => {replyword}已经在列表里啦，不需要重复添加喔')
    

#删除关键词，格式为“/del 关键词”
del_kw = on_command('删除关键词',aliases={"去掉关键词","delkeyword"},priority=50,permission=SUPERUSER|GROUP_MEMBER|GROUP_ADMIN|GROUP_OWNER,rule=acceptMessage())                
@del_kw.handle()
async def del_kw_handle(bot: Bot, event: Event):
    group_id = event.get_session_id().split("_")[1]
    try: 
        user_msg = str(event.get_message()).strip()
        keyword,replyword = user_msg.split('===')
        keyword = keyword.strip()
        keyword = escape(keyword)
        replyword = replyword.strip()
    except:
        await del_kw.finish("用法不对哦~用法:删除关键词 关键词===回复")
        raise FinishedException
    if not delkeywords(session, dic[group_id], keyword, replyword):
        await del_kw.finish(f"关键词 {unescape(keyword)} 对应的 {unescape(replyword)} 不存在")
    else:
        await del_kw.finish(f'已成功删除 {unescape(keyword)} => {unescape(replyword)}')

#查看关键词，格式为“/check”
check_kw = on_command('查询关键词',aliases={"查看关键词"},priority=50,permission=SUPERUSER|PRIVATE_FRIEND|GROUP_ADMIN|GROUP_MEMBER|GROUP_OWNER,rule=acceptMessage())                
@check_kw.handle()
async def check_kw_handle(bot: Bot, event: Event):
    group_id = event.get_session_id().split("_")[1]
    reply_msg_list = ["关键词列表为:"]
    kwdic = get_keyword_response_form(session, dic[group_id])
    for keyword,replyword in kwdic.items():
        msg = f'{unescape(keyword)} => {str(replyword)}'
        reply_msg_list.append(msg)
    reply_msg = '\n'.join(reply_msg_list)
    await check_kw.finish(reply_msg)