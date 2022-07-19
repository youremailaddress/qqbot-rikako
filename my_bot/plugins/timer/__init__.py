from nonebot import require, get_bot
from utils.permissionhandler import PermissionHandler
from nonebot.adapters.cqhttp.message import Message

news = require("nonebot_plugin_apscheduler").scheduler
news_perm = PermissionHandler("news","9:50 every day","每天发送新闻日报")
@news.scheduled_job("cron", hour="23",minute="26")
async def news_():
    bot = get_bot()
    group_id=482120682
    try:
        try:
            img_url = 'https://raw.githubusercontent.com/BugWriter2/Keji/main/output/img/news.jpg'
            cq = "[CQ:image,file="+img_url+",id=40000]"
            msg=Message(cq)
            await bot.send_group_msg(group_id=group_id, message=msg)
        except Exception as e:
            print(str(e))
            msg="呜呜，获取日报失败了，快来修理我吧"+str(e)
            await bot.send_group_msg(group_id=group_id, message=msg)

    except :
        msg="我已经很努力的向报社催了，可能今天的日报卡路上了吧"
        await bot.send_group_msg(group_id=group_id, message=msg)


