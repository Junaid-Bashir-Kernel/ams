from flask import Flask, render_template 
from studentlogin import studentloginfunction
from lecturerlogin import lecturerloginfunction
from attendance import studentattendancefunction
from admin import adminfunction
app=Flask(__name__)


app.register_blueprint(studentloginfunction)
app.register_blueprint(lecturerloginfunction)
app.register_blueprint(studentattendancefunction)
app.register_blueprint(adminfunction)



@app.route("/")
def home():

   return render_template("home.html")



if __name__=="__main__":
    app.run("0.0.0.0",port=80,debug=True)