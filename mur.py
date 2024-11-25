"""
Pour gérer le mur
"""

from flask import Blueprint, session, abort, render_template, request, redirect

import bd
from utilitaires import est_un_ami, get_utilisateur_or_die, get_utilisateur_authentifié_or_die

bp_mur = Blueprint('mur', __name__)



@bp_mur.route('/<identifiant>', methods=["GET", "POST"])
def mur(identifiant):
    """Affiche le mur d'un utilisateur"""

    with bd.creer_connexion() as conn:
        profile = bd.get_utilisateur(conn, identifiant)
        if not profile:
            abort(404)

        messages = bd.get_messages_pour(conn, identifiant)
        erreur_message = False

        if request.method == "POST":
            contenu = request.form.get("contenu")
            if contenu:
                bd.ajouter_message(
                    conn,
                    get_utilisateur_authentifié_or_die()["id_utilisateur"],
                    identifiant,
                    contenu
                )

                # Rediriger en mode GET : code 303
                return redirect(f"/mur/{identifiant}", code=303)

            erreur_message = True

    return render_template(
        'mur/mur.jinja', profile=profile, messages=messages, erreur_message=erreur_message)



@bp_mur.route('/<int:identifiant>/amis')
def afficher_amis(identifiant):
    """Affiche les amis d'un utilisateur"""

    with bd.creer_connexion() as conn:
        profile = get_utilisateur_or_die(conn, identifiant)

        amis = bd.get_amis(conn, identifiant)

        peuvent_etre_amis = False
        if "utilisateur" in session:
            id_authentifié = session["utilisateur"]["id_utilisateur"]

            peuvent_etre_amis =                     \
                (id_authentifié != identifiant) and \
                not est_un_ami(id_authentifié, amis)

    return render_template(
        'mur/amis.jinja', profile=profile, amis=amis, peuvent_etre_amis=peuvent_etre_amis)


@bp_mur.route('/<int:identifiant>/amis', methods=["post"])
def devenir_ami(identifiant):
    """Pour devenir ami"""
    id_authentifié = get_utilisateur_authentifié_or_die()["id_utilisateur"]

    if identifiant == id_authentifié:
        abort(403)

    with bd.creer_connexion() as conn:
        get_utilisateur_or_die(conn, identifiant)

        amis = bd.get_amis(conn, identifiant)
        if est_un_ami(id_authentifié, amis):
            abort(403)

        bd.ajouter_amitie(conn, identifiant, id_authentifié)
    return redirect(f"/mur/{identifiant}/amis", code=303)
