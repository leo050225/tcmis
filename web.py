from flask import Flask, render_template, request
from datetime import datetime
app = Flask(__name__)

import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# 判斷是在 Vercel 還是本地
if os.path.exists('serviceAccountKey.json'):
    # 本地環境：讀取檔案
    cred = credentials.Certificate('serviceAccountKey.json')
else:
    # 雲端環境：從環境變數讀取 JSON 字串
    firebase_config = os.getenv('FIREBASE_CONFIG')
    cred_dict = json.loads(firebase_config)
    cred = credentials.Certificate(cred_dict)

firebase_admin.initialize_app(cred)


@app.route("/")
def index():
    homepage = "<h1>施聿觀Python網頁</h1>"
    homepage += "<a href=/mis>MIS</a><br>"
    homepage += "<a href=/today>顯示日期時間</a><br>"
    homepage += "<a href=/welcome?name=施聿觀&dep=資管系>傳送使用者暱稱</a><br>"
    homepage += "<a href=/account>網頁表單傳值</a><br>"
    homepage += "<a href=/math>數學運算</a><br>"
    homepage += "<a href=/about>聿觀簡介網頁</a><br>"
    homepage += "<br><a href=/read>讀取Firestore資料</a><br>"
    return homepage

@app.route("/mis")
def course():
    return "<h1>資訊管理導論</h1>"

@app.route("/today")
def today():
    now = datetime.now()
    return render_template("today.html", datetime = str(now))

@app.route("/welcome", methods=["GET"])
def welcome():
    user = request.values.get("name")
    dep = request.values.get("dep")
    return render_template("welcome.html", name="施聿觀", dep = "資管系")

@app.route("/account", methods=["GET", "POST"])
def account():
    if request.method == "POST":
        user = request.form["user"]
        pwd = request.form["pwd"]
        result = "您輸入的帳號是：" + user + "; 密碼為：" + pwd 
        return result
    else:
        return render_template("account.html")

@app.route("/about")
def about_page():
    # 它會自動去 templates 資料夾找 about.html
    return render_template("about.html")

@app.route("/math", methods=["GET", "POST"])
def math_operation():
    if request.method == "POST":
        try:
            # 從表單取得資料並轉為浮點數（支援小數點）
            x = float(request.form["x"])
            y = float(request.form["y"])
            apt = request.form["apt"]
            result = ""

            # 使用 if...elif...else 替代原本的 match...case
            if apt == "+":
                result = f"{x} + {y} = {x + y}"
            elif apt == "-":
                result = f"{x} - {y} = {x - y}"
            elif apt == "*":
                result = f"{x} * {y} = {x * y}"
            elif apt == "/":
                if y == 0:
                    result = "錯誤：除數不可為 0"
                else:
                    result = f"{x} / {y} = {x / y}"
            else:
                result = "未知的運算符號"
            
            # 回傳計算結果
            return f"<h1>計算結果</h1><p>{result}</p><a href='/math'>回上一頁</a>"
            
        except ValueError:
            return "請輸入正確的數字！<a href='/math'>回上一頁</a>"
            
    # GET 請求時顯示輸入表單
    return render_template("math.html")

@app.route("/read")
def read():
    Result = ""
    db = firestore.client()
    collection_ref = db.collection("靜宜資管")    
    docs = collection_ref.get()    
    for doc in docs:         
        Result += "文件內容：{}".format(doc.to_dict()) + "<br>"    
    return Result

if __name__ == "__main__":
    app.run()
