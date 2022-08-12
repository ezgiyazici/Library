from flask import Flask
from flask import Flask, render_template, request, redirect, url_for, session
import config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
app = Flask(__name__)


db = create_engine('postgresql://postgres:131799@localhost/Library')
db.execute("select * from kitap")
result_set = db.execute("SELECT * FROM kitap")  
for r in result_set:  
    print(r)
@app.route('/')
def Index():
    return render_template('login.html')

@app.route('/login')
def login():
    return render_template('signup.html')

@app.route('/salonprofile')
def salonprofil():
    result_set = db.execute("SELECT * FROM kitap")  

    return render_template('salonprofil.html',kitaplar=result_set)


