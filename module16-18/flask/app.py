# reference:took help from friend and google
import time, calendar 
from flask import Flask, render_template,request, redirect, url_for, session, jsonify
from flask_session import Session
from register import *
from sqlalchemy import and_


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

url = "postgresql://gzpzugqvthxgkl:ea358a4d34b4c30c51f6441bdfce62aa4d5f314443895dd899881e6083742072@ec2-52-21-252-142.compute-1.amazonaws.com:5432/d4q27kdo396jvi"
app.config["SQLALCHEMY_DATABASE_URI"] = url

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
details=[]


def main():
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

def shelf_user(name):
  c = []
  a = Shelf.query.filter(Shelf.name == name).all()
  for i in a:
    b = Books.query.filter(Books.isbn == i.isbn).first()
    c.append(b)
  return c

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
        return render_template("search_new.html", name=name)
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
    password=request.form.get('password')
    timestamp = calendar.timegm(time.gmtime())



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
    return render_template("result.html", books = books)
  elif(author):
    books = Books.query.filter(Books.author.ilike("%"+author+"%")).all()
    return render_template("result.html", books = books)
  elif(isbn):
    books = Books.query.filter(Books.isbn.ilike("%"+isbn+"%")).all()
    return render_template("result.html", books = books)
  return render_template("result.html", books = [])

@app.route("/book/<isbn>", methods=["POST","get"])
def book(isbn):
    # session['isbn'] = isbn

    book = Books.query.get(isbn)

    if book is None:
        return render_template("error.html", message="Book not found"), 404
    if "a2s" in request.form:
      item = Shelf(isbn = isbn, name = session['username'])
      db.session.add(item)
      db.session.commit()


    if "add" in request.form or "update" in request.form:
        comment = request.form.get("comment")
        rating = request.form.get("star")
        review_check = Review.query.filter_by(isbn=isbn, name=session['username']).first()
        if review_check is None:
            review_add = Review(name=session['username'], isbn=isbn, review=comment, rating=rating)
            db.session.add(review_add)
            db.session.commit()
        else:
            review_check.review = comment
            review_check.rating = rating
        db.session.commit()
        review_check = Review.query.filter_by(isbn=isbn).all()
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

@app.route("/shelf", methods=["POST","get"])
def shelf():
  if 'username' in session:
    if 'remove' in request.form:
      isbn = request.form.get("book_isbn")
      print(isbn)
      Shelf.query.filter(Shelf.isbn == isbn, Shelf.name == session['username']).delete()
      db.session.commit()

    b1 = shelf_user(session['username'])
    return render_template("shelf.html", books = b1)
  
  



















































#need to pass searchby and search as parameters as JSON
@app.route("/api/search", methods=["POST"])
def apisearch():
  data=request.json
  searchby=(data["searchby"]).lower()
  search=data["search"]
  list=[]
  if searchby == "isbn":
    list=Books.query.filter(Books.isbn.ilike("%"+search+"%")).all()
  elif searchby == "title":
    list=Books.query.filter(Books.title.ilike("%"+search+"%")).all()  
  else:
    list=Books.query.filter(Books.author.ilike("%"+search+"%")).all()
  if len(list)==0:
    return jsonify({"Message":"No Results"}),400

  isbns=[]
  titles=[]
  authors=[]
  years=[]
  for i in list:
    isbns.append(i.isbn)
    titles.append(i.title)
    authors.append(i.author)
    years.append(i.year)

  dict={
    "isbns":isbns,
    "titles":titles,
    "authors":authors,
    "years":years
  }

  return jsonify(dict),200

@app.route("/api/book", methods=["POST"])
def apiBook():
    data = request.json
    isbn = data["isbn"]
    bookObj = Books.query.filter_by(isbn=isbn).first()
    list = Review.query.filter_by(isbn=isbn).all()
    dict = {}
    if len(list) == 0:
        dict["users"] = ["-"]
        dict["ratings"] = [0]
        dict["reviews"] = ["-"]
        return jsonify(dict), 200
    users = []
    ratings = []
    reviews = []
    for i in list:
        users.append(i.name)
        ratings.append(i.rating)
        reviews.append(i.review)
    dict = {"users" : users,
    "ratings" : ratings,
    "reviews" : reviews}
    return jsonify(dict), 200


@app.route("/api/submit_review", methods=["POST"])
def apiSubmitReview():
  data = request.json
  user = data["user"]
  isbn = data["isbn"]
  rating = data["rating"]
  review = data["review"]
  obj = Review.query.filter(and_(Review.isbn == isbn, Review.name == user)).first()
  if obj is not None:
    return jsonify({"Message":"Already reviewed for this book"})
  else:
    reviewObj = Review(isbn=isbn, name=user, rating=rating, review=review)
    db.session.add(reviewObj)
    db.session.flush()
    db.session.commit()
    return jsonify({"Message":"Successfully Reviewed"})


