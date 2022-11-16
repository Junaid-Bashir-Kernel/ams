
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#from datetime import datetime
import datetime
fig=plt.figure(figsize=(4,2) ,dpi=200)
df=pd.read_csv("attendance.csv",index_col="section")
attendance=df["attendance"]
#section=df["section"]
class_=df["class"]
attendance_n=0
present_n=0

for a in attendance:
    if a=="absent":
       attendance_n+=1
    else:
       present_n+=1

#plt.legend()

#y = np.array([attendance_n,present_n])
#mylabels = ["Absent", "Present"]

#plt.pie(y, labels = mylabels,autopct='%1.2f%%')
#plt.legend()
#title="d2104"
#plt.title(title)
#fig.savefig("1.png")
#plt.show()
#print(df.at[104,"attendance"])
#print(type(df.at[104,"attendance"]))
#print(attendance_n)
#print(present_n)
#plt.pie()
#now=datetime.now()
now=datetime.datetime.now()
print(now)
onlydate=datetime.date.today()
print(onlydate)
#print(datetime.now())
with open("Attendance.csv","r") as ascv:
        lines=ascv.readlines()
        #print(lines)
        for line in lines:
             if "25/10/2000" in line:
                 print(line)
              

       
#print(df.loc[104])