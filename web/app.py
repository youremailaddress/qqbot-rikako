from flask import Flask,render_template,redirect,session,url_for,request
from datetime import timedelta
import requests,base64,json
import os,sys,random,psutil
sys.path.append(os.path.abspath(os.path.join(os.path.split(os.path.realpath(__file__))[0],os.path.pardir)))
from my_bot.plugins.checkword.data_source import CWDBH
from utils.functions import getDir

with open(getDir("web/setting.json"),"r") as f:
    setting = json.loads(f.read())

app = Flask(__name__)
SUPERUSER = setting["SUPERUSER"]
app.config['SECRET_KEY'] =  base64.b64decode(setting["SECRET_KEY"].encode())
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
passbynav = [("login","people-circle","登录"),("status","speedometer","服务器状态"),("about","chevron-right","关于")]
usernav = [("notice","calendar3","新通知"),("comment","chat-quote-fill","建议&新功能"),("profile","gear-fill","个性设置"),("status","speedometer","服务器状态")]
adminav = [("admin","speedometer2","权限管理"),("analysis","table","行为分析"),("noticeman","collection","通知管理"),("notice","calendar3","新通知"),("comment","chat-quote-fill","建议&新功能"),("profile","gear-fill","个性设置"),("status","speedometer","服务器状态"),("note","toggles2","好友备注")]

def getNickName(uid):
    try:
        a = requests.get(f"https://v.api.aa1.cn/api/qqnicheng/?qq={uid}",timeout=1)
        return a.text[5:-10]
    except:
        return "未知"

def generate_random_str(randomlength=8):
  random_str =''
  base_str ='ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
  length =len(base_str) -1
  for i in range(randomlength):
    random_str +=base_str[random.randint(0, length)]
  return random_str

def getPidbyPort(port):
    net_con = psutil.net_connections()
    for con_info in net_con:
        if con_info.laddr.port == port:
            return con_info.pid
    return False

def getPidbyName(name):
    for proc in psutil.process_iter():
        if proc.name() == name:
            return proc.pid
    return False

def getVPSStatus():
    cpupersent = psutil.cpu_percent()
    vmempersent = psutil.virtual_memory().percent
    swappersent = psutil.swap_memory().percent
    return cpupersent,vmempersent,swappersent

def getNonebotStatus():
    pid = getPidbyPort(23345)
    if pid == False:
        return False
    nbtcpu = psutil.Process(pid).cpu_percent()
    nbtmem = psutil.Process(pid).memory_percent()
    return nbtcpu,nbtmem

def getCQHttpStatus():
    pid = getPidbyName("go-cqhttp")
    if pid == False:
        return False
    cqhcpu = psutil.Process(pid).cpu_percent()
    cqhmem = psutil.Process(pid).memory_percent()
    return cqhcpu,cqhmem

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
    # if session.get("userid") != None:
    #     return redirect(url_for("profile"))
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
            if request.form.get("remember") == "1":
                session.permanent = True
            if session["userid"] == SUPERUSER:
                return redirect(url_for("admin"))
            else:
                return redirect(url_for("profile"))
        else:
            return {"msg":"校验码不正确或已过期!"}

@app.route("/admin",methods=["GET"])
def admin():
    if session.get("userid") != SUPERUSER:
        return redirect(url_for('profile'))

@app.route("/profile",methods=["GET"])
def profile():
    if session.get("userid") == None:
        return redirect(url_for('login'))

@app.route("/about",methods=["GET"])
def about():
    if session.get("userid") == None:
        return render_template("about.html",nav=passbynav,uid="QQ号码",uname="未登录")
    elif session.get("userid") != SUPERUSER:
        return render_template("about.html",nav=usernav,uid=session.get("userid"),uname=getNickName(session.get("userid")))
    else:
        return render_template("about.html",nav=adminav,uid=session.get("userid"),uname=getNickName(session.get("userid")))

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
    nflag = 1
    cflag = 1
    if nres == False:
        nflag = 0
    if cres == False:
        cflag = 0
    if session.get("userid") == None:
        return render_template("status.html",nav=passbynav,uid="QQ号码",uname="未登录",cpupersent=vres[0],vmempersent=vres[1],swappersent=vres[2],nflag=nflag,ncpu=nres[0],nmem=nres[1],cflag=cflag,ccpu=cres[0],cmem=cres[1])
    elif session.get("userid") != SUPERUSER:
        return render_template("status.html",nav=usernav,uid=session.get("userid"),uname=getNickName(session.get("userid")),cpupersent=vres[0],vmempersent=vres[1],swappersent=vres[2],nflag=nflag,ncpu=nres[0],nmem=nres[1],cflag=cflag,ccpu=cres[0],cmem=cres[1])
    else:
        return render_template("status.html",nav=adminav,uid=session.get("userid"),uname=getNickName(session.get("userid")),cpupersent=vres[0],vmempersent=vres[1],swappersent=vres[2],nflag=nflag,ncpu=nres[0],nmem=nres[1],cflag=cflag,ccpu=cres[0],cmem=cres[1])

    

if __name__ == "__main__":
    # app.run("0.0.0.0",port=443,ssl_context=('/etc/letsencrypt/live/love.yushanruomu.com/fullchain.pem', '/etc/letsencrypt/live/love.yushanruomu.com/privkey.pem'))
    app.run("0.0.0.0",port=9087)