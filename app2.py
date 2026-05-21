from flask import Flask, jsonify , request
import sqlite3
import hashlib

app = Flask(__name__)


def db_connection():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/init", methods=["GET"])
def init_db():
    conn = db_connection()
    conn.execute("""CREATE TABLE IF NOT EXISTS students(
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 Roll_no INTEGER NOT NULL
                 )
                """)
    
    conn.commit()
    conn.close()

    return jsonify({"message": "Database created successfully"})

@app.route("/")
def home():
    return jsonify("Homepage")

@app.route("/students")
def students():
    conn = db_connection()
    rows =  conn.execute(" SELECT * FROM students").fetchall()
    conn.close()
    return jsonify([dict(row) for row  in rows])

@app.route("/students",methods=["POST"])
def add_students():
    data = request.get_json()
    name = data.get("name")
    Roll_no = data.get("Roll_no")

    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, Roll_no) VALUES( ?,? )" , (name , Roll_no))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    new_student = {"id" : new_id,
                   "name": name , 
                   "Roll_no" : Roll_no}
    

    return jsonify({"student added sucessfully" : new_student} ), 201

if __name__ =="__main__":   
    app.run(debug=True)
