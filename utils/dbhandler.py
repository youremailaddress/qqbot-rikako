import sqlite3
class SelfDefineDBHandler():
    def __init__(self,path):
        self.path = path
    
    def _ensureTable(self,tablename,config):
        '''
        确保操作之前数据库和表存在、结构完整。如果不完整则补全。
        '''
        db = sqlite3.connect(self.path,check_same_thread=False)
        cursor = db.cursor()
        try:
            cursor.execute('''select count(*) from %s;'''%(tablename))
        except:
            sql = '''CREATE TABLE %s(''' % tablename
            for col,tp,restrict in config:
                sql += "%s  %s  %s," % (col,tp,restrict)
            sql = sql[:-1]
            sql += ");"
            print(sql)
            cursor.execute(sql)
            db.commit()
        return db,cursor

    