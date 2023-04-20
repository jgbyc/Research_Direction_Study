import neo4j
import pandas as pd

class neo4j_utils:
    def __init__(self) -> None:
        self.driver = neo4j.GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
        
    def top_university(self, keyword_list):
        query = """MATCH (K:KEYWORD)<--(P:PUBLICATION)<--(F:FACULTY)-->(I:INSTITUTE)
                WHERE K.name IN $keywords 
                RETURN I.name AS University, count(P) AS Publication_count, I.photoUrl AS Pic
                ORDER BY Publication_count DESC 
                LIMIT 10"""
        with self.driver.session(database="academicworld") as session:
            result = session.run(query,keywords = keyword_list)
            df = pd.DataFrame(result.data())
            return df
    def top_keywords(self):
        query = """MATCH (K:KEYWORD)<--(P:PUBLICATION) 
                RETURN K.name AS name, COUNT(P) AS keyword_count 
                ORDER BY keyword_count DESC 
                LIMIT 20"""
        with self.driver.session(database="academicworld") as session:
            result = session.run(query)
            df = pd.DataFrame(result.data())
            return df
    def top_faculty(self,keyword_list):
        query = """MATCH (K:KEYWORD)<--(P:PUBLICATION)<--(F:FACULTY)-->(I:INSTITUTE)
                WHERE K.name IN $keywords 
                RETURN I.name AS University, count(P) AS Publication_count, F.name as Faculty_name, I.photoUrl AS Pic
                ORDER BY Publication_count DESC 
                LIMIT 30"""
        with self.driver.session(database="academicworld") as session:
            result = session.run(query,keywords = keyword_list)
            df = pd.DataFrame(result.data())
            return df