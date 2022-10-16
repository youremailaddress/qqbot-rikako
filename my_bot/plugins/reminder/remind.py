from utils.timerhandler import TMH as tmr
from nonebot.adapters.cqhttp import Bot
from utils.multimediahandler import makeAt
import time
@tmr.checker(info="remind sb sth")
async def reminder(bot:Bot,uid,gid,**kwargs):
    if uid == None:
        msg = f"[一条来自{makeAt(kwargs['sender'])}在{time.strftime('%Y/%m/%d %H:%M',time.localtime(kwargs['sendtime']))}设置的提醒消息]{kwargs['msg']}"
        await bot.send_group_msg(group_id=gid,message=msg)
    else:
        msg = f"[一条在{time.strftime('%Y/%m/%d %H:%M',time.localtime(kwargs['sendtime']))}时设置的提醒消息]{kwargs['msg']}"
        await bot.send_private_msg(user_id=uid,message=msg)