"""
Pour gérer l'authentification
"""

from flask import Blueprint, session, render_template, request, redirect, current_app as app

import bd
from utilitaires import hacher_mdp

bp_compte = Blueprint('compte', __name__)


@bp_compte.route('/authentifier', methods=['GET', 'POST'])
def authentifier():
    """Pour effectuer une authentification"""
    erreur = False
    courriel = request.form.get("courriel", default="")

    if (request.method == 'POST') :
        app.logger.info(f"Début de l'authentification pour {courriel}")
        mdp = hacher_mdp(request.form.get("mdp"))
        with bd.creer_connexion() as conn:
            utilisateur = bd.authentifier(
                conn,
                courriel,
                mdp
            )
            erreur = (not utilisateur)
            app.logger.debug(f"Authentification de {courriel} : {not erreur}")
            if not erreur:
                session["utilisateur"] = utilisateur
                return redirect('/', code=303)

    return render_template(
        'compte/authentifier.jinja',
        courriel=courriel,
        erreur=erreur
    )



@bp_compte.route('/creer', methods=['GET', 'POST'])
def creer():
    """Pour créer un compte"""

    champs = {
        "courriel" : {
            "valeur" : request.form.get("courriel", default=""),
            "en_erreur" : False
        },
        "nom" : {
            "valeur" : request.form.get("nom", default=""),
            "en_erreur" : False
        },
        "mdp" : {
            "en_erreur" : False
        },
    }

    if (request.method == 'POST') :
        mdp = request.form.get("mdp")
        if mdp != request.form.get("mdp2"):
            champs["mdp"]["en_erreur"] = True
        else :
            mdp = hacher_mdp(mdp)
            with bd.creer_connexion() as conn:
                utilisateur = {
                    "courriel" : champs["courriel"]["valeur"],
                    "nom": champs["nom"]["valeur"],
                    "mdp": mdp
                }


                utilisateur["id_utilisateur"] = bd.ajouter_utilisateur(conn, utilisateur)
                session["utilisateur"] = utilisateur
                return redirect('/', code=303)

    return render_template('compte/creer.jinja', champs=champs)



@bp_compte.route('/deconnecter', methods=['GET'])
def deconnecter():
    """Pour se déconnecter"""
    if "utilisateur" in session:
        app.logger.info(f"Déconnexion de {session['utilisateur']['courriel']}")               
    session.clear()
    return redirect("/")
