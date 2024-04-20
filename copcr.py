'''from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///C:/Users/hp/Desktop/eco_site/database.db"
app.config['UPLOAD_FOLDER'] = 'static/uploads'


db = SQLAlchemy(app)



class Articles(db.Model):
    id_article = db.Column(db.Integer, primary_key=True)
    create_date = db.Column(db.Date, default=datetime.utcnow)
    name = db.Column(db.Text)
    editor1 = db.Column(db.Text)
    image = db.Column(db.String(150))
    stock = db.Column(db.Integer)
    prix = db.Column(db.Text)
    status = db.Column(db.Text)
    categories = db.Column(db.Text)


class Admin(db.Model):
    id_admin = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    email = db.Column(db.Text)

class Fornisseure(db.Model):
    id_fornisseure = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.Text)
    specialite = db.Column(db.Text)
    adresse = db.Column(db.Text)
    ville = db.Column(db.Text)
    telephone = db.Column(db.Text)
    fax = db.Column(db.Text)

class Contact(db.Model):
    id_message = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.Text)
    email = db.Column(db.Text)
    message = db.Column(db.Text)

class Email(db.Model):
    id_email = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text)


class Purchases(db.Model):
    id_order = db.Column(db.Integer, primary_key=True)
    purchese_id = db.Column(db.Integer, db.ForeignKey('articles.id_article'))
    prenom = db.Column(db.Text)
    nom = db.Column(db.Text)
    adresse = db.Column(db.Text)
    quantite_article = db.Column(db.Integer)
    ville = db.Column(db.Text)
    nom_article = db.Column(db.Text)
    code_postal = db.Column(db.Integer)
    telephone = db.Column(db.Text)
    email = db.Column(db.Text)

def add_order(prenom, nom, adresse, quantite_article, ville, nom_article, code_postal, telephone, email, purchese_id):
    new_order = Purchases(prenom=prenom, nom=nom, adresse=adresse, quantite_article=quantite_article, ville=ville, nom_article=nom_article, code_postal=code_postal, telephone=telephone, email=email, purchese_id=purchese_id)
    db.session.add(new_order)
    db.session.commit()

    article = Articles.query.get(purchese_id)
    article.stock -= quantite_article
    db.session.commit()


def addarticle(name, editor1, prix, stock, image_name, status, categories):
    new_article = Articles(name=name, stock=stock, editor1=editor1, prix=prix, image=image_name, status=status,categories=categories)

    db.session.add(new_article)
    db.session.commit()


def addfournisseur(nom, specialite, adresse, ville, telephone, fax):
    new_fournisseur = Fornisseure(nom=nom, specialite=specialite, adresse=adresse, ville=ville, telephone=telephone, fax=fax)

    db.session.add(new_fournisseur)
    db.session.commit()


def adduser(username, password, email):
    new_user = Admin(username=username, password=password, email=email)
    db.session.add(new_user)
    db.session.commit()


def addmessage(nom, email , message):
    new_message = Contact(nom=nom, email=email, message=message)
    db.session.add(new_message)
    db.session.commit()


def add_email(email):
    new_email = Email(email=email)
    db.session.add(new_email)
    db.session.commit()



def delete_article_from_db(id_article):
    git_article = Articles.query.get(id_article)
    db.session.delete(git_article)
    db.session.commit()



def deletef(id_fornisseure):
    delete_fornisseure = Fornisseure.query.get(id_fornisseure)
    db.session.delete(delete_fornisseure)
    db.session.commit()


def get_article_by_id(article_id):

    article = Articles.query.get(article_id)
    return article


with app.app_context():
    db.create_all()



'''