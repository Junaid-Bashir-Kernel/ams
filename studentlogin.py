from ctypes import ArgumentError
from flask import Blueprint ,render_template,request ,make_response ,redirect
import datetime
import hashlib
import sqlite3
import pandas as pd


studentloginfunction=Blueprint('studentlogin',__name__)


@studentloginfunction.route("/student",methods=["POST","GET"])
def student():
    connection=sqlite3.connect("project.db")
    cursor=connection.cursor()
    
    cook=request.cookies.get("studenttoken")
    currentuser=""
    if cook ==None:
        return "user not authenticated"

    cursor.execute("SELECT * FROM student ;")
    result=cursor.fetchall()

    for user in result:
        encodedstring=user[0].encode("utf-8")
        hashedvalue=hashlib.sha256(encodedstring)
        hashedhex=hashedvalue.hexdigest()
        if cook == hashedhex:
            currentuser=user[0]
       
    #with open("attendance.csv">'r') as attendance:
            #data=attendance.readlines()
            #print(type(data))
    arr=[]       
    attendance_string=""
    with open('Attendance.csv', 'r') as f:
                        myDataList = f.readlines()
                        print(myDataList)
                        for line in myDataList:
                              if currentuser in line:
                                     attendance_string=line
                                     arr.append(attendance_string)
    
    return render_template("student.html", user=currentuser,attendance=arr)





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
                next=datetime.datetime.today() + datetime.timedelta(days=1)
                response.set_cookie("studenttoken",hexvalue,expires=next)
                return response
       else:
                return "user not found"
     
     return "method not allowed"

    