from xml.sax.saxutils import prepare_input_source
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

@app.route('/kopya/<pk>')
def kopyaGor(pk):
    result_set = db.execute("SELECT * FROM kitapkopyasi where kitapno=%s",pk)  
    return render_template('kitapkopya.html',pk=pk,kopyalar=result_set)

@app.route('/oduncalma/<pk1>/<pk2>')
def updateGet(pk1,pk2):
    result_set = db.execute("SELECT * FROM kitapkopyasi where kitapno=%s and kopyakitapno=%s",pk1,pk2)  
    #return render_template('kitapkopya.html',pk1=pk1,pk2=pk2,kopyalar=result_set)
    return render_template('kitapkopya.html',pk1=pk1,pk2=pk2,kopyalar=result_set)

@app.route('/oduncalma/<pk1>/<pk2>',methods=['POST'])
def odunc(pk1,pk2):
    result_set = db.execute("SELECT * FROM kitapkopyasi where kitapno=%s and kopyakitapno=%s",pk1,pk2)  
    #return render_template('kitapkopya.html',pk1=pk1,pk2=pk2,kopyalar=result_set)
    altarih=request.form['altarih']
    print(altarih)
    return render_template('kitapkopya.html',pk1=pk1,pk2=pk2,kopyalar=result_set)


