import pymongo
import pandas as pd

class mongodb_utils:
    
    def __init__(self):
        self.host = "mongodb://localhost:27017/"
        self.client = None
        self.db = None
        self.faculty = None
        self.publications = None
    
    def connect(self):
        self.client = pymongo.MongoClient(self.host)
        self.db = self.client["academicworld"]
        self.faculty = self.db["faculty"]
        self.publications = self.db["publications"]

    def close(self):
        self.client.close()

    def top_keywords(self):
        self.connect()
        result = self.faculty.aggregate([
            {
                "$group": {
                    "_id": "$affiliation.name",
                    "count": {"$sum": 1}
                }
            },
            {
                "$sort": {"count": -1}
            }
        ])
        df = pd.DataFrame(list(result))
        self.close()
        return df
    
    def top_pub(self, keyword):
        self.connect()
        result = self.publications.aggregate([
            {
                "$match": {
                    "keywords.name": {"$in": keyword}
                }
            },
            {
                "$project": {"_id": 0, "title": 1, "numCitations": 1, "year": 1}
            },
            {
                "$sort": {"numCitations": -1}
            },
            {
                "$limit": 15
            }
        ])
        df = pd.DataFrame(list(result))
        self.close()
        return df