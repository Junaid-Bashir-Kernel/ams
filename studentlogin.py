from flask import Blueprint ,render_template,request ,make_response ,redirect
import datetime
import hashlib
import sqlite3

studentloginfunction=Blueprint('studentlogin',__name__)



@studentloginfunction.route("/student",methods=["POST","GET"])
def student():
    connection=sqlite3.connect("project.db")
    cursor=connection.cursor()
    
    cook=request.cookies.get("studenttoken")
    currentuser=""
    if cook ==None:
        return "fuck you"

    cursor.execute("SELECT * FROM student ;")
    result=cursor.fetchall()

    for user in result:
        encodedstring=user[0].encode("utf-8")
        hashedvalue=hashlib.sha256(encodedstring)
        hashedhex=hashedvalue.hexdigest()
        if cook == hashedhex:
            currentuser=user[0]
        

    return render_template("student.html", user=currentuser)



@studentloginfunction.route("/studentlogin",methods=["GET","POST"])
def studentloginn():
     connection=sqlite3.connect("project.db")
     cursor=connection.cursor()

     if request.method=="POST":
       id=request.form["id"]
       password=request.form["password"]
       cursor.execute("SELECT * FROM student WHERE  id='{}' AND password='{}' ;".format(id,password))
       result=cursor.fetchone()
       if result:
           
                
                encodedstring=id.encode("utf-8")
                hashedname=hashlib.sha256(encodedstring)
                hexvalue=hashedname.hexdigest()
                response=make_response(redirect("/student"))
                next=datetime.datetime.today() + datetime. timedelta(days=1)
                response.set_cookie("studenttoken",hexvalue,expires=next)
                return response

     return "method not allowed"



