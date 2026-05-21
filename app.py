from flask import Flask, jsonify , request
import sqlite3

app = Flask(__name__)


student = [{
    "id":1 , "name": "dipanshu" , "Roll_no": 38
}]

@app.route("/")
def home():
    return jsonify("Homepage")

@app.route("/students")
def students():
    return jsonify(student)

@app.route("/students",methods=["POST"])
def add_students():
    data = request.get_json()
    new_student = {"id" : len(student)+1,
                   "name": data.get("name") , 
                   "Roll_no" : data.get("Roll_no")}
    
    student.append(new_student)

    return jsonify({"student added sucessfully" : new_student} ), 201

if __name__ =="__main__":   
    app.run(debug=True)
