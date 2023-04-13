USE academicworld;

-- Create index to expedite keywordCountByYear query
CREATE INDEX keywordNameIndex
ON keyword (name);

-- Create the view for keywordCountByYear(self, keywordList, yearRange)
CREATE VIEW countkeyword AS
SELECT pub.title, pub.year, keyword.name
FROM keyword
INNER JOIN publication_keyword pub_key ON pub_key.keyword_id = keyword.id
INNER JOIN publication pub ON pub.id = pub_key.publication_id;