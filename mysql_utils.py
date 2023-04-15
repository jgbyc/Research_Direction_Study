import mysql.connector

class MysqlDriver:
    def __init__(self):
        self.__config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'test_root',
            'database': 'academicworld',
            'port': 3306
        }
    
    def query(self, statement):
        db = mysql.connector.connect(**self.__config)
        cursor = db.cursor()
        cursor.execute(statement)
        data = cursor.fetchall()
        cursor.close()
        db.close()
        return data
    
    def update(self, statement):
        db = mysql.connector.connect(**self.__config)
        cursor = db.cursor()
        try:
            cursor.execute(statement)
            db.commit()
        except:
            db.rollback()
        cursor.close()
        db.close()

    def getKeywordCountByYear(self, keywordList, yearRange):
        keywordSet = '('
        for keyword in keywordList:
            keywordSet += '\'' + keyword +'\'' +','
        keywordSet = keywordSet[:-1] + ')'
        sql = f'''
        SELECT COUNT(*), year, name 
        FROM countkeyword
        WHERE year >= {yearRange[0]} AND year <= {yearRange[1]} AND name IN {keywordSet}
        GROUP BY name, year
        ORDER BY name, year
        '''
        return self.query(sql)
        
    def getFaculty(self, queryName, queryPosition, queryEmail, queryPhone, queryUniversityName):
        sql = f'''
        SELECT faculty.name, faculty.position, faculty.email, faculty.phone, university.name
        FROM faculty INNER JOIN university
        ON faculty.university_id = university.id
        WHERE faculty.name LIKE '%{self.xstr(queryName)}%' AND faculty.position LIKE '%{self.xstr(queryPosition)}%'
        AND faculty.email LIKE '%{self.xstr(queryEmail)}%' AND faculty.phone LIKE '%{self.xstr(queryPhone)}%'
        AND university.name LIKE '%{self.xstr(queryUniversityName)}%';
        '''
        return self.query(sql)
    
    def xstr(self, s):
        return '' if s is None else str(s)

