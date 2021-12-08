from flask import Flask, render_template, request, redirect
import psycopg2

name = ""
login = ""
password = ""

app = Flask(__name__)

@app.route('/login/', methods=['POST', 'GET'])
def login():
    global name
    global login
    global password
    conn = psycopg2.connect(database="login",
                            user="postgres",
                            password="1234",
                            host="localhost",
                            port="5432")
    cursor = conn.cursor()
    if request.method == 'POST':
        if request.form.get("login"):
            login = request.form.get('login')
            password = request.form.get('password')
            if (login == ""):
                conn.close()
                return 'Вы не ввели логин'
            if (password == ""):
                conn.close()
                return 'Вы не ввели пароль'

            try:
                cursor.execute("SELECT * FROM users WHERE login=%s AND password=%s", (str(login), str(password)))
                records = list(cursor.fetchall())
                name = records[0][1]
                login = records[0][2]
                password = records[0][3]
                conn.close()
                return redirect("/account/")
            except:
                conn.close()
                return 'Вы не зарегистрированны'
        elif request.form.get("registration"):
            conn.close()
            return redirect("/registration/")
    conn.close()
    return render_template('login.html')


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    global name
    global login
    global password
    conn = psycopg2.connect(database="login",
                            user="postgres",
                            password="1234",
                            host="localhost",
                            port="5432")
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        if (name == ""):
            conn.close()
            return 'Вы не ввели имя'
        if (login == ""):
            conn.close()
            return 'Вы не ввели логин'
        if (password == ""):
            conn.close()
            return 'Вы не ввели пароль'
        try:
            cursor.execute("INSERT INTO users (name,login,password) values (%s,%s,%s)", (str(name), str(login), str(password)))
            conn.commit()
            conn.close()
            return redirect("/account/")
        except:
            conn.close()
            return 'Регистрация не удалась'
    conn.close()
    return render_template('registration.html')


@app.route('/account/', methods=['POST', 'GET'])
def account():
    global name
    global login
    global password
    conn = psycopg2.connect(database="login",
                            user="postgres",
                            password="1234",
                            host="localhost",
                            port="5432")
    cursor = conn.cursor()
    if request.method == 'POST':
        return redirect("/login/")
    conn.close()
    return render_template('account.html', full_name=str(name), full_login=str(login), full_password=str(password))

