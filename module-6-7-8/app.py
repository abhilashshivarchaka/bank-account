# reference:took help from friend
import time, calendar 
from flask import Flask, render_template,request
from register import *
app = Flask(__name__)

url = "postgresql://wneikukvxiklfw:fca01fd28e4d7932baecaad12a31853270a74f5fc84104bdd2e3de36e1c07313@ec2-52-23-45-36.compute-1.amazonaws.com:5432/dcjjpgnuo8crp1"


app.config["SQLALCHEMY_DATABASE_URI"] = url

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
details=[]


def main():
    print("hello")
    db.create_all()
with app.app_context():
    main()

# if __name__ == '__main__':
# 	with app.app_context():
# 		main()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/admin")
def admin():
  return render_template("admin.html", details=details)

@app.route("/signup", methods=["POST","get"])
def signup():
  error=None
  success=None
  if "Login" in request.form:
    name=request.form.get('name')
    email=request.form.get('email')
    password=request.form.get('password')
    if (name,password) in ((item[0], item[2] ) for item in details):
        return render_template("index.html", name=name)
    elif (name) in  ((item[0] ) for item in details):
        error="wrong password"
        msg="enter correct details"
        return render_template("signup.html",error=error, msg=msg)
    else:
        error="please register"
        msg="enter details"
        return render_template("signup.html",error=error, msg=msg)


  elif "Register" in request.form:
    d=[]  
    name=request.form.get('name')
    email=request.form.get('email')
    password=request.form.get('password')
    password2=request.form.get('Cpassword')
    timestamp = calendar.timegm(time.gmtime())


    print(name)

    if len(name)<6:
      error ="Uname should have atleast of 6 characters"
    elif len(password)<5:
      error ="password should have atleast of 5 characters"
    elif (password!=password2):
      error="password not matched"
    else:
        d.append(name)
        d.append(email)
        d.append(password)
        details.append(d)
        success="Account Created Successfully"  + name
        user=Users(name=name, password=password,timestamp=timestamp)
        db.session.add(user)
        db.session.commit()
        print(success)
    return render_template("signup.html", error=error, msg=success)
  else:
    return render_template("signup.html", error=error, msg=success)


