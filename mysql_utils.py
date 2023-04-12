import mysql.connector

class MysqlDriver:
    def __init__(self):
        self.__db = mysql.connector.connect(host='localhost',
                                  user='root',
                                  password='test_root',
                                  database='academicworld',
                                  port=3306)
    
    def select(self, statement):
        with self.__db.cursor() as cursor:
            cursor.execute(statement)
            data = cursor.fetchall()
            return data
    
    def update(self, statement):
        with self.__db.cursor() as cursor:
            try:
                cursor.execute(statement)
                self.__db.commit()
            except:
                self.__db.rollback()

    def preparedKeywordCount(self, year, keyword):
        with self.__db.cursor(prepared=True) as cursor:
            preparedQuery = f'''
            select count(title) as cnt from countkeyword
            where year = '%s' and name = '%s';
            '''
            parameter = (year, keyword)
            cursor.execute(preparedQuery, params=parameter)
            data = cursor.fetchall()
            return data

