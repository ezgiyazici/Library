from xml.sax.saxutils import prepare_input_source
from flask import Flask
from flask import Flask, render_template, request, redirect, url_for, session,flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_login import UserMixin, login_user, login_required, logout_user
from flask_login import LoginManager
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash
import _datetime
import time

app = Flask(__name__)

app.secret_key = "secret123"
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)
db = create_engine('postgresql://postgres:131799@localhost/Library')

@app.route('/')
def Index():
    return render_template('login.html')

@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/login', methods=['POST'])
def login_post():
    kullaniciadi = request.form.get('kullaniciadi')
    password = request.form.get('password')

    resultset = db.execute("SELECT * FROM uye WHERE kullaniciadi=%s",kullaniciadi)  
    for r in resultset:  
        kullanıcı=r
    print(kullanıcı)
    result = db.execute("SELECT sifre FROM uye where kullaniciadi=%s",kullaniciadi)  
    for r in result:  
        sifre=r
    if not kullanıcı or str(sifre[0])!=password :
        flash('Giris bilgileriniz yanlis, tekrar deneyiniz.')
        return redirect('/login')
    return render_template('uyeprofil.html',kullanıcı=kullanıcı)

@app.route('/signup',methods=['POST'])
def signup():
    kullaniciAdi=request.form['kullaniciAdi']
    password=request.form['password']
    uyeSoyadi = request.form['uyeSoyadi']
    uyeAdi = request.form['uyeAdi']
    adres = request.form['adres']
    telefon = request.form['telefon']


    db.execute("INSERT INTO uye(uyeadi,uyesoyadi,uyeadresi,uyetelefonu,sifre,kullaniciAdi) VALUES (%s,%s,%s,%s,%s,%s)",uyeAdi,uyeSoyadi,adres,telefon,password,kullaniciAdi)

    return redirect('/login')

@app.route('/signup')
def signupIlk():
    return render_template('signup.html')

@login_manager.user_loader
def load_user(kullaniciadi):
    result_set = db.execute("SELECT * FROM uye where kullaniciadi=%s",kullaniciadi)  
    return result_set

@app.route('/kitap/<pk>')
def kitap(pk):
    result_set = db.execute("SELECT * FROM kitap,yazar where kitap.yazaradi=yazar.yazaradi AND kitap.yazarsoyadi=yazar.yazarsoyadi")
    return render_template('kitap.html',pk=pk,kitaplar=result_set)

@app.route('/oduncalinanlar/<pk>')
def oduncalinanlar(pk):
    result_set = db.execute("SELECT kitap.kitapno,kitapAdi,kopyakitapno,teslimalmatarihi,teslimtarihi FROM kitap,oduncalma where kitap.kitapno=oduncalma.kitapno and uyeno=%s",pk)
    return render_template('oduncalinankitaplar.html',pk=pk,kitaplar=result_set)


@app.route('/cezaalinanlar/<pk>',methods=['POST'])
def cezaalinanlar(pk):

    today = _datetime.date.today().strftime("%Y-%m-%d")
    ceza=db.execute("SELECT * FROM uye,ceza where uye.uyeno=ceza.uyeno and ceza.uyeno=%s",pk)
    count=0
    for v in ceza: 
        count+=1
    if count==0:
        db.execute("INSERT INTO ceza VALUES(0,%s)",pk)
    result_set = db.execute("SELECT kitap.kitapno,kitapAdi,kopyakitapno,teslimalmatarihi,teslimtarihi FROM kitap,oduncalma where kitap.kitapno=oduncalma.kitapno and uyeno=%s",pk)
    ceza=0
    for v in result_set:
        for column, value in v.items():
            if ('{0}'.format(column, value)) == "teslimtarihi":
                if ('{1}'.format(column, value)) < today:
                    ceza+=10
    db.execute("UPDATE ceza SET cezamiktari=%s WHERE uyeno=%s",str(ceza),pk)



    resultset = db.execute("SELECT * FROM ceza WHERE uyeno=%s", pk)

    return render_template('cezaalinankitaplar.html',pk=pk ,kitaplar=resultset)

@app.route('/kopya/<pk1>/<pk2>')
def kopyaGor(pk1,pk2):
    result_set = db.execute("SELECT * FROM kitapkopyasi,kitaplikkonumu where kitapno=%s and kitapkopyasi.konumno=kitaplikkonumu.konumno",pk2) 
    return render_template('kitapkopya.html',pk1=pk1,pk2=pk2,kopyalar=result_set)

@app.route('/oduncalma/<pk1>/<pk2>/<pk3>')
def updateGet(pk1,pk2,pk3):
    result_set = db.execute("SELECT * FROM kitapkopyasi,kitap where kitapkopyasi.kitapno=%s and kitapkopyasi.kopyakitapno=%s and kitap.kitapno=kitapkopyasi.kitapno",pk2,pk3)  
    #return render_template('kitapkopya.html',pk1=pk1,pk2=pk2,kopyalar=result_set)
    return render_template('oduncalma.html',pk1=pk1,pk2=pk2,pk3=pk3,kopyalar=result_set)

@app.route('/oduncalma/<pk1>/<pk2>/<pk3>',methods=['POST'])
def odunc(pk1,pk2,pk3):
    #return render_template('kitapkopya.html',pk1=pk1,pk2=pk2,kopyalar=result_set)
    altarih=request.form['altarih']
    vertarih=request.form['vertarih']
    print(altarih)
    try:
        db.execute("INSERT INTO oduncalma VALUES (%s,%s,%s,%s,%s)",pk1,pk3,pk2,altarih,vertarih)
        flash('Odunc alma basarili.')
    except:
        flash('Odunc alma basarisiz.')
    resultset = db.execute("SELECT * FROM uye WHERE uyeno=%s",pk1)  
    for r in resultset:  
        kullanıcı=r
    return render_template('uyeprofil.html',kullanıcı=kullanıcı)

@app.route('/teslimver/<pk1>/<pk2>/<pk3>')
def teslimet(pk1,pk2,pk3):
    result_set = db.execute("SELECT * FROM kitapkopyasi,kitap where kitapkopyasi.kitapno=%s and kitapkopyasi.kopyakitapno=%s and kitap.kitapno=kitapkopyasi.kitapno",pk2,pk3)  
    #return render_template('kitapkopya.html',pk1=pk1,pk2=pk2,kopyalar=result_set)
    return render_template('teslimverme.html',pk1=pk1,pk2=pk2,pk3=pk3,kopyalar=result_set)

@app.route('/teslimver/<pk1>/<pk2>/<pk3>',methods=['POST'])
def teslim(pk1,pk2,pk3):
    #return render_template('kitapkopya.html',pk1=pk1,pk2=pk2,kopyalar=result_set)
    if request.method=='POST':
        try:
            db.execute("DELETE FROM oduncalma where kitapno=%s and kopyakitapno=%s",pk2,pk3)
            flash('Teslim verme basarili.')
        except:
            flash('Teslim verme basarisiz.')
        resultset = db.execute("SELECT * FROM uye WHERE uyeno=%s",pk1)  
    for r in resultset:  
        kullanıcı=r
    return render_template('uyeprofil.html',kullanıcı=kullanıcı)


