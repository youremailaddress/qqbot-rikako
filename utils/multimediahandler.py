from nonebot.adapters.cqhttp.message import Message
from nonebot import get_driver
driver = get_driver()
global_config = get_driver().config

def makePoke(uid:str):
    '''
    戳一戳别人，群/私聊均可用
    '''
    assert uid.isdigit()
    return Message(f"[CQ:poke,qq={uid}]")

def makeAt(uid:str):
    '''
    AT别人，群可用
    '''
    assert uid.isdigit()
    return Message(f"[CQ:at,qq={uid}]")

def makeAtAll():
    '''
    AT全体成员，均可用，但只有在是管理员的群里才会提醒
    '''
    return Message("[CQ:at,qq=all]")

def makePic(url:str,type):
    '''
    发图片 url 可以是网上图片url，也可以是相对于./tmp/images/的路径，type分flash和show
    '''
    if type not in ["flash","show"]:
        return ""
    if url.startswith("http"):
        return Message(f"[CQ:image,file={url},type={type},id=40000]")
        # return Message(f"[CQ:image,file={url}]")
    else:
        return Message(f"[CQ:image,file=file:///{global_config.root}tmp/images/{url},type={type}]")

def makeTts(text:str):
    '''
    文字转语音发送
    '''
    return Message(f"[CQ:tts,text={text}]")

def makeReply():
    pass

def makeShare(url,title,content=None,image=None):
    '''
    链接分享 经测试似乎只能私聊发送
    '''
    if content==None and image==None:
        return Message(f"[CQ:share,url={url},title={title}]")
    elif content==None and image!=None:
        return Message(f"[CQ:share,url={url},title={title},image={image}]")
    elif content!=None and image==None:
        return Message(f"[CQ:share,url={url},title={title},content={content}]")
    else:
        return Message(f"[CQ:share,url={url},title={title},image={image},content={content}]")

def makeMusicShare(type,_id=None,subtype=None,url=None,audio=None,title=None,content=None,image=None):
    '''
    音乐或自定义音乐分享 经测试似乎也只能私聊发送
    '''
    if type in ["qq","163","xm"] and _id != None:
        return Message(f"[CQ:music,type={type},id={_id}]")
    elif type == "custom" and subtype!=None and url != None and audio!=None and title != None:
            if content==None and image==None:
                return Message(f"[CQ:music,type=custom,subtype={subtype},url={url},audio={audio},title={title}]")
            elif content==None and image!=None:
                return Message(f"[CQ:share,type=custom,subtype={subtype},url={url},audio={audio},title={title},image={image}]")
            elif content!=None and image==None:
                return Message(f"[CQ:share,type=custom,subtype={subtype},url={url},audio={audio},title={title},content={content}]")
            else:
                return Message(f"[CQ:share,type=custom,subtype={subtype},url={url},audio={audio},title={title},image={image},content={content}]")
    else:
        return ""

def makeNode():
    pass

def makeXML():
    pass

def makeJson():
    pass

def makeCardImage(file):
    '''
    发送卡片大图 群和私聊均可（疑惑
    '''
    return Message(f"[CQ:cardimage,file={file}]")