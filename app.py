from flask import Flask, render_template,request,redirect
import random 
import psycopg2
import hash

app = Flask(__name__)

connection = psycopg2.connect(user="postgres",password="190687",host="localhost",dbname="massenger",port="5432")
 
cursor = connection.cursor() 

@app.route('/')
def hello():
    return render_template("singup.html")




@app.route('/create',methods=["post"])
def create():
    login=request.form.get("login")
    password = request.form.get("password")
    password = hash.hash_password(password) 
    id = random.randint(100, 100000)
    cursor.execute("INSERT INTO users VALUES(%s,%s,%s);",(id, login, password))
    connection.commit()
    
    return redirect("/singIn")


@app.route('/singIn')
def singIn():
    return render_template("singIn.html")


@app.route('/check',methods=["post"])
def check():
    login=request.form.get("login")
    password = request.form.get("password")
    cursor.execute("SELECT * FROM users WHERE username = %s;",(login,))
    db_user = cursor.fetchall()
    password_db = db_user[0][2]
    check = hash.verify_password(password, password_db)
    if check==True:
        return redirect("/profil")
    else:
        return "неверный пароль"
    
@app.route('/profil')
def profil():
    return "this is your profil )))"



















app.run("0.0.0.0")

