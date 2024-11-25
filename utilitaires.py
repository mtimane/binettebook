"""
Fonctions utilitaires
"""

import hashlib

from flask import abort, session

import bd



def get_utilisateur_authentifié_or_die():
    """Retourne l'utilisateur authentifié ou faire un abort(code)"""
    if "utilisateur" not in session :
        abort(401)

    return session["utilisateur"]



def get_utilisateur_or_die(conn, identifiant):
    """Retourne le profile d'un utilisateur existant ou faire un abort(code)"""
    profile = bd.get_utilisateur(conn, identifiant)
    if profile is None:
        abort(404)
    return profile



def est_un_ami(identifiant_a_chercher, amis):
    """Indique si un identifiant est dans la liste des amis"""
    for ami in amis:
        if ami["id_utilisateur"] == identifiant_a_chercher:
            return True
    return False



def hacher_mdp(mdp_en_clair):
    """Prend un mot de passe en clair et lui applique une fonction de hachage"""
    return hashlib.sha512(mdp_en_clair.encode('utf-8')).hexdigest()