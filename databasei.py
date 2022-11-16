import sqlite3
from sqlite3 import Error

try:
  connection=sqlite3.connect("project.db")
  cursor=connection.cursor()
  #cursor.execute("CREATE TABLE student (id text  , name text ,  password text , section text);")
  #cursor.execute("CREATE TABLE  teacher(id text  , name text ,  password text , section text);")
  #cursor.execute("CREATE TABLE  Adminn (id text  ,  name text , password text);")
  #cursor.execute("INSERT INTO  student values('12103916','bashir','pass1','D2104');")
  #cursor.execute("INSERT INTO  teacher values('1333','parul','pass2','D2104');")
  #cursor.execute("INSERT INTO  Adminn  values('001' ,'root2','pass3');")
  #cursor.execute("INSERT INTO  Adminn  values('002' ,'root3','pass3');")
  #connection.commit()
  #cursor.execute("SELECT  * from teacher")
  #result=cursor.fetchall()
  #print(result)
  #for i in result:
       #print(i[0])
       #print(i[0])
  #cursor.execute("PRAGMA table_info (student);")
  #print(cursor.fetchall())
  cursor.execute(" SELECT * FROM student WHERE id='121039144' ")
  queryresult=cursor.fetchall()
  print(len(queryresult))      

except Error as e :
 print(e)
else:
 print("done")

