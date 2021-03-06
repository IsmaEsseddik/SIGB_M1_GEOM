import tkinter as tk
import isbnlib as lib
from InitialisationBDD import *
import tkinter.messagebox as msg


class Infodoc:
    """ Interface graphique relatif a la gestion de la table Infodoc de la base de données """
    def __init__(self, master):
        """Constructeur de l'interface graphique"""
        # ------------------- Atrributs objets -------------------------
        self.isbn = tk.StringVar(master, value='ISBN 978-2-74603707-6')
        self.titre = tk.StringVar(master, value='')
        self.auteur = tk.StringVar(master, value='')
        self.editeur = tk.StringVar(master, value='')
        self.date_edition = tk.StringVar(master, value='')
        self.cote = tk.StringVar(master, value='')
        self.description = None
        self.liste_recherche = None
        # ------------------ Attributs graphiques -------------------------
        self.master = master  # creation d'une simple fenêtre.
        self.master.attributes("-fullscreen", False)  # pour metre en pleine ecran.
        self.master.geometry('800x600+0+0')  # pour la taille et le positionnement initiale.
        self.master.state('zoomed')  # pour maximiser la fenetre.
        self.master['bg'] = 'bisque'  # pour l'arriere plan en couleur bisque.
        self.master.title("Gest_Biblio - Gestionnaire d'edition")  # pour donner un titre a l'application (title bar).
        # creation du conteneur principal
        self.contenu = tk.PanedWindow(self.master, orient="vertical", borderwidth=3, relief="sunken", bg='#d8d8d8')
        # creation des cadres
        self.cadre_entete = tk.Frame(self.contenu, borderwidth=3, relief="raised", bg='purple')
        self.cadre_corp = tk.Frame(self.contenu, bg='#d8d8d8')
        self.cadre_ppage = tk.Frame(self.contenu, bg='#d8d8d8')
        self.cadreapi = tk.Frame(self.cadre_corp, bg='#d8d8d8')
        self.cadrelib = tk.LabelFrame(self.cadre_corp, text="Informations sur l'edition", labelanchor="n", padx=20,
                                      pady=20, borderwidth=3, relief="sunken", bg='#d8d8d8')
        self.cadreinfo = tk.Frame(self.cadrelib, bg='#d8d8d8')
        self.cadreinfoL = tk.Frame(self.cadreinfo, bg='#d8d8d8')
        self.cadreinfoR = tk.Frame(self.cadreinfo, bg='#d8d8d8')
        self.cadraction = tk.Frame(self.cadreinfoR, bg='#d8d8d8')
        self.cadredesc = tk.Frame(self.cadrelib, bg='#d8d8d8')
        # creation de libellés
        self.welcome_label = tk.Label(self.cadre_entete,
                                      text="Gestionnaire d'editions : Ici vous pouvez rechercher un isbn"
                                           " via l'api google et enregistrer dans la base de données", bg='purple')
        self.isbn_label = tk.Label(self.cadreapi, text="ISBN : ", bg='#d8d8d8')  # creation de libellés.
        self.titre_label = tk.Label(self.cadreinfoL, text="Titre : ", bg='#d8d8d8')
        self.auteur_label = tk.Label(self.cadreinfoL, text="Auteur : ", bg='#d8d8d8')
        self.editeur_label = tk.Label(self.cadreinfoL, text="Editeur : ", bg='#d8d8d8')
        self.date_edition_label = tk.Label(self.cadreinfoL, text="Date d'edition : ", bg='#d8d8d8')
        self.cote_label = tk.Label(self.cadreinfoL, text="Cote : ", bg='#d8d8d8')
        self.description_label = tk.Label(self.cadredesc, text="Description : ", bg='#d8d8d8')
        self.ver_label = tk.Label(self.cadre_ppage, text="Esseddik Ismael, M1 Geomatique ENSG, ©2017",
                                  fg='blue', bg='#d8d8d8')
        # creation de champs
        self.isbn_champ = tk.Entry(self.cadreapi, width=50, textvariable=self.isbn, justify='center')
        self.titre_champ = tk.Entry(self.cadreinfoR, width=50, textvariable=self.titre)
        self.auteur_champ = tk.Entry(self.cadreinfoR, width=50, textvariable=self.auteur)
        self.editeur_champ = tk.Entry(self.cadreinfoR, width=50, textvariable=self.editeur)
        self.date_edition_champ = tk.Entry(self.cadreinfoR, width=50, textvariable=self.date_edition)
        self.cote_champ = tk.Entry(self.cadreinfoR, width=50, textvariable=self.cote)
        self.description_champ = tk.Text(self.cadredesc, height=30, width=70, wrap="word")
        # creation boutons
        self.bouton_api = tk.Button(self.cadreapi, text="Recherche API ", command=self.recherche_api)
        self.bouton_rechercher = tk.Button(self.cadreapi, text="Rechercher interne", command=self.listing)
        self.bouton_ajout = tk.Button(self.cadraction, text="Ajouter ", command=self.enregistrer_infodoc)
        self.bouton_suppr = tk.Button(self.cadraction, text="Supprimer ", command=self.supprimer_infodoc)
        self.bouton_maj = tk.Button(self.cadraction, text="MiseAjour ", command=self.maj_infodoc)
        self.bouton_quitter = tk.Button(self.cadre_ppage, text="Quitter", command=self.master.destroy)
        # affichage
        self.contenu.pack(side="top", expand="y", fill="both", padx=10, pady=10)
        self.cadre_entete.pack(side="top", fill="both", padx=60, pady=10)
        self.cadre_corp.pack(side="top", padx=3, pady=3)
        self.cadre_ppage.pack(side="top", fill="x", padx=3, pady=10)
        self.welcome_label.pack(padx=10, pady=10)
        self.cadreapi.pack(fill="both", expand="yes")
        self.isbn_label.pack(side='left')
        self.isbn_champ.pack(side='left')
        self.bouton_api.pack(side='right')
        self.bouton_rechercher.pack(side='right')

        self.cadrelib.pack(fill="both", expand="yes")
        self.cadreinfo.pack(side="left", fill="both", expand="yes", pady=20)
        self.cadreinfoL.pack(side="left", fill="both", expand="yes")
        self.cadreinfoR.pack(side="right", fill="both", expand="yes")
        self.cadraction.pack(side="bottom", fill="both", expand="no")
        self.cadredesc.pack(side="right", fill="both", expand="yes")

        self.titre_label.pack()
        self.titre_champ.pack(pady=1)
        self.auteur_label.pack()
        self.auteur_champ.pack(pady=1)
        self.editeur_label.pack()
        self.editeur_champ.pack(pady=1)
        self.date_edition_label.pack()
        self.date_edition_champ.pack(pady=1)
        self.cote_label.pack()
        self.cote_champ.pack(pady=1)
        self.description_label.pack()
        self.description_champ.pack()
        self.bouton_ajout.pack(side='left')
        self.bouton_suppr.pack(side='left')
        self.bouton_maj.pack(side='left')
        self.ver_label.pack(side='right')
        self.bouton_quitter.pack(side='left')

    # --------------------Methodes pour les requêtes de contrôle dans la base de données ----------------------------
    def exist_infodoc(self):
        """Methode qui verifie l'existance d' un isbn dans la table infos_documents,
         retourne une liste de tuple de contenant les valeurs de chaque champ ou NONE si non trouvé.
        """
        requetesql = """SELECT * FROM infos_documents WHERE isbn = ? """
        param = lib.EAN13(self.isbn_champ.get()),  # mise au format EAN13
        if (lecture(requetesql, param) == []):  # si aucun resultat
            return None
        else:
            return lecture(requetesql, param)

    def exist_isbn_exemp(self):
        """Methode qui verifie l'existance d' un isbn dans la table des exemplaires et retourne une liste de tuple
        contenant les valeurs de chaque champ ou NONE si non trouvé.
        :objet_exemp: objet dont l'attribut isbn sera recherhé.
        """
        requetesql = """SELECT * FROM exemplaires WHERE exemp_isbn = ? """
        param = lib.EAN13(self.isbn_champ.get()),
        if (lecture(requetesql, param) == []):
            return None
        else:
            return lecture(requetesql, param)

# -----------Ajout/suppression dans une base de données.---------
    def enregistrer_infodoc(self):
        """Methode qui ajoute une entrée valide dans la table info_documents (si elle n'existe pas déja)
        en remplissant tout les champs.
        :objet_infodoc: objet instancé d'un attribut pour chaque champs de sa table.
        """
        try:
            if (self.exist_infodoc() is None and lib.is_isbn13(lib.EAN13(self.isbn_champ.get())) is True):
                # Si l'isbn est valide et n'existe pas dans sa table
                requetesql = """INSERT INTO infos_documents(isbn, titre, auteur, editeur, date_edition, cote, description) 
                VALUES(?,?,?,?,?,?,?)"""
                param = lib.EAN13(self.isbn_champ.get()), self.titre_champ.get(), self.auteur_champ.get(), \
                    self.editeur_champ.get(), self.date_edition_champ.get(), self.cote_champ.get(), \
                    self.description_champ.get(1.0, tk.END),
                ecriture(requetesql, param)
                print("Les informations isbn ont été ajoutés dans la base de données")
            else:
                msg.showinfo('Impossible', "L'isbn existe deja dans la base de données ou est invalide ",
                             parent=self.master)
        except TypeError:
            msg.showerror('ERREUR', 'ISBN invalide !', parent=self.master)

    def supprimer_infodoc(self):
        """Methode qui supprime une entrée (si elle existe) de la table info_documents a condition que l'isbn ne soit
        associé à aucun exemplaire.
        """
        try:
            if (self.exist_infodoc() is not None):  # si l'isbn existe dans sa table
                if (self.exist_isbn_exemp() is None):  # si l'isbn n'existe pas dans la table exemplaires
                    requetesql = """DELETE FROM infos_documents WHERE isbn = ?"""
                    param = lib.EAN13(self.isbn_champ.get()),
                    ecriture(requetesql, param)
                    print("Les informations isbn ont été supprimée de la base de données")
                else:
                    msg.showinfo('Impossible', "isbn associé à un ou plusieurs exemplaire(s), supprimez d'abord les "
                                               "exemplaires", parent=self.master)
            else:
                msg.showinfo('Impossible', "isbn inexistant", parent=self.master)
        except TypeError:
            msg.showerror('ERREUR', 'ISBN invalide !', parent=self.master)

# -----------Modification dans la base de données.---------
    def maj_infodoc(self):
        """Methode qui met a jour tout les champ d'une entrée dans la base de données (si l'isbn y existe)
        de la table info_documents.
        """
        try:
            if(self.exist_infodoc() is not None):  # si l'isbn existe dans sa table
                requetesql = """UPDATE infos_documents SET titre =  ? WHERE isbn = ? """
                param = self.titre_champ.get(), lib.EAN13(self.isbn_champ.get()),
                ecriture(requetesql, param)
                requetesql = """UPDATE infos_documents SET auteur =  ? WHERE isbn = ? """
                param = self.auteur_champ.get(), lib.EAN13(self.isbn_champ.get()),
                ecriture(requetesql, param)
                requetesql = """UPDATE infos_documents SET editeur =  ? WHERE isbn = ? """
                param = self.editeur_champ.get(), lib.EAN13(self.isbn_champ.get()),
                ecriture(requetesql, param)
                requetesql = """UPDATE infos_documents SET date_edition =  ? WHERE isbn = ? """
                param = self.date_edition_champ.get(), lib.EAN13(self.isbn_champ.get()),
                ecriture(requetesql, param)
                requetesql = """UPDATE infos_documents SET cote =  ? WHERE isbn = ? """
                param = self.cote_champ.get(), lib.EAN13(self.isbn_champ.get()),
                ecriture(requetesql, param)
                requetesql = """UPDATE infos_documents SET description = ? WHERE isbn = ? """
                param = self.description_champ.get(1.0, tk.END), lib.EAN13(self.isbn_champ.get()),
                ecriture(requetesql, param)
                print("Les informations isbn ont été mis a jour dans la base de données")
            else:
                msg.showinfo('Impossible', "isbn inexistant")
        except TypeError:
            msg.showerror('ERREUR', 'ISBN invalide !', parent=self.master)

# -----------Recherche & conditionnement de l'objet---------
    def get_liste_BDD(self, champwhere="isbn"):
        """ Methode qui, selon le champ de recherche specifié en argument, recherche dans la table InfoDocument
        la valeur specifié en argument et stock la reponse sous forme d'une liste de tuple.
        :champwhere: le champ a specifier dans lequelle la valeur sera recherché(champ isbn par defaut)
        """
        if (self.isbn_champ.get() == ''):
            msg.showinfo('Erreur', "Veuillez specifier un isbn ", parent=self.master)
            return
        requetesql = """SELECT * FROM infos_documents WHERE """ + champwhere + """ REGEXP ? """
        param = lib.EAN13(self.isbn_champ.get()),
        fetch = lecture(requetesql, param)
        if (fetch == [] or fetch is None):
            msg.showinfo('Resultat', "Aucun resultat(s)", parent=self.master)
            return
        else:
            self.liste_recherche = fetch
            print(self.liste_recherche)

    def set_from_liste(self, i=0):
        """ Methode qui conditionne l'objet a partir de la liste de tuple obtenu a la derniere recherche.
        :i: numero du tuple dans la liste de recherche (1er occurence par defaut)
        """
        self.isbn.set(self.liste_recherche[i][0])
        self.titre.set(self.liste_recherche[i][1])
        self.auteur.set(self.liste_recherche[i][2])
        self.editeur.set(self.liste_recherche[i][3])
        self.date_edition.set(self.liste_recherche[i][4])
        self.cote.set(self.liste_recherche[i][5])
        self.description_champ.delete(1.0, tk.END)
        self.description_champ.insert(1.0, self.liste_recherche[i][6])
        print(self.isbn, self.titre, self.auteur, self.editeur, self.date_edition, self.cote, self.description)

    def listing(self):
        """methode pour afficher le contenu de la rechereche """
        self.get_liste_BDD()
        self.set_from_liste()

# -----------Methode API .---------
    def recherche_api(self):
        """Recupere des meta-donnée grace a l'API google a partir de l'isbn et les integre aux attributs de l'objet,
        """
        try:
            metadonnees = lib.meta(lib.EAN13(self.isbn_champ.get()))
            if metadonnees is not None:
                self.isbn.set(metadonnees['ISBN-13'])
                self.titre.set(metadonnees['Title'])
                self.auteur.set(", ".join(metadonnees['Authors']))
                self.editeur.set(metadonnees['Publisher'])
                self.date_edition.set(metadonnees['Year'])
                self.description_champ.delete(1.0, tk.END)
                self.description_champ.insert(1.0, lib.desc(lib.EAN13(self.isbn_champ.get())))
            else:
                raise NameError("ISBN introuvable ! (Verfier votre connexion)")
        except lib.NotValidISBNError:
            msg.showinfo("ERREUR !", "ISBN invalide", parent=self.master)
        except NameError as ne:
            msg.showinfo('ERREUR !', str(ne), parent=self.master)
