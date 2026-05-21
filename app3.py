from flask import Flask, jsonify , request
import sqlite3
import hashlib
from flask import render_template

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
    conn.execute("""CREATE TABLE IF NOT EXISTS users(
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL
                 )
                """)
    
    conn.commit()
    conn.close()

    return jsonify({"message": "Database created successfully"})

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login-page")
def login_page():
    return render_template("login.html")

@app.route("/register-page")
def register_page():
    return render_template("register.html")

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



@app.route("/register" ,methods=["POST"])
def register():
    data = request.get_json()
    username =data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": " username / password not found"}),400
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    try:
        conn = db_connection()
        conn.execute("INSERT INTO users (username,password) VALUES (? ,?)", (username ,hashed_password))
        conn.commit()
        conn.close()
        return jsonify({"messgege": " user registered sucessfully"}),201
    except sqlite3.IntegrityError:
        return jsonify({"error": " username laready exists"}),409


@app.route("/login",methods=["POST"])
def login():
    data = request.get_json()
    username =data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": " username / password not found"}),400
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    conn = db_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password) ).fetchone()
    conn.close()
    if user:
        return jsonify({"message " : f"welcome {username}"})
    else: 
        return jsonify({"error": " Invalid Creadnnetials "}),401
@app.route("/users", methods=["GET"])
def get_users():
    conn = db_connection()

    users = conn.execute("SELECT * FROM students").fetchall()

    result = []

    for user in users:
        result.append(dict(user))

    conn.close()

    return {"users": result}
    

if __name__ =="__main__":   
    app.run(debug=True)
