import neo4j
import pandas as pd

class neo4j_utils:
    def __init__(self) -> None:
        self.driver = neo4j.GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
    
    def top_faculty(self):
        with self.driver.session(database="academicworld") as session:
            result = session.run("MATCH (f:FACULTY) RETURN f.name AS name, f.position AS position ORDER BY name LIMIT 25")
            df = pd.DataFrame(result.data())
            return df