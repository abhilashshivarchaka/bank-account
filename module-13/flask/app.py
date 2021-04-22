import time, calendar 
from flask import Flask, render_template,request, redirect, url_for, session
from flask_session import Session
from register import *

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
url="postgresql://wneikukvxiklfw:fca01fd28e4d7932baecaad12a31853270a74f5fc84104bdd2e3de36e1c07313@ec2-52-23-45-36.compute-1.amazonaws.com:5432/dcjjpgnuo8crp1"




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
    password=request.form.get('password')
    if (name,password) in ((item[0], item[1] ) for item in details):
        session['username'] = name
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
    password=request.form.get('password')
    timestamp = calendar.timegm(time.gmtime())


    print(name)

    if len(name)<1:
      error ="Uname should have atleast of 1 characters"
    elif len(password)<1:
      error ="password should have atleast of 1 characters"
    
    else:
        d.append(name)
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

    if "add" in request.form or "update" in request.form:
        comment = request.form.get("comment")
        rating = int(request.form.get("rating"))
        # print(comment, rating)
        print(session['username'])
        review_check = Review.query.filter_by(isbn=isbn, name=session['username']).first()
        print(review_check)
        if review_check is None:
            review_add = Review(name=session['username'], isbn=isbn, review=comment, rating=rating)
            db.session.add(review_add)
            db.session.commit()
            # review_check = Review.query.filter_by(isbn=isbn, name=session['username']).first()
        else:
            review_check.review = comment
            review_check.rating = rating
        db.session.commit()
        review_check = Review.query.filter_by(isbn=isbn).all()
        # user_review = [comment for comment in review_check if comment.name == session['username']]
        user_review = review_check
        if session['username'] in (x.name for x in user_review):
          flag = True
          return render_template("review.html", book=book, review_check=review_check, user_review=user_review, flag=flag)
        else:
          flag = False
          return render_template("review.html", book=book, review_check=review_check, user_review=user_review, flag=flag)


    review_check = Review.query.filter(Review.isbn==isbn).all()
    # user_review = [comment for comment in review_check if comment.name == session['username']]
    user_review = review_check
    if session['username'] in (x.name for x in user_review):
      flag = True
      return render_template("review.html", book=book, review_check=review_check, user_review=user_review, flag=flag)
    else:
      flag = False
      return render_template("review.html", book=book, review_check=review_check, user_review=user_review, flag=flag)

@app.route("/logout", methods=["POST","get"])
def logout():
  session.pop('username', None)
  return redirect(url_for("signup"))


