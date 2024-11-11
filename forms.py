from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField

class FormAjoutUser(FlaskForm):
    nom_u = StringField("Votre nom: ")
    mdp_u = PasswordField("Votre Mot De Passe: ")
    id_role = IntegerField("Id Rôle: ")
    envoyer = SubmitField("Ajouter Utilisateur") 


class FormAjoutRole(FlaskForm):

    nom_r = StringField('Nom Rôle: ')
    envoyer = SubmitField('Ajouter Rôle')

class FormSupprRole(FlaskForm):
    id = IntegerField('Id du rôle à supprimer:')
    envoyer = SubmitField('Supprimer Rôle')
    
class FormSupprUser(FlaskForm):
    id = IntegerField('Id Utilisateur à supprimer:')
    envoyer = SubmitField('Supprimer Utilisateur')
    


