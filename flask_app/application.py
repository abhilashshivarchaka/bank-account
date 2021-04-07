from flask import Flask, render_template,request

app=Flask(__name__)

@app.route("/")

def index():
    return render_template("home.html")

@app.route("/hello", methods=["POST"])

def hello():
    name=request.form.get("name")
    return render_template("index.html" , name=name)

