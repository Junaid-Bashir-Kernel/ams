from flask import Blueprint ,render_template,request ,make_response ,redirect,jsonify
studentattendancefunction=Blueprint('studentattendance',__name__)


@studentattendancefunction.route("/attendance",methods=['GET',"POST"])
def attendance():
      data=request.form["attendance"]
      return  jsonify(data)
