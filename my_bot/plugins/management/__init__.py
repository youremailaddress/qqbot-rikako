from nonebot import get_driver
from utils.functions import EditDist
driver = get_driver()
global_config = get_driver().config
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.plugin import on_command,on_startswith
from nonebot.permission import SUPERUSER
from utils.rolehandler import is_on
from my_bot.handlers.interacthandler import BH

shut_down = on_command("关机",aliases={"shut down"},priority=1,permission=SUPERUSER)
@BH.checker(name="关机",usage="关机/shut down",intro="关闭Rikako，使其只接受开机指令",isAdmin=True)
@shut_down.handle()
async def shutDownFunc(bot: Bot, event: Event, state: T_State,matcher: Matcher):
    global_config.set_on = False
    await shut_down.finish("Rikako已经关闭啦.")

power_on = on_command('开机',aliases={"power on"},priority=1,permission=SUPERUSER)
@BH.checker(name="开机",usage="开机/power on",intro="开启Rikako，使其处于活跃状态",isAdmin=True)
@power_on.handle()
async def powerOnHandle(bot: Bot, event: Event, state: T_State,matcher: Matcher):
    if global_config.set_on ==  False:
        global_config.set_on =  True
        await power_on.finish("芜湖开机")
    else:
        await power_on.finish("已经开机了啦")

add_perm = on_startswith(msg="添加权限",priority=2,rule=is_on,permission=SUPERUSER)
@BH.checker(name="添加权限",usage="添加权限 函数名 若干用户（(*|@|groupid)_(*|#1|#2|#3|#4|userid)）",intro="添加若干用户权限至某函数",isAdmin=True)
@add_perm.handle()
async def addPermHandle(bot: Bot, event: Event, state: T_State,matcher: Matcher):
    msg = str(event.message).strip()
    msg = msg.split(" ")
    if len(msg) < 3:
        await add_perm.finish("参数不够喔。")
    funcname = msg[1]
    users = msg[2:]
    ret = ""
    for user in users:
        if len(user.split("_"))!=2:
            ret += f"用户 {user} 加入函数 {funcname} 权限被跳过\n"
            continue
        res = BH.addPerm(funcname,user.split("_")[1],user.split("_")[0])
        if res == False:
            ret += f"用户 {user} 加入函数 {funcname} 权限失败\n"
        else:
            ret += f"用户 {user} 加入函数 {funcname} 权限成功\n"
    await add_perm.finish(ret[:-1])

del_perm = on_startswith(msg="删除权限",priority=2,rule=is_on,permission=SUPERUSER)
@BH.checker(name="删除权限",usage="删除权限 函数名 若干用户（(*|@|groupid)_(*|#1|#2|#3|#4|userid)）",intro="删除若干用户权限至某函数",isAdmin=True)
@del_perm.handle()
async def delPermHandle(bot: Bot, event: Event, state: T_State,matcher: Matcher):
    msg = str(event.message).strip()
    msg = msg.split(" ")
    if len(msg) < 3:
        await del_perm.finish("参数不够喔。")
    funcname = msg[1]
    users = msg[2:]
    ret = ""
    for user in users:
        if len(user.split("_"))!=2:
            ret += f"用户 {user} 删除函数 {funcname} 权限被跳过\n"
            continue
        res = BH.delPerm(funcname,user.split("_")[1],user.split("_")[0])
        if res == False:
            ret += f"用户 {user} 删除函数 {funcname} 权限失败\n"
        else:
            ret += f"用户 {user} 删除函数 {funcname} 权限成功\n"
    await del_perm.finish(ret[:-1])

add_perm_black = on_startswith(msg="添加黑名单",priority=2,rule=is_on,permission=SUPERUSER)
@BH.checker(name="添加黑名单",usage="添加黑名单 函数名 若干用户（(*|@|groupid)_(*|#1|#2|#3|#4|userid)）",intro="添加若干用户权限至某函数黑名单",isAdmin=True)
@add_perm_black.handle()
async def addPermBlackHandle(bot: Bot, event: Event, state: T_State,matcher: Matcher):
    msg = str(event.message).strip()
    msg = msg.split(" ")
    if len(msg) < 3:
        await add_perm_black.finish("参数不够喔。")
    funcname = msg[1]
    users = msg[2:]
    ret = ""
    for user in users:
        if len(user.split("_"))!=2:
            ret += f"用户 {user} 加入函数 {funcname} 黑名单被跳过\n"
            continue
        res = BH.addPerm(funcname,user.split("_")[1],user.split("_")[0],isblack=True)
        if res == False:
            ret += f"用户 {user} 加入函数 {funcname} 黑名单失败\n"
        else:
            ret += f"用户 {user} 加入函数 {funcname} 黑名单成功\n"
    await add_perm_black.finish(ret[:-1])

del_perm_black = on_startswith(msg="删除黑名单",priority=2,rule=is_on,permission=SUPERUSER)
@BH.checker(name="删除黑名单",usage="删除黑名单 函数名 若干用户（(*|@|groupid)_(*|#1|#2|#3|#4|userid)）",intro="从某函数黑名单删除若干用户权限",isAdmin=True)
@del_perm_black.handle()
async def delPermBlackHandle(bot: Bot, event: Event, state: T_State,matcher: Matcher):
    msg = str(event.message).strip()
    msg = msg.split(" ")
    if len(msg) < 3:
        await del_perm_black.finish("参数不够喔。")
    funcname = msg[1]
    users = msg[2:]
    ret = ""
    for user in users:
        if len(user.split("_"))!=2:
            ret += f"用户 {user} 删除函数 {funcname} 黑名单被跳过\n"
            continue
        res = BH.delPerm(funcname,user.split("_")[1],user.split("_")[0],isblack=True)
        if res == False:
            ret += f"用户 {user} 删除函数 {funcname} 黑名单失败\n"
        else:
            ret += f"用户 {user} 删除函数 {funcname} 黑名单成功\n"
    await del_perm_black.finish(ret[:-1])

view_perm = on_startswith(msg="查看权限",priority=2,permission=SUPERUSER,rule=is_on)
@BH.checker(name="查看权限",usage="查看权限 0-1个函数名",intro="查看有权访问某函数的角色列表（不指定函数查询全部）",isAdmin=True)
@view_perm.handle()
async def viewPermHandle(bot: Bot, event: Event, state: T_State,matcher: Matcher):
    msg = str(event.message).strip()
    msg = msg.split(" ")
    if len(msg) > 2:
        await view_perm.finish("参数不对喔。")
    if len(msg) == 1: # 返回全部权限对应
        pairs = BH.perm.select_all_perms()
        buf = "权限如下：\n"
        for item in pairs:
            buf += f"函数名称:{BH.func.get_name_by_id(item[0])} uid:{item[1]} gid:{item[2]}\n"
        await view_perm.finish(buf[:-1])
    funcname = msg[1] # 返回 func 对应权限
    rtn = f'''{funcname}包含的有权限访问角色列表如下：\n'''
    pairs = BH.perm.select_perms_by_func(funcname)
    for item in pairs:
        rtn += f"uid:{item[1]} gid:{item[2]}\n"
    await view_perm.finish(rtn[:-1])

view_perm_black = on_startswith(msg="查看黑名单",priority=2,permission=SUPERUSER,rule=is_on)
@BH.checker(name="查看黑名单",usage="查看黑名单 0-1个函数名",intro="查看黑名单里禁止访问某函数的角色列表（不指定函数查询全部）",isAdmin=True)
@view_perm_black.handle()
async def viewPermBlackHandle(bot: Bot, event: Event, state: T_State,matcher: Matcher):
    msg = str(event.message).strip()
    msg = msg.split(" ")
    if len(msg) > 2:
        await view_perm_black.finish("参数不对喔。")
    if len(msg) == 1: # 返回全部权限对应
        pairs = BH.perm.select_all_perms(isblack=True)
        buf = "黑名单如下：\n"
        for item in pairs:
            buf += f"函数名称:{BH.func.get_name_by_id(item[0])} uid:{item[1]} gid:{item[2]}\n"
        await view_perm_black.finish(buf[:-1])
    funcname = msg[1] # 返回 func 对应权限
    rtn = f'''{funcname}黑名单包含的无权限访问角色列表如下：\n'''
    pairs = BH.perm.select_perms_by_func(funcname,isblack=True)
    for item in pairs:
        rtn += f"uid:{item[1]} gid:{item[2]}\n"
    await view_perm_black.finish(rtn[:-1])

view_func = on_startswith(msg="介绍",priority=2,rule=is_on)
# @perm.register(name="介绍",usage="介绍 0-1个函数名",intro="查看函数用法和功能说明(不指定函数名则查看全部)")
@view_func.handle()
async def viewFuncHandle(bot: Bot, event: Event, state: T_State,matcher: Matcher):
    msg = str(event.message).strip()
    msg = msg.split(" ")
    if msg[0] == "介绍":
        if len(msg) > 2:
            await view_func.finish("参数不对喔。")
        if len(msg) == 1:
            res = BH.func.get_all_func()
            buf = ""
            for item in res:
                buf += f"名称：{item[0]},用法：{item[1]},说明：{item[2]}\n"
            if buf == "":
                await view_func.finish("Σ(っ °Д °;)っ居然一个函数也没有，那我是怎么跑起来的")
            else:
                await view_func.finish(buf[:-1])
        else:
            rawfuncname = msg[1]
            distlis = [[item,EditDist(rawfuncname,item[0])/max(len(rawfuncname),len(item[0]))] for item in BH.func.get_all_func()]
            distlis = [item for item in distlis if item[1]!=1.0]
            distlis.sort(key=lambda x:x[1])
            if len(distlis) == 0:
                await view_func.finish("没有满足要求的函数，试试不加参数看看？")
            else:
                if distlis[0][1] == 0:
                    await view_func.finish(f"名称：{distlis[0][0][0]},用法：{distlis[0][0][1]},说明：{distlis[0][0][2]}")
                else:
                    buf = "没有找到同名函数，找到比较相关的函数如下：\n"
                    for item in distlis[:3]:
                        buf += f"名称：{item[0][0]},用法：{item[0][1]},说明：{item[0][2]}\n"
                    await view_func.finish(buf[:-1])
