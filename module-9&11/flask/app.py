# reference:took help from friend.
import time, calendar 
from flask import Flask, render_template,request, redirect, url_for
from sqlalchemy import or_, and_
from flask_login import login_manager, login_user, current_user, login_required, logout_user
from register import *

app = Flask(__name__)
url="postgresql://wneikukvxiklfw:fca01fd28e4d7932baecaad12a31853270a74f5fc84104bdd2e3de36e1c07313@ec2-52-23-45-36.compute-1.amazonaws.com:5432/dcjjpgnuo8crp1"

# url = "postgresql://gzpzugqvthxgkl:ea358a4d34b4c30c51f6441bdfce62aa4d5f314443895dd899881e6083742072@ec2-52-21-252-142.compute-1.amazonaws.com:5432/d4q27kdo396jvi"

app.config["SQLALCHEMY_DATABASE_URI"] = url

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
details=[]


def main():
    print("hello world")
    db.create_all()
with app.app_context():
    main()

def getDetailsFromDatabase():
	data = Users.query.order_by(Users.timestamp).all()
	details = []
	for user in data:
		det = []
		n = user.name
		p = user.password
		t = user.timestamp
		det.append(n)
		det.append(p)
		det.append(t)
		details.append(det)
	return details


@app.route("/")
def home():
    # name = "keshava"
    # return render_template("index.html", name = name)
    return redirect(url_for("signup"))

@app.route("/admin")
def admin():
  details = getDetailsFromDatabase()
  return render_template("admin.html", details=details)

@app.route("/signup", methods=["POST","get"])
def signup():
  error=None
  success=None
  details = getDetailsFromDatabase()
  if "Login" in request.form:
    name=request.form.get('name')
    email=request.form.get('email')
    password=request.form.get('password')
    if (name,password) in ((item[0], item[1] ) for item in details):
        return render_template("search.html", name=name)
    elif (name) in  ((item[0] ) for item in details):
        print(name, password)
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

    if len(name)<1:
      error ="Uname should have atleast of 1 characters"
    elif len(password)<1:
      error ="password should have atleast of 1 characters"
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

@app.route("/search", methods=["POST","get"])
def search_ele():
  title = request.form.get("title")
  author = request.form.get("author")
  isbn = request.form.get("isbn")
  if title:
    books = Books.query.filter(Books.title.ilike("%"+title+"%")).all()
  elif(author):
    books = Books.query.filter(Books.author.ilike("%"+author+"%")).all()
  elif(isbn):
    books = Books.query.filter(Books.isbn.ilike("%"+isbn+"%")).all()
  return render_template("result.html", books = books)

@app.route("/book/<isbn>", methods=["POST","get"])
def book(isbn):


    book = Books.query.get(isbn)
    if book is None:
        return render_template("error.html", message="Book not found"), 404

    if request.method == "POST":
        if "add" in request.form or "update" in request.form:
            comment = request.form.get("comment")
            rating = int(request.form.get("rating"))

            if (rating < 1 & rating > 5):
                return render_template("error.html", message="incorrect value")

            review_check = Review.query.filter(and_(Review.isbn==isbn, Review.name==current_user.username)).first()
            if review_check is None:
                review_add = Review(name=current_user.username, isbn=isbn, review=comment, review_numb=rating)
                db.session.add(review_add)

            else:
                review_check.review = comment
                review_check.review_numb = rating
            db.session.commit()

        elif "remove" in request.form:
            review_check = Review.query.filter(and_(Review.isbn==isbn, Review.name==current_user.username)).first()
            db.session.remove(review_check)
            db.session.commit()

    review_check = Review.query.filter(Review.isbn==isbn).all()
    user_review = [comment for comment in review_check if comment.username == current_user.username]
    if user_review:
        user_review=user_review[0]
        review_check.remove(user_review)
    return render_template("review.html", book=book, review_check=review_check, user_review=user_review)



