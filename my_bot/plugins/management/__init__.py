from nonebot import get_driver
from utils.functions import EditDist
from utils.model import *
driver = get_driver()
global_config = get_driver().config
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.plugin import on_message, on_command,on_shell_command,get_loaded_plugins,on_startswith
from nonebot.permission import SUPERUSER
from utils.rolehandler import is_on
from utils.permissionhandler import PMH as perm, User

shut_down = on_command("关机",aliases={"shut down"},priority=1,permission=SUPERUSER)
@perm.register(name="关机",usage="关机/shut down",intro="关闭Rikako，使其只接受开机指令")
@shut_down.handle()
async def shutDownFunc(bot: Bot, event: Event, state: T_State,matcher: Matcher):
    global_config.set_on = False
    await shut_down.finish("Rikako已经关闭啦.")

power_on = on_command('开机',aliases={"power on"},priority=1,permission=SUPERUSER)
@perm.register(name="开机",usage="开机/power on",intro="开启Rikako，使其处于活跃状态")
@power_on.handle()
async def powerOnHandle(bot: Bot, event: Event, state: T_State,matcher: Matcher):
    if global_config.set_on ==  False:
        global_config.set_on =  True
        await power_on.finish("芜湖开机")
    else:
        await power_on.finish("已经开机了啦")

add_role = on_startswith(msg="添加角色",priority=2,rule=is_on,permission=SUPERUSER)
@perm.register(name="添加角色",usage="添加角色 角色名 若干用户（(*|@|groupid)_(*|#1|#2|#3|#4|userid)）",intro="添加若干用户至某角色")
@add_role.handle()
async def addRoleHandle(bot: Bot, event: Event, state: T_State,matcher: Matcher):
    msg = str(event.message).strip()
    msg = msg.split(" ")
    if len(msg) < 2:
        await add_role.finish("参数不够喔。")
    else:
        role = msg[1]
        userid = msg[2:]
        if perm.session.query(Role).filter(Role.name==role).count() == 0:
            newrole = Role(name=role)
            perm.session.add(newrole)
            perm.session.commit()
            await add_role.send(f"创建了新的角色{role}")
        roleid = perm.session.query(Role).filter(Role.name==role).one().id
        for user in userid:
            try:
                perm.session.add(Role_User(rid=roleid,uid=str(User(user))))
                perm.session.commit()
            except:
                perm.session.rollback()
        await add_role.finish(f"成功添加角色{role}及下属用户{userid}")

remove_role = on_startswith(msg="删除角色",priority=2,permission=SUPERUSER,rule=is_on)
@perm.register(name="删除角色",usage="删除角色 角色名 若干用户（(*|@|groupid)_(*|#1|#2|#3|#4|userid)）",intro="删除角色(及相应用户对应关系[默认所有涉及本角色的数据列！慎重])")
@remove_role.handle()
async def removeRoleHandle(bot: Bot, event: Event, state: T_State,matcher: Matcher):
    msg = str(event.message).strip()
    msg = msg.split(" ")
    if len(msg) < 2:
        await remove_role.finish("参数不够喔。")
    else:
        role = msg[1]
        userid = msg[2:]
        if perm.session.query(Role).filter(Role.name==role).count() == 0:
            await remove_role.finish(f"{role}不存在。角色删除失败")
        else:
            roleid = perm.session.query(Role).filter(Role.name==role).one().id
            if userid != []:
                for usr in userid:
                    try:
                        perm.session.query(Role_User).filter(Role_User.rid==roleid,Role_User.uid==str(User(usr))).delete()
                        perm.session.commit()
                    except Exception as e:
                        perm.session.rollback()
                        await remove_role.send(f"{usr}不符合格式要求！从角色{role}删除用户{usr}失败")
                if perm.session.query(Role_User).filter(Role_User.rid==roleid).count() == 0:
                    perm.session.query(Role).filter(Role.id==roleid).delete()
                    perm.session.commit()
                    await remove_role.send(f"检测到{role}已为空角色，将于处理完成后进行清除")
                await remove_role.finish(f"从角色{role}删除用户{userid}")
            else:
                perm.session.query(Role_User).filter(Role_User.rid==roleid).delete()
                perm.session.query(Role).filter(Role.id==roleid).delete()
                perm.session.commit()
                await remove_role.finish(f"删除角色{role}及其全部用户对应关系")

set_perm = on_startswith(msg="添加权限",priority=2,permission=SUPERUSER,rule=is_on)
@perm.register(name="添加权限",usage="添加权限 函数名 （至少一个）角色名",intro="赋予(至少一个)角色名某函数的使用权限")
@set_perm.handle()
async def setPermHandle(bot: Bot, event: Event, state: T_State,matcher: Matcher):
    msg = str(event.message).strip()
    msg = msg.split(" ")
    if len(msg) < 3:
        await set_perm.finish("参数不够喔。")
    else:
        funcname = msg[1]
        rolename = msg[2:]
        if perm.session.query(Func).filter(Func.name==funcname).count() == 0:
            await set_perm.finish(f"函数{funcname}不存在，你是不是记错了？")
        else:
            funcid = perm.session.query(Func).filter(Func.name==funcname).one().id
            for roles in rolename:
                if perm.session.query(Role).filter(Role.name==roles).count() == 0:
                    await set_perm.send(f"角色{roles}不存在，已跳过。请先添加角色后再设置权限")
                    continue
                roid = perm.session.query(Role).filter(Role.name==roles).one().id
                newpair = Func_Role(fid=funcid,rid=roid)
                try:
                    perm.session.add(newpair)
                    perm.session.commit()
                except Exception as e:
                    print(str(e))
                    perm.session.rollback()
            await set_perm.finish(f"成功为函数{funcname}添加{rolename}组的权限！")

revoke_perm = on_startswith(msg="删除权限",priority=2,permission=SUPERUSER,rule=is_on)
@perm.register(name="删除权限",usage="删除权限 函数名 0至多个角色名",intro="撤销某角色（如果没有指定则撤销全部！慎重）对某函数的权限")
@revoke_perm.handle()
async def revokePermHandle(bot: Bot, event: Event, state: T_State,matcher: Matcher):
    msg = str(event.message).strip()
    msg = msg.split(" ")
    if len(msg) < 2:
        await revoke_perm.finish("参数不够喔。")
    else:
        funcname = msg[1]
        rolename = msg[2:]
        # 获取 func_id
        if perm.session.query(Func).filter(Func.name == funcname).count() == 0:
            await revoke_perm.finish(f"函数{funcname}不存在，你是不是记错了？")
        else:
            funcid = perm.session.query(Func).filter(Func.name == funcname).one().id
            if rolename != []:
                for rname in rolename:
                    if perm.session.query(Role).filter(Role.name==rname).count()!=0:
                        rid = perm.session.query(Role).filter(Role.name==rname).one().id
                        try:
                            perm.session.query(Func_Role).filter(Func_Role.fid==funcid,Func_Role.rid==rid).delete()
                        except Exception as e:
                            print(str(e))
                            pass
                        perm.session.commit()
                    else:
                        await revoke_perm.send(f"角色{rname}不存在，已经跳过，你是不是记错了？")
                await revoke_perm.finish(f"角色{rolename}对函数{funcname}的权限已被撤销。")
            else:
                perm.session.query(Func_Role).filter(Func_Role.fid==funcid).delete()
                perm.session.commit()
                await revoke_perm.finish(f"所有访问{funcname}的权限角色已被撤销。")

view_role = on_startswith(msg="查看角色",priority=2,permission=SUPERUSER,rule=is_on)
@perm.register(name="查看角色",usage="查看角色 0-1个角色名",intro="查看角色名对应的用户（不指定角色查询全部）")
@view_role.handle()
async def viewRoleHandle(bot: Bot, event: Event, state: T_State,matcher: Matcher):
    msg = str(event.message).strip()
    msg = msg.split(" ")
    if len(msg) > 2:
        await view_role.finish("参数不对喔。")
    else:
        if len(msg) == 1:
            pairs = perm.session.query(Role_User).join(Role).all()
            buf = "角色如下：\n"
            for item in pairs:
                buf += item.role.name+":"+item.uid+"\n"
            await view_role.finish(buf[:-1])
        else:
            rolename = msg[1]
            rtn = f'''{rolename}包含的用户如下：\n'''
            pairs = perm.session.query(Role_User).join(Role).filter(Role.name==rolename).all()
            for item in pairs:
                rtn += f'''{item.uid}\n'''
            await view_role.finish(rtn[:-1])

view_perm = on_startswith(msg="查看权限",priority=2,permission=SUPERUSER,rule=is_on)
@perm.register(name="查看权限",usage="查看权限 0-1个函数名",intro="查看有权访问某函数的角色列表（不指定函数查询全部）")
@view_perm.handle()
async def viewPermHandle(bot: Bot, event: Event, state: T_State,matcher: Matcher):
    msg = str(event.message).strip()
    msg = msg.split(" ")
    if len(msg) > 2:
        await view_perm.finish("参数不对喔。")
    if len(msg) == 1:
        pairs = perm.session.query(Func.name,Role.name).filter(Func.id==Func_Role.fid,Func_Role.rid==Role.id).all()
        buf = "权限如下：\n"
        for item in pairs:
            buf += item[0] + ":" + item[1] + "\n"
        await view_perm.finish(buf[:-1])
    funcname = msg[1]
    rtn = f'''{funcname}包含的有权限访问角色列表如下：\n'''
    pairs = perm.session.query(Func,Func_Role,Role).filter(Func.name==funcname,Func_Role.fid==Func.id,Func_Role.rid==Role.id).all()
    for item in pairs:
        rtn += f"{item[2].name}\n"
    await view_perm.finish(rtn[:-1])

view_func = on_startswith(msg="介绍",priority=2,rule=is_on)
@perm.register(name="介绍",usage="介绍 0-1个函数名",intro="查看函数用法和功能说明(不指定函数名则查看全部)")
@view_func.handle()
async def viewFuncHandle(bot: Bot, event: Event, state: T_State,matcher: Matcher):
    msg = str(event.message).strip()
    msg = msg.split(" ")
    if msg[0] == "介绍":
        if len(msg) > 2:
            await view_func.finish("参数不对喔。")
        if len(msg) == 1:
            buf = ""
            for func in perm.session.query(Func).all():
                buf += f"名称：{func.name},用法：{func.usage},说明：{func.intro}\n"
            if buf == "":
                await view_func.finish("Σ(っ °Д °;)っ居然一个函数也没有，那我是怎么跑起来的")
            else:
                await view_func.finish(buf[:-1])
        else:
            rawfuncname = msg[1]
            distlis = [[func,EditDist(rawfuncname,func.name)/max(len(rawfuncname),len(func.name))] for func in perm.session.query(Func).all()]
            distlis = [item for item in distlis if item[1]!=1.0]
            distlis.sort(key=lambda x:x[1])
            if len(distlis) == 0:
                await view_func.finish("没有满足要求的函数，试试不加参数看看？")
            else:
                if distlis[0][1] == 0:
                    await view_func.finish(f"名称：{distlis[0][0].name},用法：{distlis[0][0].usage},说明：{distlis[0][0].intro}")
                else:
                    buf = "没有找到同名函数，找到比较相关的函数如下：\n"
                    for item in distlis[:3]:
                        buf += f"名称：{item[0].name},用法：{item[0].usage},说明：{item[0].intro}\n"
                    await view_func.finish(buf[:-1])

# view_black = on_startswith(msg="viewblack",priority=2,permission=SUPERUSER,rule=is_on)
# view_black_perm = PermissionHandler("viewblack","viewblack funcname","查看黑名单里 funcname 对应的 role")
# @view_black.handle()
# async def viewBlackHandle(bot: Bot, event: Event):
#     msg = str(event.message).strip()
#     msg = msg.split(" ")
#     if len(msg)!=2:
#         await view_black.finish("参数不对喔。用法 viewblack funcname")
#     else:
#         funcname = msg[1]
#         rtn = f'''黑名单里{funcname}对应的角色有：\n'''
#         sql = '''select role_name from disable_table,func_table,role_table where func_name=? and func_table.func_id=disable_table.func_id and disable_table.role_id=role_table.role_id;'''
#         rolename = view_black_perm.dbh.getmany("disable_table",view_black_perm.cfg["disable_table"],sql,(funcname,))
#         for role in rolename:
#             rtn += f"角色名：{role[0]}"
#         await view_black.finish(rtn)

# add_black = on_startswith(msg="addblack",priority=2,permission=SUPERUSER,rule=is_on)
# add_black_perm = PermissionHandler("addblack","addblack funcname ?rolename","添加黑名单里 funcname 对应的 rolename(至少一个)")
# @add_black.handle()
# async def addBlackHandle(bot: Bot, event: Event):
#     msg = str(event.message).strip()
#     msg = msg.split(" ")
#     if len(msg) < 3:
#         await add_black.finish("参数不对喔。用法 addblack funcname ?rolename")
#     else:
#         funcname = msg[1]
#         rolename = msg[2:]
#         sql = '''select func_id from func_table where func_name = ?;'''
#         func_id = add_black_perm.dbh.getone("func_table",remove_role_perm.cfg["func_table"],sql,(funcname,))
#         if func_id == None:
#             await add_black.finish(f"{funcname}不存在，你是不是记错了？")
#         rolelis = []
#         for index in range(len(rolename)):
#             sql = '''select role_id from role_table where role_name=?;'''
#             role_id = add_black_perm.dbh.getone("role_table",add_black_perm.cfg["role_table"],sql,(rolename[index],))
#             if role_id == None:
#                 break
#             rolelis.append(role_id)
#         if (len(rolename)!=len(rolelis)):
#             await add_black.finish(f"{rolename[len(rolelis)]}角色不存在，要先添加角色才能加入黑名单哦")
#         # 对这些合法 role 进行权限赋予
#         # 赋予之前检查是否已有权限
#         for role in rolelis:
#             sql = '''select count(*) from disable_table where func_id=? and role_id=?;'''
#             exists_ = set_perm_perm.dbh.getone("disable_table",set_perm_perm.cfg["disable_table"],sql,(func_id,role))
#             if exists_ == 0:
#                 sql = '''insert into disable_table(func_id,role_id) values (?,?);'''
#                 set_perm_perm.dbh.push("disable_table",set_perm_perm.cfg["disable_table"],sql,(func_id,role))
#             else:
#                 pass
#         await set_perm.finish(f"成功将{rolename}加入函数{funcname}的黑名单！")

# revoke_black = on_startswith(msg="revokeblack",priority=2,permission=SUPERUSER,rule=is_on)
# revoke_black_perm = PermissionHandler("revokeblack","revokeblack funcname *rolename","移除黑名单里 funcname 对应的 rolename(默认全部，慎重！)")
# @revoke_black.handle()
# async def revokeBlackHandle(bot: Bot, event: Event):
#     msg = str(event.message).strip()
#     msg = msg.split(" ")
#     if len(msg) < 2:
#         await revoke_black.finish("参数不够喔。用法 revokeblack funcname *rolename")
#     else:
#         funcname = msg[1]
#         rolename = msg[2:]
#         # 获取 func_id
#         sql = '''select func_id from func_table where func_name = ?;'''
#         func_id = revoke_black_perm.dbh.getone("func_table",revoke_black_perm.cfg["func_table"],sql,(funcname,))
#         if func_id == None:
#             await revoke_black.finish(f"{funcname}不存在，你是不是记错了？")
#         if rolename !=[]: # 不是全部删除
#             rolelis = []
#             for index in range(len(rolename)):
#                 sql = '''select role_id from role_table where role_name=?;'''
#                 role_id = revoke_black_perm.dbh.getone("role_table",revoke_black_perm.cfg["role_table"],sql,(rolename[index],))
#                 if role_id == None:
#                     break
#                 rolelis.append(role_id)
#             if (len(rolename)!=len(rolelis)):
#                 await revoke_black.finish(f"{rolename[len(rolelis)]}角色不存在，要先添加角色才能加入黑名单哦")
#             sql = '''delete from disable_table where func_id=? and role_id=?'''
#             datalis = [(func_id,role) for role in rolelis]
#             revoke_black_perm.dbh.pushmany("disable_table",revoke_black_perm.cfg["disable_table"],sql,datalis)
#             await revoke_black.finish(f"{rolename}对{funcname}的权限已被撤销。")
#         else:
#             sql = '''delete from disable_table where func_id=?;'''
#             revoke_black_perm.dbh.push("disable_table",revoke_black_perm.cfg["disable_table"],sql,(func_id,))
#             await revoke_black.finish(f"所有访问{funcname}的权限角色已被撤销。")