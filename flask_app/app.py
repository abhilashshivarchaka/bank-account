from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, world!"

@app.route('/Abhilash')
def Abhilash():
    return "Hello, Abhilash!"

@app.route('/Abhi')
def Abhi():
    return "Hello, Abhi"
