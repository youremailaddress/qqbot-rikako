import datetime
from utils.timerhandler import TMH as tmr
from nonebot.adapters.cqhttp import Bot
from utils.multimediahandler import makePic,makeCardImage

@tmr.checker(info="爬取每日新闻的定时器")
async def dailynews(bot:Bot,uid,gid,**kwargs):
    try:
        try:
            year = datetime.datetime.now().year
            month = datetime.datetime.now().month
            day = datetime.datetime.now().day
            img_url = f'https://raw.githubusercontent.com/pkupersonalities/Keji/main/output/img/news_{year}_{month}_{day-1}.jpg'
            msg = makeCardImage(img_url)
        except Exception as e:
            print(str(e))
            msg="呜呜，获取日报失败了，快来修理我吧"+str(e)
    except :
        msg="我已经很努力的向报社催了，可能今天的日报卡路上了吧"
    
    try:
        if gid == None:
            await bot.send_private_msg(user_id=uid,message=msg)
        else:
            await bot.send_group_msg(group_id=gid,message=msg)
    except Exception as e:
        print(str(e))
        msg=makePic(img_url,type="show")
        if gid == None:
            await bot.send_private_msg(user_id=uid,message=msg)
        else:
            await bot.send_group_msg(group_id=gid,message=msg)