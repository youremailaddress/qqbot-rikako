import aiosqlite

class HandleDB():
    def __init__(self,path,mode,config):
        '''
        path:路径
        mode:single,eachgroup,eachperson
        config:单表结构 形如 config['column_name'] = type
        表名根据 mode 确定
            如果是 single mode 则 默认表名 default
            如果是 eachgroup mode 则 默认表名 groupid
            如果是 eachperson mode 则 默认表名 personid
        '''
        self.path = path
        assert mode in ["single","eachgroup","eachperson"]
        assert isinstance(config,dict)
        if mode == "single":
            self.mode == 0
        elif mode == "eachgroup":
            self.mode == 1
        else:
            self.mode == 2
        self.config = config
    
    async def _ensureDBAndTable(self,tablename):
        '''
        确保操作之前数据库和表存在、结构完整。如果不完整则补全。
        '''
        db = await aiosqlite.connect(self.path,check_same_thread=false)
        cursor = await db.cursor()
        try:
            await cursor.execute('''select count(*) from ?;''',(tablename,))
        except:
            sql = '''CREATE TABLE %s(''' % tablename
            for k,v in self.config:
                sql += "%s  %s," % (k,v)
            sql += ");"
            await cursor.execute(sql)
            await db.commit()
        return db,cursor