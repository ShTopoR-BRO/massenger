from flask import Flask, render_template,request,redirect, make_response
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
    cursor.execute("SELECT * FROM users WHERE username = %s;",(login,))
    if cursor.fetchall() != []:
        return render_template("error.html")
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
    if db_user == []:
        return "такого пользователя не существует"
    password_db = db_user[0][2]
    check = hash.verify_password(password, password_db)
    if check==True:
        resp = make_response(redirect("/profil"))
        resp.set_cookie('user',str(db_user[0][0]))
        return resp
    else:
        return "неверный пароль"
    
@app.route('/profil')
def profil():
    if request.cookies.get('user') is not None:
        id = int(request.cookies.get('user'))
        cursor.execute("SELECT id_contact FROM contacts WHERE id_user = %s;",(id,))
        all_user_contacts = cursor.fetchall()
        
        result = []
        for i in all_user_contacts:
            print(i)
            cursor.execute("SELECT username FROM users WHERE id = %s;",(i[0],))
            user = cursor.fetchall()
            result.append(user[0])
       
        
       
        return render_template("profil.html", all_conact= result)
    else:
        return "неавторизованный пользватель"

@app.route('/sendMess/<username>',methods=["post"])
def send(username):
    id = random.randint(100, 100000)
    chat=request.form.get("chat")
    if chat == "":
        return render_template("error.html")
    sendler = int(request.cookies.get('user'))
    resept = username
    cursor.execute("SELECT id FROM users WHERE username = %s;",(resept,))
    resept=cursor.fetchall()[0][0]
    cursor.execute("INSERT INTO dialogs VALUES(%s,%s,%s,%s);",(id, sendler, resept, chat))
    connection.commit()
    return redirect("/chat/"+username)


@app.route('/chat/<username>')
def chat(username):
    sendler = int(request.cookies.get('user'))
    cursor.execute("SELECT id FROM users WHERE username = %s;",(username,))
    resept=cursor.fetchall()[0][0]
    cursor.execute("SELECT chat FROM dialogs WHERE (id_res = %s and id_send = %s) or (id_send = %s and id_res = %s);",(sendler,resept,sendler,resept))
    result = cursor.fetchall()
    return render_template("chat.html", all_messages = result,chat_with = username)

    
@app.route('/add_contact', methods=["post"])
def add_contact():
    contact = request.form.get("contact")
    id = random.randint(100, 100000)
    owner = int(request.cookies.get('user'))
    resept = contact
    cursor.execute("SELECT id FROM users WHERE username = %s;",(resept,))
    if  cursor.fetchall() == []:
        return render_template("error.html")
    resept=cursor.fetchall()[0][0]   
    cursor.execute("INSERT INTO contacts VALUES(%s,%s,%s);",(id, owner, resept))
    connection.commit()
    return redirect("/profil")    


@app.route('/exit', methods=["get"])
def exit():
    resp = make_response(redirect("/singIn"))
    resp.set_cookie('user', '', max_age=0)
    return resp













app.run("0.0.0.0")

