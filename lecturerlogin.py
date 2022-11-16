from flask import Blueprint ,render_template,request ,make_response ,redirect
import datetime
import hashlib
import sqlite3


lecturerloginfunction=Blueprint('lecturerlogin',__name__)



@lecturerloginfunction.route("/lecturer",methods=["POST","GET"])
def lecturer():
    connection=sqlite3.connect("project.db")
    cursor=connection.cursor()

    cook=request.cookies.get("lectoken")
    currentuser=""
    if cook ==None:
         return "not authenticated"

    cursor.execute("SELECT * FROM teacher;")
    result=cursor.fetchall()

    for user in result:
           encodedstring=user[0].encode("utf-8")
           hashedvalue=hashlib.sha256(encodedstring)
           hashedhex=hashedvalue.hexdigest()
           if cook == hashedhex:
              currentuser=user[0]
    students=[]      
    names=[]    
    cursor.execute("SELECT * FROM student;")
    studentresult=cursor.fetchall()
    for student  in studentresult:
         
         students.append(student[0])    
         names.append(student[1])


    classes=[
        {
            "class":"python",
             "timing":"03",
             "section":"D2104",
             "teacherid":"1333"

        },
        {
            "class":"data structures",
             "timing":"10",
             "section":"D2104",
             "teacherid":"1333"

        }
    ]
    classesfiltered=[]
    #cursor.execute("SELECT id  from teacher WHERE id='{}'".format(currentuser))
    #id_result=cursor.fetchall()

    for obj in classes:
        #for ids in id_result:
            if obj["teacherid"]==currentuser:
                classesfiltered.append(obj)
    print(classesfiltered)

    return render_template("lecturer.html", user=currentuser,names=names,classes=classesfiltered,students=students)



@lecturerloginfunction.route("/lecturerlogin",methods=["GET","POST"])
def lecturerloginn():
     connection=sqlite3.connect("project.db")
     cursor=connection.cursor()

     if request.method=="POST":
       id=request.form["id"]
       password=request.form["password"]
       cursor.execute("SELECT * FROM  teacher  WHERE id='{}' AND password='{}';".format(id,password))
       result=cursor.fetchone()
       if result:
                
                encodedstring=id.encode("utf-8")
                hashedname=hashlib.sha256(encodedstring)
                hexvalue=hashedname.hexdigest()
                response=make_response(redirect("/lecturer"))
                next=datetime.datetime.today() + datetime. timedelta(days=1)
                response.set_cookie("lectoken",hexvalue,expires=next)
                return response
       else :
                return "user not found"

     return "method not allowed"


