import pyodbc 
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=ENG-AENEA;'
                      'Database=FOE;'
                      'UID=mdf-app;'
                      'PWD=kuwuca-34;'
                      )
           
cursor = conn.cursor()

q = cursor.execute("SELECT TOP (1000) [cntPersonnelId]"
               ",[strTitle]"
               ",[strSalutation]"
               ",[strForename]"
               ",[strSurname]"
               ",[strJobTitle]"
               ",[strEmailAddress]"
               ",[lngPersonID]"
               "FROM [FOE].[MDF].[vtblPersonnel]")