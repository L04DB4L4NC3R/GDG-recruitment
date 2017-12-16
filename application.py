from flask import Flask, render_template,url_for,request,session,redirect
from cs50 import SQL
from helpers import login_required

db=SQL("sqlite:///gdg.db")
app=Flask(__name__)
app.secret_key="shhh"


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/home')
def home():
    if session.get("reg_no"):
        return render_template("home.html")
    return redirect(url_for('index'))


@app.route("/register",methods=["POST"])
def register():
    if request.form["name"]=="" or request.form["reg_no"]=="" or request.form["password"]=="":
        return render_template("failure.html")
    
    data=db.execute("SELECT * FROM students")
    for i in data:
        if request.form["name"] == i["name"] or request.form["reg_no"]== i["reg_no"]:
            return "Someone with these details already exists, please enter unique details"
        
    db.execute("INSERT INTO students (name,reg_no,password) VALUES (:name , :reg_no,:p)"\
               ,name=request.form["name"],reg_no=request.form["reg_no"],p=request.form["password"])
    return render_template("success.html")



@app.route("/login",methods=["GET","POST"])
def login():    
    session.clear()
    if request.method=="POST":
        
        if request.form["name"]=="" or request.form["password"]=="":
            return render_template("failure.html")
        
        password=db.execute("SELECT password FROM students WHERE name=:name",name=request.form["name"])
    
        if not len(password) or password[0]["password"]!=request.form["password"]:
            return "Invalid password"
        
        reg=db.execute("SELECT reg_no FROM students WHERE name=:name",name=request.form["name"])
        session['reg_no']=reg[0]["reg_no"]
        
        return redirect(url_for('home'))
    else:
        return render_template("login.html")

        
@app.route("/unregister",methods=["GET","POST"])
#@login_required
def unregister():
    if request.method=="POST":
        data=db.execute("SELECT * FROM students WHERE reg_no=:r",r=request.form['reg_no'])
        if len(data)<1:
            return "No user of this registration number found"
        if request.form["reg_no"]!=session["reg_no"]:
            return "You dont have the permission to unregister for this registration number"
        
        db.execute("DELETE FROM students WHERE reg_no = :reg_no",reg_no=session['reg_no'])
        return render_template("unregistered.html", reg_no=request.form['reg_no'])
    else:
        return render_template("unregister.html")

@app.route('/photos')
def photos():
    data=[]
    fetch=db.execute("SELECT link FROM cache WHERE reg_no=:r",r=session.get("reg_no"))
    for i in fetch:
        data.append(i["link"])
    return render_template("photos.html",data=data)

@app.route("/users")
def users():
    data=db.execute("SELECT name,reg_no FROM students")
    return render_template("users.html",data=data)


@app.route("/logout",methods=["GET","POST"])
#@login_required
def logout():
    session.clear()
    return render_template("logout.html")


@app.route("/page",methods=["GET","POST"])
#@login_required
def page():
    if request.method=="POST":
        data=[]
        if request.form["link"]=="":
            return render_template("failure.html")
        db.execute("INSERT INTO cache VALUES (:r,:l)",r=session.get("reg_no"),l=request.form["link"])
        fetch=db.execute("SELECT link FROM cache WHERE reg_no=:r",r=session.get("reg_no"))
        for i in fetch:
            data.append(i["link"])
        return render_template("photos.html",data=data)
    else:
        return render_template("page.html")

@app.route('/rmv')
def rmv():
    val=request.args.get("val")
    db.execute("DELETE FROM cache WHERE link = :ln",ln=val)
    return redirect(url_for('photos'))
    
if __name__=="__main__":
    Flask.DEBUG=1
    Flask.run(app)


    
