import neo4j
import pandas as pd

class neo4j_utils:
    def __init__(self) -> None:
        self.driver = neo4j.GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "test_root"))
    
    def top_faculty(self):
        with self.driver.session() as session:
            result = session.run("MATCH (f:Faculty) RETURN f.name AS name, f.numCitations AS numCitations ORDER BY numCitations DESC LIMIT 25")
            df = pd.DataFrame(result.data())
            return df