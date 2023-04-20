from flask import Flask, render_template, request, redirect,url_for
import Clase as c

username = None

def insert_into_tabel(venit, tinta, procent_tinta,categorii,procent_categorii,valoare_categorii,cheltuieli):
    print("Inserare venit si tinta")
    c.insertVenitTinta(venit, tinta, procent_tinta,categorii,procent_categorii,valoare_categorii,cheltuieli)
    
def login(email,password):
    print("Incercare de logare pentru: " + email + " - " + password)
    
    user = c.IsLoginValid(email, password)
    #ok = (user != None)
    return user


app = Flask(__name__)

@app.route("/home", methods = ['POST','GET'])
def DisplayHomePage():
    if request.method == 'POST':
        print("DisplayHomePage")
        print(request.form)
        email = request.form['email']
        password = request.form['password']
        user = login(email, password)
        ok = (user != None)
        if ok == True:
            print("Login ok pentru: ", user.Nume + ' ' + user.Prenume)
            username = user.Prenume
            return redirect("meniu?username=" + username)
        else:
            print("Login failed")
           
    return render_template("Autentificare.html")

@app.route("/meniu", methods = ['POST','GET'])
def meniu():
    print("DisplayMeniuPage")
    user = request.args.get('username')
    return render_template("Meniu.html",username=user)

@app.route('/info',methods = ['POST','GET'])
def DisplayInfo():
    print("DisplayInfo")
    return render_template("Info.html")

@app.route('/intro',methods = ['POST','GET'])
def DisplayIntroducereDate():
    print("DisplayIntroducereDate")
    if request.method == 'POST':
        #print(request.form)
        venit_din_html = request.form['venit']
        tinta_din_html = request.form['tinta']
        procent_tinta_din_html = request.form['procent_tinta']
        categorii_din_html = request.form['categorii']
        procent_categorii_din_html = request.form['procent_categorii']
        valoare_categorii_din_html = request.form['valoare_categorii']
        cheltuieli_din_html = request.form['cheltuieli']
        #....
        
        insert_into_tabel(venit_din_html,tinta_din_html, procent_tinta_din_html,categorii_din_html,procent_categorii_din_html,valoare_categorii_din_html,cheltuieli_din_html)
        
    return render_template("IntroducereDate.html")
    

@app.route('/rezultate',methods = ['POST','GET'])
def DisplayRezultate():
    print("DisplayRezultate")
    return render_template("Rezultate.html")

@app.route('/concluzii',methods = ['POST','GET'])
def DisplayConcluzii():
    print("DisplayConcluzii")
    return render_template("Concluzii.html")

app.run(port=5000)

