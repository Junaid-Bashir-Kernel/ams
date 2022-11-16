from flask import Blueprint ,render_template,request ,make_response ,redirect
import datetime
import hashlib
import sqlite3

adminfunction=Blueprint('adminlogin',__name__)


@adminfunction.route("/adminhome",methods=["GET"])
def adminpage():

   return render_template("adminhome.html")


@adminfunction.route("/adminregister",methods=["GET","POST"])
def adminregister():
     connection=sqlite3.connect("project.db")
     cursor=connection.cursor()
    
     if request.method=="POST":
        id=request.form["id"]
        name=request.form["name"]
        password=request.form["password"]
        
        cursor.execute("INSERT INTO Adminn values ('{}','{}','{}');".format(id,name,password))
        connection.commit()
        return "registered"

     return "method not allowed" 


@adminfunction.route("/adminlogin",methods=["POST","GET"])
def adminlogin():
      
      connection=sqlite3.connect("project.db")
      cursor=connection.cursor()
     
      if request.method=="POST":
     
       id=request.form["id"]
       password=request.form["password"]

       cursor.execute("SELECT * from Adminn WHERE id='{}' AND password='{}'".format(id,password))
       result=cursor.fetchone()

       if  result:
           encoded=id.encode("utf-8")
           hashedvalue=hashlib.sha256(encoded)
           hexvalue=hashedvalue.hexdigest()
           response=make_response(redirect("/admin"))
           next=datetime.datetime.today() + datetime. timedelta(days=1)
           response.set_cookie("admintoken",hexvalue,expires=next)
           return response       
       else:
        return "user not found"

      #return render_template("adminsignup.html")
      return "method not allowed"



@adminfunction.route("/admin",methods=["POST","GET"])
def admin():
    #if request.method=="POST":
       connection=sqlite3.connect("project.db")
       cursor=connection.cursor()
       currentuser=""
       token=request.cookies.get("admintoken")
       if token ==None:
          return "unauthenticated"
       cursor.execute("SELECT * FROM Adminn;")
       result=cursor.fetchall()
       for admin in result:
          encoded=admin[0].encode("utf-8")
          hashed=hashlib.sha256(encoded)
          hexvalue=hashed.hexdigest()
          if token == hexvalue:
             currentuser=admin[0]

       studentcolumns=[]
       teachercolumns=[]
       cursor.execute("PRAGMA table_info (student);")
       sresult=cursor.fetchall()
       for  column in sresult:
             if column[1] =="id":
                pass
             else:
               studentcolumns.append(column[1])

       cursor.execute("PRAGMA table_info (teacher) ;")
       tresult=cursor.fetchall()
       for  column in tresult:
             if column[1]=="id":
                pass
             else:  
               teachercolumns.append(column[1])
        
       studentids=[]
       teacherids=[]
       cursor.execute("SELECT id from student;")
       sids=cursor.fetchall()
       for id in sids:
            studentids.append(id[0])
       cursor.execute("SELECT id from teacher")
       tids=cursor.fetchall()
       for id in tids:
            teacherids.append(id[0])

       return render_template("admin.html",user=currentuser,scolumns=studentcolumns,tcolumns=teachercolumns,sids=studentids,tids=teacherids)

      
@adminfunction.route("/addstudent",methods=["GET","POST"])
def addstudent():
       connection=sqlite3.connect("project.db")
       cursor=connection.cursor()
      
       if request.method=="POST":
            id=request.form["id"]
            name=request.form["name"]
            section=request.form["section"]
            password=request.form["password"]
            cursor.execute("SELECT * FROM student WHERE id='{}'".format(id))
            queryresult=cursor.fetchall()
            if len(queryresult) !=0:
               return "student already present"
               
            cursor.execute("INSERT INTO student values ('{}','{}','{}','{}');".format(id,name,password,section))
            connection.commit()
            
            return "added student"
            #return "student added"




@adminfunction.route("/updatestudent",methods=["POST","GET"])
def updatestudent():
      connection=sqlite3.connect("project.db")
      cursor=connection.cursor()
      if request.method=="POST":
         id=request.form["id"]
         column=request.form["column"]
         value=request.form["value"]
         sqlquery="UPDATE student  SET '{}'='{}' WHERE id='{}' ;".format(column,value,id)
         cursor.execute(sqlquery)
         connection.commit()
         
         return "student record updated"


@adminfunction.route("/delstudent",methods=["POST","GET"])
def delete():
     connection=sqlite3.connect("project.db")
     cursor=connection.cursor()
     if request.method=="POST":
         id=request.form["id"]
         cursor.execute("DELETE FROM student WHERE id='{}';".format(id))
         connection.commit()
         return "deleted"







#TEACHER SECTION 

@adminfunction.route("/addteacher",methods=["GET","POST"])
def addteacher():
       connection=sqlite3.connect("project.db")
       cursor=connection.cursor()
      
       if request.method=="POST":
            id=request.form["id"]
            name=request.form["name"]
            section=request.form["section"]
            password=request.form["password"]
            
            cursor.execute("SELECT * FROM teacher WHERE id='{}'".format(id))
            queryresult=cursor.fetchall()
            if len(queryresult) !=0:
               return "lecturer  already present"

            cursor.execute("INSERT INTO student values ('{}','{}','{}','{}');".format(id,name,password,section))
            connection.commit()
            
            return "teacher added"


@adminfunction.route("/updateteacher",methods=["POST","GET"])
def updateteacher():
      connection=sqlite3.connect("project.db")
      cursor=connection.cursor()
      if request.method=="POST":
         id=request.form["id"]
         column=request.form["column"]
         value=request.form["value"]
         sqlquery="UPDATE  teacher SET '{}'='{}' WHERE id='{}' ;".format(column,value,id)
         cursor.execute(sqlquery)
         connection.commit()
         return "updated teacher"

         
@adminfunction.route("/delteacher",methods=["POST","GET"])
def deleteteacher():
     connection=sqlite3.connect("project.db")
     cursor=connection.cursor()
     if request.method=="POST":
         id=request.form["id"]
         cursor.execute("DELETE FROM teacher WHERE id='{}';".format(id))
         connection.commit()
         
         return "deleted teacher"

