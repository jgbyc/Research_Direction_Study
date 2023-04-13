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

    def keywordCountByYear(self, keywordList, yearRange):
        with self.__db.cursor() as cursor:
            keywordSet = '('
            for keyword in keywordList:
                keywordSet += '\'' + keyword +'\'' +','
            keywordSet = keywordSet[:-1] + ')'
            # print(keywordSet)
            sql = f'''
            SELECT COUNT(*), year, name 
            FROM countkeyword
            WHERE year >= {yearRange[0]} AND year <= {yearRange[1]} AND name IN {keywordSet}
            GROUP BY name, year
            ORDER BY name, year
            '''
            cursor.execute(sql)
            data = cursor.fetchall()
            # print(data)
            return data

