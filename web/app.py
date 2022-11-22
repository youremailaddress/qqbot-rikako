from flask import Flask,render_template,redirect,session,url_for,request
from datetime import timedelta
import requests,base64,json
import os
with open(os.path.split(os.path.realpath(__file__))[0]+"/setting.json","r") as f:
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
        a = requests.get(f"https://v.api.aa1.cn/api/qqnicheng/?qq={uid}")
        print(a.text)
        return a.text[5:-10]
    except:
        return "未知"

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
    if request.method == "GET":
        return render_template("login.html",nav=passbynav,uid="QQ号码",uname="未登录")
    if request.method == "POST":
        if not request.form.get("user") or not request.form.get("checkword"):
            return {"msg":"QQ号码或校验码未填写"}
        if not request.form.get("user").isdigit():
            return {"msg":"QQ号码不正确!"}
        if len(request.form.get("checkword"))<5 or len(request.form.get("checkword")) > 8:
            return {"msg":"校验码过短或过长"}
        if not request.form.get("checkword").isalnum():
            return {"msg":"校验码含有特殊字符!"}
        # todo 判断是否在数据库里 如果不在 返回错误消息 如果在 跳到指定页面并按要求记录session
        print(request.form.get("user"),request.form.get("checkword"),request.form.get("remember"))
        return {"status":"OK"}

if __name__ == "__main__":
    # app.run("0.0.0.0",port=443,ssl_context=('/etc/letsencrypt/live/love.yushanruomu.com/fullchain.pem', '/etc/letsencrypt/live/love.yushanruomu.com/privkey.pem'))
    app.run("0.0.0.0",port=9087)