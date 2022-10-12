from flask import Blueprint ,render_template,request ,make_response ,redirect
import datetime
import hashlib
import sqlite3

adminfunction=Blueprint('adminlogin',__name__)

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


@adminfunction.route("/adminlogin",methods=["GET","POST"])
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

      return render_template("adminsignup.html")



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

       return render_template("admin.html",user=currentuser)

      
    
 