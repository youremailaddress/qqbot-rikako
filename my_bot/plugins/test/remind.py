from utils.timerhandler import TMH as tmr
from nonebot.adapters.cqhttp import Bot

@tmr.checker(info="remind sb sth")
async def reminder(bot:Bot,uid,gid,**kwargs):
    await bot.send_private_msg(user_id=uid,message=str(kwargs))