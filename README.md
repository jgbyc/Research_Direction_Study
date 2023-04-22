# Title
Research Direction Study.
# Purpose
This dash board can assist students to efficiently seek and determine the appropriate research topic. 

The target user should be students or any personnel who has interests on current popular research trends.

# Demo
Give the link to your video demo. Read the video demo section below to understand what contents are expected in your demo.
# Installation
1. Install python package by using the requirements.txt
2. Run SQL script sql_install.sql
# Usage
1. View the top ten research keywords from the Top Keyword widget to get the rough idea of current popular research topics.
2. From the dropdown list, select several interested keywords for further investigation.
3. From the Keyword count trend widget, users can know the number of publications containing the selected keywords per year.
4. From the Top publication by keyword widget, users can view the highest citied publications containing the selected keywords per year.
5. By dragging the double end sliders, users can zoom into the interested time range to better investigate the details of two aforementioned widgets.
6. By using the Treemap Top University/Faculty widget, users can find top universities and corresponding faculties which are most contributing to the selected keywords.
7. If users would like to know the detailed contact information of certain faculties, they can use the widget Faculty's Information to search and filter the faculty information. If searched faculty does not exist in the database, a new faculty record and corresponding university record can be added into the database by clicking on the Button Insert New Faculty.
8. When user check the faculty information, the publication's information widget will be filtered to show only publications written by selected faculties. Also, users may choose to further filter by entering the publications information. By checking the certain publications and click on the Button Delete listed publications, the corresponding publications will be removed from the database.
# Design
This dashboard is layout in rectangular shape. Also, related widgets are bundled and listed together. The layout sequence of widget is intentionally designed to match the expected trends of thoughts and behavior flows. Also, the continuous  color palette is used to make the graph better visualized. 
# Implementation
This dashboard is implemented by using the Dash Plotly framework and Pandas. Multiple callback function is implemented to archive the interactive user interface.
The package mysql-connector-python, pymongo, neo4j are used to setup the corresponding database connections.
# Database Techniques
1. Index. The keyword table column name is indexed to support the query of Keyword count trend widget. Before implementing this index, each query lasts about 5 seconds. By using the index, the query is almost immediate. 
2. View. The countkeyword view is created to simplified the query of Keyword cont trend widget. This view reflects the join results of three tables keyword, publication_keyword, publication. 
3. Stored Procedure. The stored procedure updateFaculty is created to hide the complex sql manipulation from the web server. This stored procedure firstly check if the entered university exists in the university table. If not, a new university record will be created. Then a new faculty will be added into database accordingly. 
4. Trigger. When the user intends to delete one publication record from the database, before deletion happens, the trigger deletePublication will firstly delete the records in the table publication_keyword and table faculty_publication referenced by the foreign key in table publication.

All aforementioned four database techniques are created by running the SQL script file sql_install.sql before start the web server.
# Extra-Credit Capabilities
N/A
# Contributions
The team contains two members.

Kun Ren (kunren2@illinois.edu) implements below functionalities in 35 ~ 40 h:
* mongodb_utils.py
* neo4j_utils.py
* Top Keyword Widget
* Top Publication by Keyword Widget
* The University/Faculty by Keyword Widget
* Demo video

Yichen Bi (ybi5@illinois.edu) implements below functionalities in 35 ~ 40 h:
* mysql_utils.py
* sql_install.sql
* Keyword Count Trend Widget
* Faculty's Information Widget
* Publication's Information Widget
* README.md