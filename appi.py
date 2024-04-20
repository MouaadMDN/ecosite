from flask import Flask, render_template, request, redirect, url_for, flash, session
from cr_database import addarticle, db, Articles, Fornisseure, addfournisseur, adduser, Admin, add_email, addmessage, add_order, Email, Contact,Purchases, delete_article_from_db, deletef, get_article_by_id, Categories
from os import path
import os
from functools import wraps
from sqlalchemy import func
#from flask_paginate import Pagination, get_page_args

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///C:/Users/hp/Desktop/eco_site/database.db"
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SECRET_KEY'] = 'heufhezpf654'


db.init_app(app)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap






@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        name = request.form['name']
        editor1 = request.form['editor1']
        prix = request.form['prix']
        stock = request.form['stock']
        status = request.form['status']
        categories_id = request.form['categories_id']
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                image_filename = os.path.basename(image.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
                image.save(save_path)
            else:
                save_path = None
        else:
            save_path = None

        addarticle(name, editor1, prix, stock, image_filename, status, categories_id)
        return redirect('dashboard')

    if 'username' in session and 'email' in session:
        username = session['username']
        email = session['email']

    all_article = Articles.query.all()
    reversed_articles = list(reversed(all_article))
    number_article = db.session.query(func.count(Articles.id_article)).scalar()# this line gir total articles whe hane in database
    number_Fournisseur = db.session.query(func.count(Fornisseure.id_fornisseure)).scalar()# this line gir total Fornisseure whe hane in database
    number_users = db.session.query(func.count(Admin.id_admin)).scalar()
    return render_template('indexd.html', all_article=reversed_articles, number_users=number_users, username=username, email=email, number_article=number_article, number_Fournisseur=number_Fournisseur)








'''@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        name = request.form['name']
        editor1 = request.form['editor1']
        prix = request.form['prix']
        stock = request.form['stock']
        status = request.form['status']
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                image_filename = os.path.basename(image.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
                image.save(save_path)
            else:
                save_path = None
        else:
            save_path = None

        addarticle(name, editor1, prix, stock, save_path, status)
        return redirect('dashboard')

    if 'username' in session and 'email' in session:
        username = session['username']
        email = session['email']

    all_article = Articles.query.all()
    reversed_articles = list(reversed(all_article))
    number_article = db.session.query(func.count(Articles.id_article)).scalar()# this line gir total articles whe hane in database
    number_Fournisseur = db.session.query(func.count(Fornisseure.id_fornisseure)).scalar()# this line gir total Fornisseure whe hane in database

    return render_template('indexd.html', all_article=reversed_articles, username=username, email=email, number_article=number_article, number_Fournisseur=number_Fournisseur)

'''
@app.route('/index')
@app.route('/')
def index():
    all_article = Articles.query.all()

    return render_template('index.html', all_article=all_article)



@app.route('/shop')
def shop():
    git_all_articles = Articles.query.all()
    categorie = Categories.query.all()
    return render_template('shop.html', categorie=categorie, git_all_articles=git_all_articles)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        nom = request.form['nom']
        email = request.form['email']
        message = request.form['message']
        addmessage(nom, email, message)
        return redirect('contact')


    return render_template('contact.html')


@app.route('/shop_details/<int:shop_id>')
def shop_details(shop_id):
    git_article= get_article_by_id(shop_id)
    git_all_articles = Articles.query.all()
    return render_template('shop_details.html', git_article=git_article, git_all_articles=git_all_articles)



@app.route('/details/<int:details_id>', methods=['GET', 'POST'])
@login_required
def details(details_id):
    article_by_id = Articles.query.get(details_id)

    if request.method == 'POST':
        article_by_id.name = request.form['name']
        article_by_id.editor1 = request.form['editor1']
        article_by_id.stock = request.form['stock']
        article_by_id.prix = request.form['prix']
        article_by_id.status = request.form['status']
        article_by_id.categories_id = request.form['categories_id']

        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                image_filename = os.path.basename(image.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
                image.save(save_path)
                article_by_id.image = save_path
        db.session.commit()
        return redirect(url_for('articles'))
    return render_template('details.html', article_by_id=article_by_id)


@app.route('/checkout/<int:checkout_id>', methods=['GET', 'POST'])
def checkout(checkout_id):
    git_article_id = Articles.query.get(checkout_id)
    if request.method == 'POST':
        prenom = request.form['prenom']
        nom = request.form['nom']
        adresse = request.form['adresse']
        quantite_article = int(request.form['quantite_article'])
        ville = request.form['ville']
        nom_article = request.form['nom_article']
        code_postal = request.form['code_postal']
        telephone = request.form['telephone']
        email = request.form['email']
        purchese_id = request.form['purchese_id']

        article_price = float(git_article_id.prix)
        total_price = quantite_article * article_price

        add_order(prenom, nom, adresse, quantite_article, ville, nom_article, code_postal, telephone, email, purchese_id)
        flash('{total_price} تمة عملية الشراء بنجاح ')
        session['prenom'] = prenom
        session['nom'] = nom
        session['total_price'] = total_price
        session['email'] = email
        session['quantite_article'] = quantite_article
        session['ville'] = ville
        session['telephone'] = telephone
        session['nom_article'] = nom_article
        session['adresse'] = adresse


        return redirect(url_for('billing'))

    return render_template('checkout.html', git_article_id=git_article_id, checkout_id=checkout_id)


@app.route('/fournisseur', methods=['GET', 'POST'])
# this founction add fournisseur to database
@login_required
def fournisseur():
    if request.method == 'POST':
        nom = request.form['nom']
        specialite = request.form['specialite']
        adresse = request.form['adresse']
        ville = request.form['ville']
        telephone = request.form['telephone']
        fax = request.form['fax']
        addfournisseur(nom, specialite, adresse, ville, telephone, fax)
    else:
        return 'request is nit post '

    return redirect('dashboard')

@app.route('/detailsf')
def detailsf():
    show_all_fournisseur = Fornisseure.query.all()
    return render_template('detailsf.html', show_all_fournisseur=show_all_fournisseur)

@app.route('/articles')
@login_required
def articles():
    show_all_article = Articles.query.all()
    reversed_articles = list(reversed(show_all_article))

    return render_template('articles.html', show_all_article=reversed_articles)


@app.route('/editf/<int:f_id>', methods=['GET', 'POST'])
@login_required
def editf(f_id):
    git_id_fournisseur = Fornisseure.query.get(f_id)

    if request.method == 'POST':
        git_id_fournisseur.nom =request.form['nom']
        git_id_fournisseur.specialite =request.form['specialite']
        git_id_fournisseur.adresse =request.form['adresse']
        git_id_fournisseur.ville =request.form['ville']
        git_id_fournisseur.telephone =request.form['telephone']
        git_id_fournisseur.fax =request.form['fax']
        db.session.commit()

    return render_template('editf.html', git_id_fournisseur=git_id_fournisseur)


@app.route('/addnewuser', methods=['GET', 'POST'])
@login_required
def addnewuser():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        adduser(username, password, email)
    else:
        return 'request is not POST '

    return redirect(url_for('dashboard'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = Admin.query.filter_by(email=email, password=password).first()
        if user:
            session['username'] = user.username
            session['email'] = user.email
            session['logged_in'] = True

            return redirect('dashboard')
        else:
            return 'infermation is not correct'

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('login')


@app.route('/addemail', methods=['GET', 'POST'])
@login_required
def addemail():
    if request.method == 'POST':
        email = request.form['email']
        redirect_url = request.form['redirect_url']
        add_email(email)
        return redirect(redirect_url)
    else:
        return 'request is no POST'




@app.route('/email')
@login_required
def email():
    git_all_emails = Email.query.all()
    return render_template('email.html', git_all_emails=git_all_emails)


@app.route('/messages')
@login_required
def messages():
    git_all_messages = Contact.query.all()
    return render_template('messages.html', git_all_messages=git_all_messages)



@app.route('/dmessage/<int:message_id>')
@login_required
def dmessage(message_id):
    git_message_by_id = Contact.query.get(message_id)
    return render_template('dmessage.html', git_message_by_id=git_message_by_id)



@app.route('/purchases')
@login_required
def purchases():
    git_all_purchases = Purchases.query.all()
    return render_template('purchases.html', git_all_purchases=git_all_purchases)



@app.route('/delete/<int:delete_id>', methods=['GET', 'POST'])
@login_required
def delete(delete_id):
    if request.method == 'POST':
        delete_article_by_id = Articles.query.get(delete_id)
        if delete_article_by_id:
            delete_article_from_db(delete_id)
            return redirect(url_for('dashboard'))

        delete_fournisseur_by_id = Fornisseure.query.get(delete_id)
        if delete_fournisseur_by_id:
            deletef(delete_id)
            return redirect(url_for('detailsf'))


        else:
            'try  again '
    return redirect('dashbard')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_name = request.form.get('search_name')
        results = Articles.query.filter(Articles.name.ilike(f"%{search_name}%")).all()
    categorie = Categories.query.all()
    return render_template('search.html', results=results, search_name=search_name, categorie=categorie)


@app.route('/billing')
def billing():
    prenom = session.get('prenom')
    nom = session.get('nom')
    total_price = session.get('total_price')
    email = session.get('email')
    ville = session.get('vill')
    telephone = session.get('telephone')
    quantite_article = session.get('quantite_article')
    nom_article = session.get('nom_article')
    adresse = session.get('adresse')
    return render_template('billing.html', prenom=prenom, nom=nom, adresse=adresse, total_price=total_price, email=email, ville=ville, telephone=telephone, quantite_article=quantite_article, nom_article=nom_article)


@app.route('/searchd', methods=['GET', 'POST'])
def searchd():
    if request.method == 'POST':
        search_a = request.form.get('search_word')
        search_f = request.form.get('search_f')
        all_results = []

        if search_a:
            results_a = Articles.query.filter(Articles.name.ilike(f"%{search_a}%")).all()
            all_results.extend(results_a)
        if search_f:
            results_f = Fornisseure.query.filter(Fornisseure.nom.ilike(f"%{search_f}%")).all()
            all_results.extend(results_f)
    else:return redirect(url_for('dashboard'))
    return render_template('searchd.html', search_a=search_a, search_f=search_f, all_results=all_results)



@app.route('/categories/<categorie>')
def categories(categorie):
    git_categorie = Categories.query.filter_by(name=categorie).first()
    git_articles = Articles.query.filter_by(categories_id=git_categorie.name).all()
    categorie = Categories.query.all()
    return render_template('categories.html', git_categorie=git_categorie, git_articles=git_articles, categorie=categorie)

if __name__ == '__main__':
    app.run(debug=True)