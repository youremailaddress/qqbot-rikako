from flask import Flask,render_template,redirect,session,url_for,request
from datetime import timedelta
import base64,json
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.split(os.path.realpath(__file__))[0],os.path.pardir)))
from web.utils.tools import *
import utils.conf.confparser
from my_bot.plugins.checkword.data_source import CWDBH

app = Flask(__name__)
SUPERUSER = os.getenv("SUPER")
app.config['SECRET_KEY'] =  base64.b64decode(os.getenv("SECRET_KEY").encode())
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
passbynav = [("login","people-circle","登录"),("status","speedometer","服务器状态"),("about","chevron-right","关于")]
usernav = [("notice","calendar3","新通知"),("comment","chat-quote-fill","建议&新功能"),("profile","gear-fill","个性设置"),("status","speedometer","服务器状态")]
adminav = [("admin","speedometer2","权限管理"),("analysis","table","行为分析"),("noticeman","collection","通知管理"),("notice","calendar3","新通知"),("comment","chat-quote-fill","建议&新功能"),("profile","gear-fill","个性设置"),("status","speedometer","服务器状态"),("note","toggles2","好友备注")]


@app.route("/",methods=['GET'])
def index():
    if session.get("userid") == None:
        return redirect(url_for('login'))
    else:
        if session.get("userid") == SUPERUSER:
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('profile'))

@app.route("/login",methods=['GET','POST'])
def login():
    if session.get("userid") != None:
        return redirect(url_for("index"))
    if request.method == "GET":
        ckw = generate_random_str()
        session["checkword"] = ckw
        return render_template("login.html",nav=passbynav,uid="QQ号码",uname="未登录",checkword=ckw)
    if request.method == "POST":
        if not request.form.get("user") or not request.form.get("checkword") or not session.get("checkword"):
            return {"msg":"QQ号码或校验码未填写,或cookie存在问题"}
        if not request.form.get("user").isdigit():
            return {"msg":"QQ号码不正确!"}
        if len(request.form.get("checkword")) != 8 or session.get("checkword") != request.form.get("checkword"):
            return {"msg":"校验码被篡改!"}
        # todo 判断是否在数据库里 如果不在 返回错误消息 如果在 跳到指定页面并按要求记录session
        if CWDBH.check_checkword(request.form.get("user"),request.form.get("checkword")):
            session["userid"] = request.form.get("user")
            session["username"] = getNickName(session.get("userid"))
            if request.form.get("remember") == "1":
                session.permanent = True
            return redirect(url_for("index"))
        else:
            return {"msg":"校验码不正确或已过期!"}

@app.route("/admin",methods=["GET"])
def admin():
    if session.get("userid") != SUPERUSER:
        return redirect(url_for('profile'))
    return render_template("admin.html",nav=adminav,uid=session.get("userid"),uname=session.get("username"),permnow="",blacknow="",func=[],group=[],friend=[])

@app.route("/profile",methods=["GET"])
def profile():
    if session.get("userid") == None:
        return redirect(url_for('login'))

@app.route("/about",methods=["GET"])
def about():
    if session.get("userid") == None:
        return render_template("about.html",nav=passbynav,uid="QQ号码",uname="未登录")
    elif session.get("userid") != SUPERUSER:
        return render_template("about.html",nav=usernav,uid=session.get("userid"),uname=session.get("username"))
    else:
        return render_template("about.html",nav=adminav,uid=session.get("userid"),uname=session.get("username"))

@app.route("/analysis",methods=["GET"])
def analysis():
    if session.get("userid") != SUPERUSER:
        return redirect(url_for('profile')) 

@app.route("/comment",methods=["GET"])
def comment():
    if session.get("userid") == None:
        return redirect(url_for('login'))

@app.route("/note",methods=["GET"])
def note():
    if session.get("userid") != SUPERUSER:
        return redirect(url_for('profile'))

@app.route("/notice",methods=["GET"])
def notice():
    if session.get("userid") == None:
        return redirect(url_for('login'))

@app.route("/noticeman",methods=["GET"])
def noticeman():
    if session.get("userid") != SUPERUSER:
        return redirect(url_for('profile'))

@app.route("/status",methods=["GET"])
def status():
    vres = getVPSStatus()
    nres = getNonebotStatus()
    cres = getCQHttpStatus()
    if session.get("userid") == None:
        return render_template("status.html",nav=passbynav,uid="QQ号码",uname="未登录",cpupersent=vres[0],vmempersent=vres[1],swappersent=vres[2],nres=nres,cres=cres)
    elif session.get("userid") != SUPERUSER:
        return render_template("status.html",nav=usernav,uid=session.get("userid"),uname=getNickName(session.get("userid")),cpupersent=vres[0],vmempersent=vres[1],swappersent=vres[2],nres=nres,cres=cres)
    else:
        return render_template("status.html",nav=adminav,uid=session.get("userid"),uname=getNickName(session.get("userid")),cpupersent=vres[0],vmempersent=vres[1],swappersent=vres[2],nres=nres,cres=cres)

if __name__ == "__main__":
    # app.run("0.0.0.0",port=443,ssl_context=('/etc/letsencrypt/live/love.yushanruomu.com/fullchain.pem', '/etc/letsencrypt/live/love.yushanruomu.com/privkey.pem'))
    app.run("0.0.0.0",port=9087)