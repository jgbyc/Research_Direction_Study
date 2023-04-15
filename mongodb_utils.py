import pymongo
import pandas as pd

class mongodb_utils:
    
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["academicworld"]
        self.faculty = self.db["faculty"]
        self.publications = self.db["publications"]
    
    def all_faculty(self):
        result = self.faculty.distinct("name")
        df = pd.DataFrame(list(result))
        return df

    def all_publications(self):
        result = self.publications.distinct("title")
        df = pd.DataFrame(list(result))
        return df

    def all_univerisity(self):
        result = self.faculty.distinct("affiliation.name")
        df = pd.DataFrame(list(result))
        return df

    def top_keywords(self):
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
        return df
    
    def top_pub(self, keyword):
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
        return df