import tkinter as tk
from InitialisationBDD import *
import re
import tkinter.messagebox as msg


class Lect:
    """ Interface graphique relatif a la gestion de la table Lecteur de la base de données """
    def __init__(self, master):
        """Constructeur de l'interface graphique"""
        # ------------------- Atrributs objets -------------------------
        self.num_etudiant = tk.StringVar(master, value='')
        self.nom = tk.StringVar(master, value='')
        self.prenom = tk.StringVar(master, value='')
        self.date_naissance = tk.StringVar(master, value='')
        self.niveau_etude = tk.StringVar(master, value='')
        self.num_tel = tk.StringVar(master, value='')
        self.suspension = tk.StringVar(master, value='')
        self.commentaire = None
        self.liste_recherche = None
        # ------------------ Attributs graphiques -------------------------
        self.master = master  # creation d'une simple fenêtre.
        self.master.attributes("-fullscreen", False)  # pour metre en plein ecran.
        self.master.geometry('750x425+0+0')  # pour la taille et le positionnement initiale.
        self.master.state('normal')  # pour maximiser la fenetre.
        self.master['bg'] = 'bisque'  # pour l'arriere plan en couleur gris.
        self.master.title("Gest_Biblio - Gestionnaire de lecteurs")  # pour donner un titre a l'application (title bar).
        # creation du conteneur principale
        self.contenu = tk.PanedWindow(self.master, orient="vertical", borderwidth=3, relief="sunken", bg='#d8d8d8')
        # creation des cadres
        self.cadre_entete = tk.Frame(self.contenu, borderwidth=3, relief="raised", bg='Blue')
        self.cadre_corp = tk.Frame(self.contenu, bg='#d8d8d8')
        self.cadre_ppage = tk.Frame(self.contenu, bg='#d8d8d8')
        self.cadrenumetu = tk.Frame(self.cadre_corp, bg='#d8d8d8')
        self.cadrelib = tk.LabelFrame(self.cadre_corp, text="Informations sur le lecteur", labelanchor="n", padx=20,
                                      pady=20, borderwidth=3, relief="sunken", bg='#d8d8d8')
        self.cadreinfo = tk.Frame(self.cadrelib, bg='#d8d8d8')
        self.cadreinfoL = tk.Frame(self.cadreinfo, bg='#d8d8d8')
        self.cadreinfoR = tk.Frame(self.cadreinfo, bg='#d8d8d8')
        self.cadraction = tk.Frame(self.cadreinfoR, bg='#d8d8d8')
        self.cadrecom = tk.Frame(self.cadrelib, bg='#d8d8d8')
        # creation de libellés
        self.welcome_label = tk.Label(self.cadre_entete, text="Gestionnaire de lecteur : Ici vous pouvez rechercher "
                                                              "un lecteur dans la base de données", bg='blue')
        self.numetu_label = tk.Label(self.cadrenumetu, text="Numero étudiant : ", bg='#d8d8d8')  # creation de libellés.
        self.nom_label = tk.Label(self.cadreinfoL, text="Nom : ", bg='#d8d8d8')
        self.prenom_label = tk.Label(self.cadreinfoL, text="Prenom : ", bg='#d8d8d8')
        self.date_naissance_label = tk.Label(self.cadreinfoL, text="Date de naissance : ", bg='#d8d8d8')
        self.niveau_etude_label = tk.Label(self.cadreinfoL, text="Niveau d'étude : ", bg='#d8d8d8')
        self.num_tel_label = tk.Label(self.cadreinfoL, text="Numero de telephone : ", bg='#d8d8d8')
        self.suspension_label = tk.Label(self.cadreinfoL, text="Date de suspension(AAAA-MM-JJ)", bg='#d8d8d8')
        self.commentaire_label = tk.Label(self.cadrecom, text="Commentaire : ", bg='#d8d8d8')
        self.ver_label = tk.Label(self.cadre_ppage, text="Esseddik Ismael, M1 Geomatique ENSG, ©2017",
                                  fg='blue', bg='#d8d8d8')
        # creation de champs
        self.numetu_champ = tk.Entry(self.cadrenumetu, textvariable=self.num_etudiant, width=50, justify='center')
        self.nom_champ = tk.Entry(self.cadreinfoR, textvariable=self.nom, width=50)
        self.prenom_champ = tk.Entry(self.cadreinfoR, textvariable=self.prenom, width=50)
        self.date_naissance_champ = tk.Entry(self.cadreinfoR, textvariable=self.date_naissance, width=50)
        self.niveau_etude_champ = tk.Entry(self.cadreinfoR, textvariable=self.niveau_etude, width=50)
        self.num_tel_champ = tk.Entry(self.cadreinfoR, textvariable=self.num_tel, width=50)
        self.suspension_champ = tk.Entry(self.cadreinfoR, textvariable=self.suspension, width=50, state='disabled',
                                         disabledbackground='bisque')
        self.commentaire_champ = tk.Text(self.cadrecom, height=10, width=70, wrap="word", state='normal')
        # creation des boutons
        self.bouton_recherche = tk.Button(self.cadrenumetu, text="Rechercher un lecteur", command=self.listing)
        self.bouton_ajout = tk.Button(self.cadraction, text="Ajouter ", command=self.enregistrer_lect)
        self.bouton_suppr = tk.Button(self.cadraction, text="Supprimer ", command=self.supprimer_lect)
        self.bouton_maj = tk.Button(self.cadraction, text="MiseAjour ", command=self.maj_lect)
        self.bouton_quitter = tk.Button(self.cadre_ppage, text="Quitter", command=self.master.destroy)
        # affichage
        self.contenu.pack(side="top", expand="y", fill="both", padx=10, pady=10)
        self.cadre_entete.pack(side="top", fill="both", padx=60, pady=10)
        self.cadre_corp.pack(side="top", padx=3, pady=3)
        self.cadre_ppage.pack(side="top", fill="x", padx=3, pady=10)
        self.cadrenumetu.pack(fill="both", expand="yes")
        self.cadrelib.pack(fill="both", expand="yes")
        self.cadreinfo.pack(side="left", fill="both", expand="yes", pady=20)
        self.cadreinfoL.pack(side="left", fill="both", expand="yes")
        self.cadreinfoR.pack(side="right", fill="both", expand="yes")
        self.cadraction.pack(side="bottom", fill="both", expand="no")
        self.cadrecom.pack(side="right", fill="both", expand="yes")

        self.welcome_label.pack(padx=10, pady=10)
        self.numetu_label.pack(side='left')
        self.bouton_recherche.pack(side='right')
        self.nom_label.pack()
        self.prenom_label.pack()
        self.date_naissance_label.pack()
        self.niveau_etude_label.pack()
        self.num_tel_label.pack()
        self.suspension_label.pack()
        self.commentaire_label.pack()

        self.numetu_champ.pack(side='left')
        self.nom_champ.pack(pady=1)
        self.prenom_champ.pack(pady=1)
        self.date_naissance_champ.pack(pady=1)
        self.niveau_etude_champ.pack(pady=1)
        self.num_tel_champ.pack(pady=1)
        self.suspension_champ.pack(pady=1)
        self.commentaire_champ.pack()

        self.bouton_ajout.pack(side='left')
        self.bouton_suppr.pack(side='left')
        self.bouton_maj.pack(side='left')

        self.ver_label.pack(side='right')
        self.bouton_quitter.pack(side="left")

    # --------------------Methodes requête de contrôle dans la base de données ----------------------------
    def exist_Lect(self):
        """Methode qui verifie l'existance d' un num_etudiant dans la base de donnee et retourne une liste de tuple de 
        contenant les valeurs de chaque champ ou NONE si non trouvé.
        """
        requetesql = """SELECT * FROM lecteurs WHERE num_etudiant = ? """
        param = self.numetu_champ.get(),
        if (lecture(requetesql, param) == []):
            return None
        else:
            return lecture(requetesql, param)

    def lect_checkemprunt(self):
        """Methode qui verifie l'existence d'un numero étudiant dans la table relation
        """
        requetesql = """SELECT * FROM relation WHERE id_lecteur = ? """
        param = self.numetu_champ.get(),
        if (lecture(requetesql, param) == []):
            return None
        else:
            return lecture(requetesql, param)

    # -----------Ajout/suppression dans une base de données.---------
    def enregistrer_lect(self):
        """Methode qui ajoute une entrée (si elle n'existe pas deja) dans la table exemplaires en remplissant tout les
         champs.
        """
        if (self.exist_Lect() is None and re.match(r"(^[0-9])", self.numetu_champ.get()) is not None):
            # si le num_etudiant n'existe pas dans sa table ou
            requetesql = """INSERT INTO lecteurs(num_etudiant, nom, prenom, date_naissance, niveau_etude, num_tel, 
            suspension, commentaire) VALUES(?,?,?,?,?,?,?,?)"""
            param = self.numetu_champ.get(), self.nom_champ.get(), self.prenom_champ.get(),\
                self.date_naissance_champ.get(), self.niveau_etude_champ.get(), self.num_tel_champ.get(),\
                None, self.commentaire_champ.get(1.0, tk.END),
            ecriture(requetesql, param)
            print("Le lecteur a été ajouté dans la base de données")
        else:
            msg.showinfo('Impossible', "Lecteur déjà inscrit ou id incorrect", parent=self.master)

    def supprimer_lect(self):
        """Methode qui retire une entrée (si elle existe) de la table lecteurs a condition que ce dernier n'ait pas
         d'emprunt en cours.
        """
        if (self.exist_Lect() is not None):  # si le lecteur existe dans sa table
            if (self.lect_checkemprunt() is None):  # si le lecteur n'a pas d'emprunt(s) en cours
                requetesql = """DELETE FROM lecteurs WHERE num_etudiant = ?"""
                param = self.numetu_champ.get(),
                ecriture(requetesql, param)
                print("Le lecteur a été supprimée de la base de données")
            else:
                msg.showinfo('Impossible', "un ou plusieurs exemplaire(s) non rendu(s)", parent=self.master)
        else:
            msg.showinfo('Impossible', "Lecteur inexistant", parent=self.master)

    # -----------Modification dans la base de données.---------
    def maj_lect(self):
        """Methode qui met a jour tout les champ d'une entrée dans la base de donnée (si le numero etudiant y existe)
        de la table exemplaire.
        """
        if (self.exist_Lect() is not None):  # si le numero etudiant existe dans sa table
            requetesql = """UPDATE lecteurs SET nom = ? WHERE num_etudiant = ? """
            param = self.nom_champ.get(), self.numetu_champ.get(),
            ecriture(requetesql, param)
            requetesql = """UPDATE lecteurs SET prenom = ? WHERE num_etudiant = ? """
            param = self.prenom_champ.get(), self.numetu_champ.get(),
            ecriture(requetesql, param)
            requetesql = """UPDATE lecteurs SET date_naissance = ? WHERE num_etudiant = ? """
            param = self.date_naissance_champ.get(), self.numetu_champ.get(),
            ecriture(requetesql, param)
            requetesql = """UPDATE lecteurs SET niveau_etude = ? WHERE num_etudiant = ? """
            param = self.niveau_etude_champ.get(), self.numetu_champ.get(),
            ecriture(requetesql, param)
            requetesql = """UPDATE lecteurs SET num_tel = ? WHERE num_etudiant = ? """
            param = self.num_tel_champ.get(), self.numetu_champ.get(),
            ecriture(requetesql, param)
            # requetesql = """UPDATE lecteurs SET suspension = ? WHERE num_etudiant = ? """
            # param = self.suspension_champ.get(), self.numetu_champ.get(),
            # ecriture(requetesql, param)  !!!Provoque une erreur sur la Maj des suspension!!!
            requetesql = """UPDATE lecteurs SET commentaire = ? WHERE num_etudiant = ? """
            param = self.commentaire_champ.get(1.0, tk.END), self.numetu_champ.get(),
            ecriture(requetesql, param)
            print("Les informations isbn ont été mis a jour dans la base de données")
        else:
            msg.showinfo('Impossible', "Numero étudiant inexistant", parent=self.master)

    # -----------Recherche & conditionnement de l'objet---------
    def get_liste_BDD(self, champwhere="num_etudiant"):
        """ Methode qui, selon le champ de recherche specifié en argument, recherche dans la table lecteurs
        la valeur specifié en argument et stock la réponse sous forme d'une liste de tuple dans un attribut
        static propre a la classe.
        :champwhere: le champ a specifier dans lequelle la valeur sera recherché(num_etudiant par defaut)
        """
        if (self.numetu_champ.get() == ''):
            msg.showinfo('Erreur', "Veuillez specifier un numero etudiant. ", parent=self.master)
            return
        requetesql = """SELECT * FROM lecteurs WHERE """ + champwhere + """ REGEXP ? """
        param = self.numetu_champ.get(),
        fetch = lecture(requetesql, param)
        if (fetch == [] or fetch is None):
            msg.showinfo('Resultat', "Aucun resultat(s)", parent=self.master)
            return
        else:
            self.liste_recherche = lecture(requetesql, param)
            print(self.liste_recherche)

    def set_from_liste(self, i=0):
        """ Methode qui conditionne l'objet a partir d'un tuple de la liste d recherche
        :i: numero du tuple dans la liste de recherche (1er occurence par defaut)
        """
        self.num_etudiant.set(self.liste_recherche[i][0])
        self.nom.set(self.liste_recherche[i][1])
        self.prenom.set(self.liste_recherche[i][2])
        self.date_naissance.set(self.liste_recherche[i][3])
        self.niveau_etude.set(self.liste_recherche[i][4])
        self.num_tel.set(self.liste_recherche[i][5])
        self.suspension.set(self.liste_recherche[i][6])
        self.commentaire_champ.delete(1.0, tk.END)
        self.commentaire_champ.insert(1.0, str(self.liste_recherche[i][7]))

        print(self.num_etudiant, self.nom, self.prenom, self.date_naissance, self.niveau_etude, self.num_tel,
              self.suspension, self.commentaire)

    def listing(self):
        """methode pour afficher le contenu de la rechereche """
        self.get_liste_BDD()
        self.set_from_liste()
