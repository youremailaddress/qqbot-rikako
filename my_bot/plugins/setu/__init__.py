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
@perm.checker(name="色图",usage="来张色图 一至多个查询词(空格分开、默认无)",intro="随机回复一张色图,来源:lolicon,多个关键词默认与连接，如果找不到图会用或连接，最后尝试无关键词发送")
async def setuhandle(bot: Bot, event: Event,state: T_State,matcher: Matcher):
    msg = str(event.message).strip()
    if msg == "":
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.get('https://api.lolicon.app/setu/v2?proxy=pixiv.re/{{pid}}.{{ext}}')
            res = resp.json()
            await tryCardImage(setu,res["data"][0]["urls"]["original"])
    else:
        queries = msg.split(" ")
        querystring = "&tag=" + "&tag=".join(queries)
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.get('https://api.lolicon.app/setu/v2?proxy=pixiv.re/{{pid}}.{{ext}}&r18=0'+querystring)
            res = resp.json()
            print(res)
            await tryCardImage(setu,res["data"][0]["urls"]["original"])
