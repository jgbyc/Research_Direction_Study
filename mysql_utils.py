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
    
    def getYearSliderRange(self, keywordList):
        keywordSet = '('
        for keyword in keywordList:
            keywordSet += '\'' + keyword +'\'' +','
        keywordSet = keywordSet[:-1] + ')'
        sql = f'''
        SELECT MIN(year), MAX(year)
        FROM countkeyword
        WHERE name in {keywordSet};
        '''
        queryResult = self.query(sql)
        return int(queryResult[0][0]), int(queryResult[0][1])

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
        ORDER BY name, year;
        '''
        return self.query(sql)
        
    def getFaculty(self, queryName, queryPosition, queryEmail, queryPhone, queryUniversityName):
        sql = f'''
        SELECT faculty.id, faculty.name, faculty.position, faculty.research_interest, faculty.email, faculty.phone, faculty.photo_url, university.name
        FROM faculty INNER JOIN university
        ON faculty.university_id = university.id
        WHERE faculty.name LIKE '%{self.xstr(queryName)}%' AND faculty.position LIKE '%{self.xstr(queryPosition)}%'
        AND faculty.email LIKE '%{self.xstr(queryEmail)}%' AND faculty.phone LIKE '%{self.xstr(queryPhone)}%'
        AND university.name LIKE '%{self.xstr(queryUniversityName)}%'
        LIMIT 100;
        '''
        return self.query(sql)
    
    def insertFaculty(self, insertName, insertPosition, insertEmail, insertPhone, insertUniversityName, insertResearchInterest, insertPhotoURL):
        if len(self.getFaculty(insertName, insertPosition, insertEmail, insertPhone, insertUniversityName)) > 0:
            return 'Faculty exist.'

        args = [self.xstr(insertName), self.xstr(insertPosition), self.xstr(insertResearchInterest), self.xstr(insertEmail),
                self.xstr(insertPhone), self.xstr(insertPhotoURL), self.xstr(insertUniversityName)]
        db = mysql.connector.connect(**self.__config)
        cursor = db.cursor()
        try:
            cursor.callproc('updateFaculty', args)
        except:
            db.rollback()
            response = 'Fail to insert.'
        else:
            db.commit()
            response = 'Faculty inserted.'
        finally:
            cursor.close()
            db.close()
            return response
    
    def getPublication(self, queryTitle, queryVenue, queryYear, queryNumOfCitations, facultyIDList):
        if len(facultyIDList) == 0:
            sql = f'''
            SELECT publication.id, publication.title, publication.venue, publication.year, publication.num_citations
            FROM publication
            WHERE publication.title LIKE '%{self.xstr(queryTitle)}%' AND publication.venue LIKE '%{self.xstr(queryVenue)}%'
            AND publication.year LIKE '%{self.xstr(queryYear)}%' AND publication.num_citations LIKE '%{self.xstr(queryNumOfCitations)}%'
            LIMIT 100;
            '''
            return self.query(sql)
        
        facultyIDSet = ''
        for each in facultyIDList:
            facultyIDSet += str(each) + ','
        facultyIDSet = '(' + facultyIDSet[:-1] + ')'
        sql = f'''
        SELECT publication.id, publication.title, publication.venue, publication.year, publication.num_citations
        FROM publication INNER JOIN faculty_publication
        ON publication.id = faculty_publication.publication_id
        WHERE faculty_publication.faculty_id IN {facultyIDSet}
        AND publication.title LIKE '%{self.xstr(queryTitle)}%' AND publication.venue LIKE '%{self.xstr(queryVenue)}%'
        AND publication.year LIKE '%{self.xstr(queryYear)}%' AND publication.num_citations LIKE '%{self.xstr(queryNumOfCitations)}%'
        LIMIT 100;
        '''
        return self.query(sql)
    
    def deletePublication(self, publicationIDList):
        publicationIDSet = ''
        for each in publicationIDList:
            publicationIDSet += str(each) + ','
        publicationIDSet = '(' + publicationIDSet[:-1] + ')'
        sql = f'''
        DELETE FROM publication
        WHERE publication.id IN {publicationIDSet};
        '''
        db = mysql.connector.connect(**self.__config)
        cursor = db.cursor()
        try:
            cursor.execute(sql)
        except:
            db.rollback()
            response = 'Fail to delete'
        else:
            db.commit()
            response = 'Successively deleted'
        finally:
            cursor.close()
            db.close()
            return response
           
    def xstr(self, s):
        return '' if s is None else str(s)

