USE academicworld;

-- Create index to expedite keywordCountByYear query
CREATE UNIQUE INDEX keywordNameIndex
ON keyword (name);

-- Create the view for keywordCountByYear(self, keywordList, yearRange)
CREATE VIEW countkeyword AS
SELECT pub.title, pub.year, keyword.name
FROM keyword
INNER JOIN publication_keyword pub_key ON pub_key.keyword_id = keyword.id
INNER JOIN publication pub ON pub.id = pub_key.publication_id;

-- Create the Stored Procedure to update the faculty information.
delimiter $$
CREATE PROCEDURE updateFaculty(
IN new_faculty_name varchar(512), new_position varchar(512), new_researchInterest varchar(512), new_email varchar(512), new_phone varchar(512), new_photo varchar(512), new_universityName varchar(512))
BEGIN
    -- Check if the university name exist in the university table 
    DECLARE targetUniversityID INT;
    DECLARE maxUniversityID INT;
    DECLARE maxFacultyID INT;
    SELECT id INTO targetUniversityID from university where name = new_universityName;
    IF targetUniversityID IS NULL
    THEN 
        SELECT MAX(id) INTO maxUniversityID FROM university;
        INSERT INTO university (id, name) VALUES (maxUniversityID + 1, new_universityName);
        SET targetUniversityID = maxUniversityID + 1;
	END IF;
    
	SELECT MAX(id) INTO maxFacultyID FROM faculty;
	INSERT INTO faculty 
	VALUES (maxFacultyID + 1, new_faculty_name, new_position, new_researchInterest, new_email, new_phone, new_photo, targetUniversityID);
END$$
delimiter ;

-- Create Trigger to to make sure the publication_keyword and faculty_publication tutles are deleted before delete faculty tutles.
DELIMITER $$
CREATE TRIGGER deletePublication BEFORE DELETE
ON publication FOR EACH ROW
    BEGIN
        DELETE FROM publication_keyword WHERE publication_keyword.publication_id = OLD.id;
        DELETE FROM faculty_publication WHERE faculty_publication.publication_id = OLD.id;
    END$$
DELIMITER ;