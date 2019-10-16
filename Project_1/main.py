import os
from forms import AddForm,DelForm
from flask import Flask,render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app=Flask(__name__)

app.config["SECRET_KEY"]="mykey"

##############################################
########SQL_DATABASE#########
##############################################

basedir=os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///"+os.path.join(basedir,"data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db=SQLAlchemy(app)
Migrate(app,db)

################################################
######## MODEL ############
################################################

class Examination(db.Model):

    __tablename__= "Exam"

    id=db.Column(db.Integer,primary_key=True)

    name=db.Column(db.Text)

    def __init__(self,name):
        self.name=name

    def __repr__(self):
        return f"Student Name: {self.name}"


###############################################
######## ADD VIEWS ###########
###############################################


@app.route("/")
def index():

    return render_template("home.html")

@app.route("/add",methods=["GET","POST"])
def add():

    form=AddForm()

    if form.validate_on_submit():
        name=form.name.data                   ## Getting name from the form.

        new_name = Examination(name)            ## new_name is the object of the class.
        db.session.add(new_name)              ## We are adding new_name
        db.session.commit()

        return redirect(url_for("list"))

    return render_template("add.html",form=form)

@app.route("/list")
def list():

    students=Examination.query.all()

    return render_template("pup_list.html",students=students)

@app.route("/del",methods=["GET","POST"])
def delete():

    form=DelForm()

    if form.validate_on_submit():

        id=form.id.data

        to_del=Examination.query.get(id)
        db.session.delete(to_del)
        db.session.commit()

        return redirect(url_for("list"))

    return render_template("delete.html",form=form)

