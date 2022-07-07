from nonebot import get_driver
driver = get_driver()
global_config = get_driver().config

from nonebot.matcher import StopPropagation,Matcher
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event,GroupMessageEvent
from nonebot.plugin import on_message, on_command,on_shell_command,get_loaded_plugins,on_startswith
from nonebot.permission import SUPERUSER
from utils.permissionhandler import PermissionHandler
from utils.rolehandler import is_on
# 这个插件由原来 admin 重构而来 含有 function 如下:
# 开关机函数 只有 superuser 才有权限
# 修改权限函数 只有 superuser 才有权限修改权限
# 查看权限函数

shut_down = on_command("关机",aliases={"shut down"},priority=1,permission=SUPERUSER)
@shut_down.handle()
async def shutDownFunc(bot:Bot,event:Event):
    global_config.set_on = False
    await shut_down.finish("Rikako已经关闭啦.")

power_on = on_command('开机',aliases={"power on"},priority=1,permission=SUPERUSER)
@power_on.handle()
async def powerOnHandle(bot: Bot, event: Event):
    if global_config.set_on ==  False:
        global_config.set_on =  True
        await power_on.finish("芜湖开机")
    else:
        await power_on.finish("已经开机了啦")

add_role = on_startswith(msg="addrole",priority=2,rule=is_on,permission=SUPERUSER)
add_role_perm = PermissionHandler("addrole","addrole rolename *userid","添加角色(及用户对应关系)")
@add_role.handle()
async def addRoleHandle(bot: Bot, event: Event):
    msg = str(event.message).strip()
    msg = msg.split(" ")
    if len(msg) < 2:
        await add_role.finish("参数不够喔。用法 addrole rolename *userid")
    else:
        role = msg[1]
        userid = msg[2:]
        sql = '''select role_id from role_table where role_name=?;'''
        roleid = add_role_perm.dbh.getone("role_table",add_role_perm.cfg["role_table"],sql,(role,))
        if roleid == None:
            sql = '''insert into role_table(role_name) values (?);'''
            add_role_perm.dbh.push("role_table",add_role_perm.cfg["role_table"],sql,(role,))
            if userid == []:
                await add_role.finish(f"没有查询到该 role ，判定为新的角色。已经创建了新的空白角色{role}。")
        is_checked = True
        notok = None
        for user in userid:
            if not add_role_perm.checkUserParse(user):
                is_checked = False
                notok = user
                break
        if not is_checked:
            await add_role.finish(f"userid 出错，最早的错误出现在 userid {notok}。检查一下再来喔。")
        for user in userid:
            sql = '''select count(*) from role_user_table,role_table where role_name = ? and role_table.role_id=role_user_table.role_id and user_id=?;'''
            _exists = add_role_perm.dbh.getone("role_user_table",add_role_perm.cfg["role_user_table"],sql,(role,user)) # 查找是否已经存在 role_user 组合
            if _exists == 0:
                sql = '''select role_id from role_table where role_name=?;'''
                roleid = add_role_perm.dbh.getone("role_table",add_role_perm.cfg["role_table"],sql,(role,))
                sql = '''insert into role_user_table(role_id,user_id) values (?,?);'''
                add_role_perm.dbh.push("role_user_table",add_role_perm.cfg["role_user_table"],sql,(roleid,user))
            else:
                pass
        await add_role.finish("成功添加角色及对应 user 规则")

remove_role = on_startswith(msg="removerole",priority=2,permission=SUPERUSER,rule=is_on)
remove_role_perm = PermissionHandler("removerole","removerole rolename *userid","删除角色(及相应用户对应关系[默认所有涉及本角色的数据列！慎重])")
@remove_role.handle()
async def removeRoleHandle(bot: Bot, event: Event):
    msg = str(event.message).strip()
    msg = msg.split(" ")
    if len(msg) < 2:
        await remove_role.finish("参数不够喔。用法 removerole rolename *userid")
    else:
        role = msg[1]
        userid = msg[2:]
        sql = '''select role_id from role_table where role_name=?;'''
        roleid = remove_role_perm.dbh.getone("role_table",remove_role_perm.cfg["role_table"],sql,(role,))
        if roleid == None:
            await remove_role.finish(f"{role}不存在。角色删除失败")
        if userid != []: # userid 不为空，则只删除role_user_table里的对应关系
            is_checked = True
            notok = None
            for user in userid:
                if not remove_role_perm.checkUserParse(user):
                    is_checked = False
                    notok = user
                    break
            if not is_checked:
                await remove_role.finish(f"userid 出错，最早的错误出现在 userid {notok}。检查一下再来喔")
            sql = '''delete from role_user_table where role_id=? and user_id=?'''
            datalis = [(roleid,user) for user in userid]
            remove_role_perm.dbh.pushmany("role_user_table",remove_role_perm.cfg["role_user_table"],sql,datalis)
            await remove_role.finish(f"{role}-{userid}对应关系已经删除")
        else: # userid 为空，则需要删除 role_table/role_user_table/func_role_table/disable_table 对应的role
            sql = '''delete from role_table where role_id=?;'''
            remove_role_perm.dbh.push("role_table",remove_role_perm.cfg["role_table"],sql,(roleid,))
            sql = '''delete from role_user_table where role_id=?;'''
            remove_role_perm.dbh.push("role_user_table",remove_role_perm.cfg["role_user_table"],sql,(roleid,))
            sql = '''delete from func_role_table where role_id=?;'''
            remove_role_perm.dbh.push("func_role_table",remove_role_perm.cfg["func_role_table"],sql,(roleid,))
            sql = '''delete from disable_table where role_id=?;'''
            remove_role_perm.dbh.push("disable_table",remove_role_perm.cfg["disable_table"],sql,(roleid,))
            await remove_role.finish(f"{role}角色删除完毕")

set_perm = on_startswith(msg="setperm",priority=2,permission=SUPERUSER,rule=is_on)
set_perm_perm = PermissionHandler("setperm","setperm funcname ?rolename","赋予rolename(至少一个) funcname 的使用权限")
@set_perm.handle()
async def setPermHandle(bot: Bot, event: Event):
    msg = str(event.message).strip()
    msg = msg.split(" ")
    if len(msg) < 3:
        await set_perm.finish("参数不够喔。用法 setperm funcname ?rolename")
    else:
        funcname = msg[1]
        rolename = msg[2:]
        # 获取 func_id
        sql = '''select func_id from func_table where func_name = ?;'''
        func_id = set_perm_perm.dbh.getone("func_table",remove_role_perm.cfg["func_table"],sql,(funcname,))
        if func_id == None:
            await set_perm.finish(f"{funcname}不存在，你是不是记错了？")
        else:
            # 先判断是不是都是合法role
            rolelis = []
            for index in range(len(rolename)):
                sql = '''select role_id from role_table where role_name=?;'''
                role_id = set_perm_perm.dbh.getone("role_table",set_perm_perm.cfg["role_table"],sql,(rolename[index],))
                if role_id == None:
                    break
                rolelis.append(role_id)
            if (len(rolename)!=len(rolelis)):
                await set_perm.finish(f"{rolename[len(rolelis)]}角色不存在，要先添加角色才能设置权限哦")
            # 对这些合法 role 进行权限赋予
            # 赋予之前检查是否已有权限
            for role in rolelis:
                sql = '''select count(*) from func_role_table where func_id=? and role_id=?;'''
                exists_ = set_perm_perm.dbh.getone("func_role_table",set_perm_perm.cfg["func_role_table"],sql,(func_id,role))
                if exists_ == 0:
                    sql = '''insert into func_role_table(func_id,role_id) values (?,?);'''
                    set_perm_perm.dbh.push("func_role_table",set_perm_perm.cfg["func_role_table"],sql,(func_id,role))
                else:
                    pass
            await set_perm.finish(f"成功为函数{funcname}添加{rolename}组的权限！")

revoke_perm = on_startswith(msg="revokeperm",priority=2,permission=SUPERUSER,rule=is_on)
revoke_perm_perm = PermissionHandler("revokeperm","revokeperm funcname *rolename","撤销rolename(如果没有指定则撤销全部！慎重) funcname 的使用权限")
@revoke_perm.handle()
async def revokePermHandle(bot: Bot, event: Event):
    msg = str(event.message).strip()
    msg = msg.split(" ")
    if len(msg) < 2:
        await revoke_perm.finish("参数不够喔。用法 revokeperm funcname *rolename")
    else:
        funcname = msg[1]
        rolename = msg[2:]
        # 获取 func_id
        sql = '''select func_id from func_table where func_name = ?;'''
        func_id = revoke_perm_perm.dbh.getone("func_table",revoke_perm_perm.cfg["func_table"],sql,(funcname,))
        if func_id == None:
            await revoke_perm.finish(f"{funcname}不存在，你是不是记错了？")
        if rolename !=[]: # 不是全部删除
            rolelis = []
            for index in range(len(rolename)):
                sql = '''select role_id from role_table where role_name=?;'''
                role_id = revoke_perm_perm.dbh.getone("role_table",revoke_perm_perm.cfg["role_table"],sql,(rolename[index],))
                if role_id == None:
                    break
                rolelis.append(role_id)
            if (len(rolename)!=len(rolelis)):
                await revoke_perm.finish(f"{rolename[len(rolelis)]}角色不存在，要先添加角色才能撤销权限哦")
            sql = '''delete from func_role_table where func_id=? and role_id=?'''
            datalis = [(func_id,role) for role in rolelis]
            revoke_perm_perm.dbh.pushmany("func_role_table",revoke_perm_perm.cfg["func_role_table"],sql,datalis)
            await revoke_perm.finish(f"{rolename}对{funcname}的权限已被撤销。")
        else:
            sql = '''delete from func_role_table where func_id=?;'''
            revoke_perm_perm.dbh.push("func_role_table",revoke_perm_perm.cfg["func_role_table"],sql,(func_id,))
            await revoke_perm.finish(f"所有访问{funcname}的权限角色已被撤销。")

view_role = on_startswith(msg="viewrole",priority=2,permission=SUPERUSER,rule=is_on)
view_role_perm = PermissionHandler("viewrole","viewrole rolename","查看 rolename 对应的 user")
@view_role.handle()
async def viewRoleHandle(bot: Bot, event: Event):
    msg = str(event.message).strip()
    msg = msg.split(" ")
    if len(msg) != 2:
        await view_role.finish("参数不对喔。用法 viewrole rolename")
    else:
        rolename = msg[1]
        rtn = f'''{rolename}包含的用户如下：\n'''
        sql = '''select user_id from role_table,role_user_table where role_table.role_id=role_user_table.role_id and role_name=?;'''
        userid = view_role_perm.dbh.getmany("role_table",view_role_perm.cfg["role_table"],sql,(rolename,))
        for user in userid:
            rtn += f'''用户规则:{user[0]}\n'''
        await view_role.finish(rtn)

view_perm = on_startswith(msg="viewperm",priority=2,permission=SUPERUSER,rule=is_on)
view_perm_perm = PermissionHandler("viewperm","viewperm funcname","查看 funcname 对应的有权限的 role")
@view_perm.handle()
async def viewPermHandle(bot: Bot, event: Event):
    msg = str(event.message).strip()
    msg = msg.split(" ")
    if len(msg) != 2:
        await view_perm.finish("参数不对喔。用法 viewperm funcname")
    else:
        funcname = msg[1]
        rtn = f'''{funcname}包含的有权限访问角色列表如下：\n'''
        sql = '''select role_name from role_table,func_role_table,func_table where func_name=? and func_table.func_id=func_role_table.func_id and func_role_table.role_id=role_table.role_id;'''
        role_name = view_perm_perm.dbh.getmany("func_table",view_perm_perm.cfg["func_table"],sql,(funcname,))
        for role in role_name:
            rtn += f"角色名：{role[0]}"
        await view_perm.finish(rtn)

view_black = on_startswith(msg="viewblack",priority=2,permission=SUPERUSER,rule=is_on)
view_black_perm = PermissionHandler("viewblack","viewblack funcname","查看黑名单里 funcname 对应的 role")
@view_black.handle()
async def viewBlackHandle(bot: Bot, event: Event):
    msg = str(event.message).strip()
    msg = msg.split(" ")
    if len(msg)!=2:
        await view_black.finish("参数不对喔。用法 viewblack funcname")
    else:
        funcname = msg[1]
        rtn = f'''黑名单里{funcname}对应的角色有：\n'''
        sql = '''select role_name from disable_table,func_table,role_table where func_name=? and func_table.func_id=disable_table.func_id and disable_table.role_id=role_table.role_id;'''
        rolename = view_black_perm.dbh.getmany("disable_table",view_black_perm.cfg["disable_table"],sql,(funcname,))
        for role in rolename:
            rtn += f"角色名：{role[0]}"
        await view_black.finish(rtn)

add_black = on_startswith(msg="addblack",priority=2,permission=SUPERUSER,rule=is_on)
add_black_perm = PermissionHandler("addblack","addblack funcname ?rolename","添加黑名单里 funcname 对应的 rolename(至少一个)")
@add_black.handle()
async def addBlackHandle(bot: Bot, event: Event):
    msg = str(event.message).strip()
    msg = msg.split(" ")
    if len(msg) < 3:
        await add_black.finish("参数不对喔。用法 addblack funcname ?rolename")
    else:
        funcname = msg[1]
        rolename = msg[2:]
        sql = '''select func_id from func_table where func_name = ?;'''
        func_id = add_black_perm.dbh.getone("func_table",remove_role_perm.cfg["func_table"],sql,(funcname,))
        if func_id == None:
            await add_black.finish(f"{funcname}不存在，你是不是记错了？")
        rolelis = []
        for index in range(len(rolename)):
            sql = '''select role_id from role_table where role_name=?;'''
            role_id = add_black_perm.dbh.getone("role_table",add_black_perm.cfg["role_table"],sql,(rolename[index],))
            if role_id == None:
                break
            rolelis.append(role_id)
        if (len(rolename)!=len(rolelis)):
            await add_black.finish(f"{rolename[len(rolelis)]}角色不存在，要先添加角色才能加入黑名单哦")
        # 对这些合法 role 进行权限赋予
        # 赋予之前检查是否已有权限
        for role in rolelis:
            sql = '''select count(*) from disable_table where func_id=? and role_id=?;'''
            exists_ = set_perm_perm.dbh.getone("disable_table",set_perm_perm.cfg["disable_table"],sql,(func_id,role))
            if exists_ == 0:
                sql = '''insert into disable_table(func_id,role_id) values (?,?);'''
                set_perm_perm.dbh.push("disable_table",set_perm_perm.cfg["disable_table"],sql,(func_id,role))
            else:
                pass
        await set_perm.finish(f"成功将{rolename}加入函数{funcname}的黑名单！")

revoke_black = on_startswith(msg="revokeblack",priority=2,permission=SUPERUSER,rule=is_on)
revoke_black_perm = PermissionHandler("revokeblack","revokeblack funcname *rolename","移除黑名单里 funcname 对应的 rolename(默认全部，慎重！)")
@revoke_black.handle()
async def revokeBlackHandle(bot: Bot, event: Event):
    msg = str(event.message).strip()
    msg = msg.split(" ")
    if len(msg) < 2:
        await revoke_black.finish("参数不够喔。用法 revokeblack funcname *rolename")
    else:
        funcname = msg[1]
        rolename = msg[2:]
        # 获取 func_id
        sql = '''select func_id from func_table where func_name = ?;'''
        func_id = revoke_black_perm.dbh.getone("func_table",revoke_black_perm.cfg["func_table"],sql,(funcname,))
        if func_id == None:
            await revoke_black.finish(f"{funcname}不存在，你是不是记错了？")
        if rolename !=[]: # 不是全部删除
            rolelis = []
            for index in range(len(rolename)):
                sql = '''select role_id from role_table where role_name=?;'''
                role_id = revoke_black_perm.dbh.getone("role_table",revoke_black_perm.cfg["role_table"],sql,(rolename[index],))
                if role_id == None:
                    break
                rolelis.append(role_id)
            if (len(rolename)!=len(rolelis)):
                await revoke_black.finish(f"{rolename[len(rolelis)]}角色不存在，要先添加角色才能加入黑名单哦")
            sql = '''delete from disable_table where func_id=? and role_id=?'''
            datalis = [(func_id,role) for role in rolelis]
            revoke_black_perm.dbh.pushmany("disable_table",revoke_black_perm.cfg["disable_table"],sql,datalis)
            await revoke_black.finish(f"{rolename}对{funcname}的权限已被撤销。")
        else:
            sql = '''delete from disable_table where func_id=?;'''
            revoke_black_perm.dbh.push("disable_table",revoke_black_perm.cfg["disable_table"],sql,(func_id,))
            await revoke_black.finish(f"所有访问{funcname}的权限角色已被撤销。")