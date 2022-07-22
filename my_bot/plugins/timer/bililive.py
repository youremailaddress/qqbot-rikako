import requests,time
from ..bililivereminder.data_source import BiliLiveDBHandler
from nonebot.adapters.cqhttp.message import Message

def gettimestamp(timestr):
    return int(time.mktime(time.strptime(timestr,'%Y-%m-%d %H:%M:%S')))

def getbililive(uid):
    resp = requests.get(f"https://api.live.bilibili.com/xlive/web-room/v1/index/getRoomBaseInfo?uids={uid}&;req_biz=video")
    js = resp.json()
    if js['data']['by_uids'] == {}:
        return None
    else:
        m = js['data']['by_uids'][str(uid)]
        return m["title"],m['live_url'],m['cover'],m['uname'],m["live_time"]

async def handleblive(bot):
    bilidb = BiliLiveDBHandler()
    dic = bilidb.fetch_blive()
    for k,v in dic.items():
        resp = getbililive(k)
        if resp == None:
            continue
        title,liveurl,cover,uname,livetime = resp
        for config in v:
            if int(time.time())-gettimestamp(livetime)>60:
                continue
            elif config["ingroup"] == 0:
                msg = Message(f"你关注的{uname}主播开播啦，直播名字{title}，直播地址{liveurl}")
                await bot.send_private_msg(user_id=config["user"],message=msg+Message(f'[CQ:image,file={cover}]'))
            else:
                msg = Message(f"你关注的{uname}主播开播啦，直播名字{title}，直播地址{liveurl}")
                await bot.send_group_msg(group_id=config["group"], message=msg+Message(f'[CQ:image,file={cover}]'))
    bilidb.freedbhandler()