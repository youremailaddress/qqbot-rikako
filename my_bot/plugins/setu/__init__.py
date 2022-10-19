import httpx
from nonebot.plugin import on_command
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from utils.permissionhandler import PMH as perm
from utils.multimediahandler import makeCardImage,makePic

async def tryCardImage(handler,url):
    try:
        await handler.finish(makeCardImage(url))
    except Exception as e:
        if str(e).strip() != "":
            await handler.finish(makePic(url=url,type="show"))

setu = on_command("来张色图",priority=50)
@setu.handle()
@perm.checker(name="色图",usage="来张色图 来源(默认lolicon) 一至多个查询词 空格分开(默认无)",intro="随机回复一张色图,来源有三:lolicon/yuban/cyfan,可指定切换,其中cyfan不支持按照关键词索引，多个关键词默认与连接，如果找不到图会用或连接，最后尝试无关键词发送")
async def setuhandle(bot: Bot, event: Event,state: T_State,matcher: Matcher):
    msg = str(event.message).strip()
    providers = ["lolicon","yuban","cyfan"]
    fr = 0 # 默认lolicon
    hasquery = False
    if msg != "":
        msgs = msg.split(" ")
        if msgs[0] in providers:
            fr = providers.index(msgs[0])
            if len(msgs) != 1:
                hasquery = True
                query = msgs[1:]
        else:
            hasquery = True
            query = msgs
    if fr == 2 and hasquery:
        await setu.finish("cyfan 不支持查询词")
    if fr == 2 and not hasquery:
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.get('https://api.cyfan.top/acg?restype=json&num=1')
            res = resp.json()
            await tryCardImage(setu,res["ctx"]["url"][0])
    if fr == 0:
        if hasquery == False:
            async with httpx.AsyncClient(timeout=20) as client:
                resp = await client.get('https://api.lolicon.app/setu/v2?proxy=pixiv.re/{{pid}}.{{ext}}')
                res = resp.json()
                print(res["data"][0]["urls"]["original"])
                await tryCardImage(setu,res["data"][0]["urls"]["original"])
        else:
            pass