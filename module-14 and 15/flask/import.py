# reference:-took help from friend and google.
import os,csv,sys;
from flask import Flask
from register import *

app=Flask(__name__)


url="postgresql://wneikukvxiklfw:fca01fd28e4d7932baecaad12a31853270a74f5fc84104bdd2e3de36e1c07313@ec2-52-23-45-36.compute-1.amazonaws.com:5432/dcjjpgnuo8crp1"


app.config["SQLALCHEMY_DATABASE_URI"] = url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


def main():
    with app.app_context():
        db.create_all()
        f=open("books.csv")
        reader=csv.reader(f)
        for isbn, title, author, year in reader:
            print(isbn,title,author,year)
            book=Books(isbn=isbn, title=title, author=author, year=year)
            db.session.add(book)
            db.session.commit()
        print("Success", file=sys.stdout)

if __name__ == "__main__":
    main()