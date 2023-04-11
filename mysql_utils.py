import pymysql

class MysqlDriver:
    def __init__(self):
        self.__db = pymysql.connect(host='localhost',
                                  user='root',
                                  password='test_root',
                                  database='academicworld',
                                  port=3306,
                                  cursorclass=pymysql.cursors.DictCursor)
    
    def select(self, statement):
        cursor = self.__db.cursor()
        cursor.execute(statement)
        data = cursor.fetchall()
        return data
    
    def update(self, statement):
        cursor = self.__db.cursor()
        try:
            cursor.execute(statement)
            self.__db.commit()
        except:
            self.__db.rollback()

