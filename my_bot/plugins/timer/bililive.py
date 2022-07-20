import requests
def getbililive(uid):
    resp = requests.get(f"https://api.live.bilibili.com/xlive/web-room/v1/index/getRoomBaseInfo?uids={uid}&;req_biz=video")
    js = resp.json()
    if js['data']['by_uids'] == {}:
        return None
    else:
        m = js['data']['by_uids'][str(uid)]
        return m["title"],m['live_url'],m['cover'],m['uname']

def handleblive():
    pass