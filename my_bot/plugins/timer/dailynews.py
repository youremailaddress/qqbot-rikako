from nonebot.adapters.cqhttp.message import Message
async def news(bot,group_id):
    try:
        try:
            img_url = 'https://raw.githubusercontent.com/pkupersonalities/Keji/main/output/img/news.jpg'
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