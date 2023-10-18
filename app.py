from flask import Flask, render_template,request
from tongcheng import ly
from xiecheng import xc
from tuniu import tn
import pymysql
app = Flask(__name__)
app.debug=True

@app.route("/",methods=["GET","POST"])
def index():
    return render_template("index.html")

@app.route("/register",methods=["GET", "POST"])#注册界面
def register():
    if request.method=="GET":
        return render_template("register.html")
    if request.method=="POST":
        name = request.form.get("username")
        usernum = request.form.get("usernum")
        password = request.form.get("password")
        conn = pymysql.connect(user="root", password="110110", host="localhost", charset="utf8", port=3306, db="travel",autocommit=True)
        curs = conn.cursor(cursor=pymysql.cursors.DictCursor)
        #sql="DELETE FROM userinformation"
        #curs.execute(sql)
        sql = 'insert into userinformation(nickname, usernum,password) values(%s,%s,%s)'
        curs.execute(sql,(name,usernum,password))
        print("注册成功")
        return render_template("index.html")
@app.route("/login",methods=["GET","POST"])#登陆界面
def login():
    if request.method=="GET":
        return render_template("login.html")
    name=request.form.get("usernum")
    password=request.form.get("password")
    conn = pymysql.connect(user="root", password="110110", host="localhost", charset="utf8", port=3306, db="travel",autocommit=True)
    curses = conn.cursor(cursor=pymysql.cursors.DictCursor)
    curses.execute("select usernum,password from userinformation where usernum=%s",name)
    data = curses.fetchall()
    flag=0
    for i in data:
        if i['usernum']==name and i['password']==password:
            flag=1
            return render_template("index.html")
    if flag==0:
        return render_template("login.html")

@app.route("/london")
def london():
    conn = pymysql.connect(user="root", password="110110", host="localhost", charset="utf8", port=3306, db="travel",autocommit=True)
    curses = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "DELETE FROM london3"
    curses.execute(sql)
    sql = "DELETE FROM london2"
    curses.execute(sql)
    ly('london')
    xc('london')
    tn('london')
    curses.execute("select * from london3 ")
    data1 = curses.fetchall()
    curses.execute("select * from london2 ")
    data2 = curses.fetchall()
    return render_template("place.html",det='伦敦',dete='London',detpic='/static/img/img/伦敦.jpg',data=data1,infor=data2)

@app.route("/newyork")
def newyork():
    conn = pymysql.connect(user="root", password="110110", host="localhost", charset="utf8", port=3306, db="travel",autocommit=True)
    curses = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "DELETE FROM newyork3"
    curses.execute(sql)
    sql = "DELETE FROM newyork2"
    curses.execute(sql)
    ly('newyork')
    xc('newyork')
    tn('newyork')
    curses.execute("select * from newyork3 ")
    # 获取所有的查询结果
    data1 = curses.fetchall()
    curses.execute("select * from newyork2 ")
    data2 = curses.fetchall()

    return render_template("place.html",det='纽约',dete='New York',detpic='/static/img/img/纽约.jpg',data=data1,infor=data2)

@app.route("/sanfrancisco")
def sanfrancisco():
    conn = pymysql.connect(user="root", password="110110", host="localhost", charset="utf8", port=3306, db="travel",autocommit=True)
    curses = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "DELETE FROM sanfrancisco3"
    curses.execute(sql)
    sql = "DELETE FROM sanfrancisco2"
    curses.execute(sql)
    ly('san')
    xc('san')
    tn('san')
    curses.execute("select * from sanfrancisco3")
    # 获取所有的查询结果
    data1 = curses.fetchall()
    curses.execute("select * from sanfrancisco2 ")
    data2 = curses.fetchall()
    return render_template("place.html",det='旧金山',dete='San Francisco',detpic='/static/img/img/旧金山背景.jpg',data=data1,infor=data2)

@app.route("/city/<flag>/<pl>")
def city(flag,pl):
    print((flag,pl))
    if flag=='New York':
        flag='newyork'
    elif flag=='San Francisco':
        flag='sanfrancisco'
    conn = pymysql.connect(user="root", password="110110", host="localhost", charset="utf8", port=3306, db="travel",autocommit=True)
    # 返回字典形式查询结果
    curses = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # 执行sql语句
    curses.execute("select * from %s where name= '%s'"%(flag,pl))
    # 获取所有的查询结果
    data = curses.fetchall()
    passage=data[0]['in_introduction']
    passage1=passage.split("~")
    passage = data[0]['in_time']
    passage2 = passage.split("~")
    passage = data[0]['in_money']
    passage3 = passage.split("~")
    passage = data[0]['in_tips']
    passage4 = passage.split("~")
    return render_template("pass.html",data=data,passage1=passage1,passage2=passage2,passage3=passage3,passage4=passage4)


if __name__ == '__main__':
    #tong()
    app.run(debug=True)
