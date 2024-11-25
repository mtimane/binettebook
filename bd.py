"""
Connexion à la BD
"""

import os
import types
import contextlib
import mysql.connector


@contextlib.contextmanager
def creer_connexion():
    """Pour créer une connexion à la BD"""
    conn = mysql.connector.connect(
        user=os.getenv('BD_UTILISATEUR'),
        password=os.getenv('BD_MDP'),
        host=os.getenv('BD_SERVEUR'),
        database=os.getenv('BD_NOM_SCHEMA'),
        raise_on_warnings=True
    )

    # Pour ajouter la méthode get_curseur() à l'objet connexion
    conn.get_curseur = types.MethodType(get_curseur, conn)

    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    else:
        conn.commit()
    finally:
        conn.close()


@contextlib.contextmanager
def get_curseur(self):
    """Permet d'avoir les enregistrements sous forme de dictionnaires"""
    curseur = self.cursor(dictionary=True)
    try:
        yield curseur
    finally:
        curseur.close()



def ajouter_utilisateur(conn, utilisateur):
    "Ajoute un utilisateur dans la BD"
    with conn.get_curseur() as curseur:
        curseur.execute(
            "INSERT INTO utilisateur (courriel, nom, mdp) VALUES (%(courriel)s, %(nom)s, %(mdp)s)",
            utilisateur
        )
        return curseur.lastrowid



def get_utilisateurs(conn):
    "Retourne tous les utilisateurs"
    with conn.get_curseur() as curseur:
        curseur.execute("SELECT * FROM utilisateur")
        return curseur.fetchall()



def get_utilisateur(conn, identifiant):
    """Retourne un utilisateur"""
    with conn.get_curseur() as curseur:
        curseur.execute(
            "SELECT * FROM utilisateur WHERE id_utilisateur=%(id_utilisateur)s",
            {
                "id_utilisateur": identifiant
            }
        )
        return curseur.fetchone()



def authentifier(conn, courriel, mdp):
    """Retourne un utilisateur avec le courriel et le mdp"""
    with conn.get_curseur() as curseur:
        curseur.execute(
            "SELECT * FROM utilisateur WHERE courriel=%(courriel)s and mdp=%(mdp)s",
            {
                "courriel": courriel,
                "mdp" : mdp
            }
        )
        return curseur.fetchone()



def get_messages_pour(conn, identifiant):
    """Retourne les messages pour un utilisateur"""
    with conn.get_curseur() as curseur:
        curseur.execute(
            "SELECT contenu, nom, fk_auteur FROM message " +
            "INNER JOIN utilisateur on fk_auteur=id_utilisateur " +
            "WHERE fk_destinataire=%(id)s",
            {
                "id": identifiant
            }
        )
        return curseur.fetchall()



def ajouter_message(conn, auteur, destinataire, contenu):
    """Pour ajouter un message à un utilisateur"""
    with conn.get_curseur() as curseur:
        curseur.execute(
            "INSERT INTO message (contenu, fk_auteur, fk_destinataire) " +
            "VALUES (%(contenu)s, %(fk_auteur)s, %(fk_destinataire)s)",
            {
                "contenu": contenu,
                "fk_auteur": auteur,
                "fk_destinataire": destinataire
            }
        )



def get_amis(conn, identifiant):
    """Retourne tous les amis d'un utilisateur"""
    with conn.get_curseur() as curseur:
        curseur.execute(
            "SELECT id_utilisateur,nom FROM utilisateur INNER JOIN " +
            "( " +
            "   SELECT fk_utilisateur as ami FROM `amitie` WHERE fk_ami=%(id)s " +
            "   UNION " +
            "   SELECT fk_ami         as ami FROM `amitie` WHERE fk_utilisateur=%(id)s " +
            ") Foo on id_utilisateur=ami;",
            {
                "id": identifiant
            }
        )
        return curseur.fetchall()



def ajouter_amitie(conn, id1, id2):
    """Ajoute un lien d'amitié entre id1 et id2"""
    with conn.get_curseur() as curseur:
        curseur.execute(
            "INSERT INTO amitie " +
            "(fk_utilisateur, fk_ami) VALUES (%(id1)s, %(id2)s)",
            {
                "id1": id1,
                "id2": id2
            }
        )
