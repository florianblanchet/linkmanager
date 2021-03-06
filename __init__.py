#source : https://www.youtube.com/watch?v=qla-KaMF-2Q
from flask import Flask, render_template, request, redirect, url_for
from models import *
app = Flask(__name__)

@app.before_request
def before_request():
	initialize_db()

@app.teardown_request
def teardown_request(exception):
	db.close()

@app.route('/')
def home():
	#print(Links.select().count())
	for link in Links.select():
		print(str(link.id)+' Catégorie : ' + link.categorie + '  ; Title :  ' + link.title +'  ; href :  ' +link.href+'  ; nb_aside :  ' +link.nb_aside)
	#for link in Links.select().where(Links.categorie == 'Divers'):
	#	print(link.title)
	#print(Links.select(Links.categorie)[1].categorie)
	#print(Links.select.where(Links.categorie=='Telecom'))
	#print(msg)
	categ = Links.select(Links.categorie).distinct() #Renvoie la liste des categories
	nb_asi = Links.select(Links.nb_aside).distinct() #Renvoie la liste des nb_aside
	mix=[]
	for i in range(len(categ)):
		mix.append([categ[i].categorie,nb_asi[i].nb_aside]) #Compacte dasn une liste commune
	return render_template('new_post.html',links=Links.select(),categories=mix,taille=len(Links.select(Links.categorie).distinct())+1)

#@app.route('/new_link/')
#def new_post():
#    return render_template('new_post.html')

@app.route('/create/', methods=['POST'])
def create_post():
	if (Links.select().where(Links.categorie == request.form['categorie']).count()==0): #Si nouvelle categorie
		Links.create(
			title= request.form['title'],
			href = request.form['href'],
			nb_aside= str(len(Links.select(Links.categorie).distinct())+1) ,
			categorie = request.form['categorie']
			)
	else :
		Links.create(
			title= request.form['title'],
			href = request.form['href'],
			nb_aside= Links.select().where(Links.categorie==request.form['categorie'])[0].nb_aside ,
			categorie = request.form['categorie']
			)

	#message='hello'
	return redirect(url_for('home'))

@app.route('/delete/', methods=['POST'])
def delete_post():
	lien = Links.get(Links.title == request.form['title'])
	ico_restants = Links.select().where(Links.categorie==lien.categorie).count()
	if (ico_restants==1) : # Si c'est le dernier 
		nb_aside_sup = lien.nb_aside
		change = Links.select().where(Links.nb_aside>nb_aside_sup)
		for link in change:
			link.nb_aside = str(int(link.nb_aside)-1)  #Actualise le nb_aside
			link.save()
	lien.delete_instance()  # Supprime l'icone 
	return redirect(url_for('home'))

@app.errorhandler(404)
def page_not_found(error):

    return "Cette page n'existe pas bro ! ", 404

@app.errorhandler(DatabaseError)
def special_exception_handler(error):

    return "T'as un pb dans ta bdd", 500

if __name__ == '__main__':
    app.run(debug=True)
