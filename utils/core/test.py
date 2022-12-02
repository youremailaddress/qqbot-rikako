if __name__ == "__main__":
    import sys
    sys.path.append("/home/wuhan/workdir/qqbot-rikako/")
    from utils.core.db.confdb import ConfigDB
    from utils.core.db.funcdb import FunctionDB
    from utils.core.db.permdb import PermissionDB
    from utils.core.db.timerdb import TimerDB

    conf = ConfigDB()
    func = FunctionDB()
    perm = PermissionDB()
    timer = TimerDB()
    # 测试 FunctionDB
    print(func.add_func("测试1","test intro","test changed!",istimer=False,paramstring="{'test':123}"))
    print(func.add_func("测试2","test intro","test usage",istimer=True,paramstring="{'another':234}"))
    print(func.select_func_by_name("测试1"))
    print(func.select_func_by_name("测试3"))
    print(func.get_id_by_name("测试1"))
    print(func.get_id_by_name("测试3"))
    print(func.get_name_by_id("测试3"))
    print(func.get_name_by_id("1"))
    print(func.get_name_by_id(1))
    print(func.select_func_by_id("1"))
    print(func.select_func_by_id(1))
    # 测试 PermissionDB
    print(perm.add_perm(1,"182930291","*"))
    print(perm.add_perm(2,"@","*"))
    print(perm.add_perm(1,"*","#1",isblack=True))
    print(perm.select_all_perms())
    print(perm.select_all_perms(isblack=True))
    print(perm.del_perm(1,"182930291","#1"))
    print(perm.del_perm(1,"182930291","*"))
    print(perm.select_all_perms())
    print(perm.select_perms_by_func("测试2"))
    print("Config")
    # 测试 ConfigDB
    print(conf.add_conf(1,"123213123","{'asdas':12312}"))
    print(conf.add_conf(1,"126728381","{'asdas':12312}"))
    print(conf.add_conf(1,"123213123","{'asdas':12312asd}"))
    print(conf.add_conf(1,"123213123","{'asdas':12312asdasd}"))
    print(conf.add_conf(2,"123213123","{'sadaf':asfdsdfs}"))
    print(conf.get_main_conf(1,"123213123"))
    print(conf.unset_main_conf(1))
    print(conf.set_main_conf(1))
    print(conf.get_user_conf("1278317238"))
    print(conf.get_user_conf("123213123"))
    print(conf.get_user_func_conf(1,"123213123"))
    print(conf.get_user_func_conf(1,"1231431241"))
    print(conf.del_conf(6))
    print(conf.get_user_func_conf(1,"123213123"))
    print(conf.get_conf_by_id(1))
    print("Timer")
    # 测试 TimerDB                   
    print(timer.add_timer(1,"127364782",'712862389',127838271,1226371827,3))
    print(timer.select_timer_by_id(1))
    print(timer.select_timer_by_user("127364782"))
    print(timer.select_timer_by_name("测试1"))
    print(timer.del_timer_by_id(1))
    print(timer.select_timer_by_user("127364782"))
    