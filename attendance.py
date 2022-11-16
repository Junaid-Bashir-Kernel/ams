from unicodedata import name
from flask import Blueprint ,render_template,request ,make_response ,redirect,jsonify,send_file
import datetime
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

studentattendancefunction=Blueprint('studentattendance',__name__)
#now=datetime.datetime.now()
today=datetime.date.today()


@studentattendancefunction.route("/attendance",methods=['GET',"POST"])
def attendance():
      
      if request.method=="POST":
            
            data=request.form["attendance"]
            classs=request.form["class"]
            student=request.form["student"]
            section=request.form["section"]
            
      
      
            with open('Attendance.csv', 'r+') as f:
                        myDataList = f.readlines()
                        nameList = []
                        attendance_record_time=[]
                        for line in myDataList:
                              entry = line.split(',')
                              print(entry)
                              print(attendance_record_time)
                              nameList.append(entry[0])
                              attendance_record_time.append(entry[3])

                        if student not in nameList and today not in  attendance_record_time:
                                
                                     f.writelines(f'\n{student},{classs},{data},{today},{section}')

                        elif student in nameList and  today in attendance_record_time:
                                   return "attendance already marked"
                         
            return  jsonify("attendance marked for {}".format(today))


@studentattendancefunction.route("/update",methods=["POST","GET"])
def update():
      if request.method=="POST":
            updatedvalue=request.form["updatedvalue"]
            student=request.form["student"]
            df = pd.read_csv("attendance.csv", index_col="id")
            df.at[student, 'attendance'] =updatedvalue

            df = df.reset_index()
            df.to_csv("attendance.csv", index=False)
            response=make_response(render_template("lecturer.html" ,done="yes"))
            return response



@studentattendancefunction.route("/delete",methods=["POST","GET"])
def delete():
      if request.method=="POST":
         student=request.form["student"]
         df = pd.read_csv('attendance.csv')
# pick the rows with ID=1946 or 2001
         df = df[~df.id.isin([student])]
# if you want to do the opposite, then use the negation operator (~), that is,
# df[~df.ID.isin([1946, 2001])]
# Write the updated DataFrame into employees.csv'.
         
         df.to_csv('attendance.csv', index=False)
         
      response=make_response(render_template("lecturer.html" ,done="yes"))
      return response



@studentattendancefunction.route("/report",methods=["POST","GET"])
def record():
                
                absent_n=0
                present_n=0
               
                if request.method=="POST":
                        givendate=request.form["date"]
                
                        with open("attendance.csv","r") as attendance_csv:
                                lines=attendance_csv.readlines()
                                for line in lines:
                                     if  givendate in line:
                                          if "present" in line:
                                                present_n+=1
                                          elif "absent" in  line:
                                                 absent_n+=1

                fig=plt.figure(figsize=(4,2) ,dpi=200)
                y = np.array([absent_n,present_n])
                mylabels = ["Absent", "Present"]
                plt.pie(y, labels = mylabels,autopct='%1.2f%%')
                plt.legend()
                fig.savefig("1.png")
                #plt.show()
                #response=make_response(redirect("/lecturer"))
                #response.headers.set("content-disposition","attachment;filename='report.png'")
                #return response
                return send_file("./1.png" ,as_attachment=True)
                        
                   

@studentattendancefunction.route("/getattendance",methods=["POST","GET"])
def getattendance():
      if request.method=="POST":
         id=request.form["id"]
         date=request.form["date"]
         section=request.form["section"]

         with open("attendance.csv","r+") as attendance_csv:
              lines=attendance_csv.readlines()
              for line in lines:
                   if id in line and date in line and section in line:
                        return jsonify({"attendance":line})
                      