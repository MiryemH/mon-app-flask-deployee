import os
from forms import FormAjoutUser, FormAjoutRole, FormSupprRole, FormSupprUser
from flask import Flask, render_template, url_for, redirect
#from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = "cleSecrète"

##############################################
### Section de configuration de BDD        ###
##############################################
basedir = os.path.abspath(os.path.dirname(__file__))
#sqlite:///chemin/absolu/vers/votre/projet/database.db
# le premier slash (/) indique que le chemin est absolu. 
# Le deuxième slash (/) sépare le protocole (sqlite:) du chemin d'accès absolu. 
# Le troisième slash (/) sépare le chemin d'accès absolu du nom de la BDD #

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'users_roles.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
#Migrate(app, db)

##############################################
### Section des Modèles         ###
##############################################

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    nom_role = db.Column(db.String(64), unique=True)
    #Plusieurs users associés à un rôle
    #backref='role' spécifie que chaque instance de la classe "User" 
    # aura un attribut supplémentaire appelé "role" de type Role, 
    #lazy=True, lorsqu'on fait role.lst_users, les users associés à ce role
    #seront chargés en différé (au moment de l'accès à la propriété)
    #c'est un objet SQLAlchemy qui sera renvoyé
    lst_users = db.relationship('User', backref='role', lazy='dynamic')
    
    # id sera automatiquement créer, on ne l'ajoute pas au constructeur!
    def __init__(self, nom):
        self.nom_role = nom
        
    def __repr__(self):
        # renvoie une chaine de représentation d'un rôle
        return f"Rôle: {self.nom_role}"
    
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    nom_u = db.Column(db.String(40), unique=True, index=True)
    mdp = db.Column(db.String(10))
    id_role = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
    # id sera automatiquement créer, on ne l'ajoute pas au constructeur!
    def __init__(self, nom, mdp, id_r):
        self.nom_u = nom
        self.mdp =  mdp
        self.id_role = id_r
             
    def __repr__(self):
        # renvoie une chaine de représentation d'un user
        if self.role:
            return f"User:  {self.nom_u}, {self.role}"
        else:
            return f"User:  {self.nom_u} n'a pas de rôle attribué"

@app.route('/')
def index():
    db.drop_all()
    db.create_all()
    return render_template('index.html')

@app.route('/ajout_role', methods=['GET', 'POST'])
def ajouter_role():
    form = FormAjoutRole()

    if form.validate_on_submit():
        nom_r = form.nom_r.data

        # Ajouter un nouveau rôle à la BDD
        nv_role = Role(nom_r)
        db.session.add(nv_role)
        db.session.commit()

        return redirect(url_for('lister_roles_et_users'))

    return render_template('ajout_role.html',form=form)

@app.route('/ajout_user', methods=['GET', 'POST'])
def ajouter_user():

    form = FormAjoutUser()

    if form.validate_on_submit():
        nom_u = form.nom_u.data
        mdp_u = form.mdp_u.data
        id_role = form.id_role.data
        # ajouter un nouveau user à la bdd
        nv_user = User(nom_u, mdp_u, id_role)
        db.session.add(nv_user)
        db.session.commit()

        return redirect(url_for('lister_roles_et_users'))

    return render_template('ajout_user.html',form=form)

@app.route('/listes')
def lister_roles_et_users():
    # Obtenir les listes des users et des rôles
    lst_roles = Role.query.all()
    lst_users = User.query.all()
    return render_template('affficher_listes.html', lst_roles=lst_roles, lst_users=lst_users )

@app.route('/suppression_user', methods=['GET', 'POST'])
def supprimer_user():

    form = FormSupprUser()

    if form.validate_on_submit():
        id = form.id.data
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()

        return redirect(url_for('lister_roles_et_users'))
    return render_template('suppr_user.html',form=form)


if __name__ == '__main__':
    app.run(debug=True)

    