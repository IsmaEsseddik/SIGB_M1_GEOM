import tkinter as tk
import datetime as dt  # pour les operation sur le temps
from InitialisationBDD import *
import tkinter.messagebox as msg  # pour les messagebox  de notifications
import tkinter.simpledialog as msg2  # pour les messagebox de saisie


class Emprunt:
    """ Interface graphique relative à la gestion de la table relation de la base de données
        pour un emprunt d'exemplaire"""

    def __init__(self, master):
        """constructeur de l'interface graphique"""
        # ------------------- Atrributs objets -------------------------
        self.id_lecteur = tk.IntVar(master, value='')
        self.nom = tk.StringVar(master, value=None)
        self.prenom = tk.StringVar(master, value=None)
        self.id_exemplaire = tk.IntVar(master, value='')
        self.date_emprunt = None
        self.date_retour = None
        self.liste_d_emprunt = []
        # ------------------ Attributs graphiques -------------------------
        self.master = master  # creation d'une simple fenêtre.
        self.master.attributes("-fullscreen", False)  # pour metre en fullscreen.
        self.master.geometry('800x600+0+0')  # pour la taille et le positionnement initiale.
        self.master.state('zoomed')  # pour maximiser la fenetre.
        self.master['bg'] = 'bisque'  # pour le background en couleur gris.
        self.master.title("Gest_Biblio - Gestionnaire de lecteurs")  # pour donner un titre a l'application.
        # creation du conteneur principale
        self.contenu = tk.PanedWindow(self.master, orient="vertical", borderwidth=3, relief="sunken", bg='#d8d8d8')
        # creation des cadres
        self.cadre_entete = tk.Frame(self.contenu, borderwidth=3, relief="raised", bg='#16eff4')
        self.cadre_corp = tk.Frame(self.contenu,  bg='#d8d8d8')
        self.cadre_ppage = tk.Frame(self.contenu, bg='#d8d8d8')
        self.cadrenumetu = tk.LabelFrame(self.cadre_corp, text="Etudiant", bg='#d8d8d8')
        self.cadrecodebar = tk.LabelFrame(self.cadre_corp, text='Exemplaire', bg='#d8d8d8')
        self.cadremprunt = tk.LabelFrame(self.cadre_corp, text="Informations", borderwidth=5,
                                         relief="sunken", bg="#d8d8d8", labelanchor='n')
        # creation d'une barre de defilement
        self.scrolling = tk.Scrollbar(self.cadremprunt)

        # creation de libellés
        self.welcome_label = tk.Label(self.cadre_entete, text="Emprunt d'exemplaire", bg='#16eff4')
        self.numetu_label = tk.Label(self.cadrenumetu, text="Numero Etudiant: ", bg='#d8d8d8')
        self.nom_label = tk.Label(self.cadrenumetu, text="Nom: ", bg='#d8d8d8')
        self.prenom_label = tk.Label(self.cadrenumetu, text="Prenom: ", bg='#d8d8d8')

        self.codebar_label = tk.Label(self.cadrecodebar, text="Codebar", bg='#d8d8d8')
        self.ver_label = tk.Label(self.cadre_ppage, text="Esseddik Ismael, M1 Geomatique ENSG, ©2017",
                                  fg='blue', bg='#d8d8d8')
        # creation de champs
        self.numetu_champ = tk.Entry(self.cadrenumetu, textvariable=self.id_lecteur, width=50, justify='center',
                                     state='disabled')
        self.nom_champ = tk.Entry(self.cadrenumetu, textvariable=self.nom, width=50, justify='center',
                                  state='disabled')
        self.prenom_champ = tk.Entry(self.cadrenumetu, textvariable=self.prenom, width=50, justify='center',
                                     state='disabled')
        self.codebar_champ = tk.Entry(self.cadrecodebar, textvariable=self.id_exemplaire, width=50, justify='center')
        self.logemprunt = tk.Text(self.cadremprunt, bg="#d8d8d8", wrap="word", yscrollcommand=self.scrolling.set,
                                  state="disabled")
        # creation boutons
        self.bouton_numetu = tk.Button(self.cadrenumetu, text='Changer lecteur', command=self.get_lecteur)
        self.bouton_emprunt = tk.Button(self.cadrecodebar, text='Emprunt', command=self.enregistrer_emprunt)
        self.bouton_prolongement = tk.Button(self.cadrecodebar, text='Prolongement', command=self.prolongement)
        self.bouton_listemprunt = tk.Button(self.cadrenumetu, text="Liste d'Emprunts", command=self.lister_emprunt)
        self.bouton_quitter = tk.Button(self.cadre_ppage, text="Quitter", command=self.master.destroy)
        # affichage
        self.contenu.pack(side="top", expand="y", fill="both", padx=10, pady=10)
        self.cadre_entete.pack(side="top", fill="both", padx=60, pady=10)
        self.cadre_corp.pack(side="top", padx=3, pady=3)
        self.cadre_ppage.pack(side="bottom", fill="x", padx=3, pady=10)
        self.cadrenumetu.pack(side='top', fill="both", expand="yes")
        self.cadrecodebar.pack(side='top', fill="both", expand="yes")
        self.cadremprunt.pack(fill="both", expand="yes")
        self.welcome_label.pack(padx=10, pady=10)
        self.numetu_label.pack(side='left')
        self.numetu_champ.pack(side='left')
        self.nom_label.pack(side='left')
        self.nom_champ.pack(side='left')
        self.prenom_label.pack(side='left')
        self.prenom_champ.pack(side='left')
        self.codebar_label.pack(side='left')
        self.codebar_champ.pack(side='left')
        self.scrolling.pack(side='right', fill='y')
        self.logemprunt.pack()
        self.bouton_numetu.pack(side='top')
        self.bouton_listemprunt.pack(side='top')
        self.bouton_emprunt.pack(side='right')
        self.bouton_prolongement.pack(side='right')

        self.ver_label.pack(side='right')
        self.bouton_quitter.pack(side="left")
        self.get_lecteur()

    # --------------------Methodes requête de contrôle dans la base de données ----------------------------
    def exist_idLect(self):
        """Methode qui verifie l'existance d'un num_etudiant dans la table lecteurs et retourne une liste de tuple 
        contenant les valeurs de chaque champ ou NONE si non trouvé.
        """
        requetesql = """SELECT * FROM lecteurs WHERE num_etudiant = ? """
        param = self.numetu_champ.get(),  # valeur saisie dans le champ de la fenetre
        return lecture(requetesql, param)

    def idlect_checkSuspension(self):
        """Methode qui retourne la valeur de la suspension d'un lecteur en booléen.
        """
        requetesql = """SELECT suspension FROM lecteurs WHERE num_etudiant = ? """
        param = self.numetu_champ.get(),
        suspension = lecture(requetesql, param)
        return suspension[0][0]  # retourne la valeur precise du champ

    def idlect_checkemprunt(self):
        """Methode qui recherche et renvoie la liste de tout les emprunt du lecteur depuis la table relation
        """
        requetesql = """SELECT * FROM relation WHERE id_lecteur = ? """
        param = self.numetu_champ.get(),
        return lecture(requetesql, param)

    def exist_idexemp(self):
        """Methode qui verifie l'existance d'un codebar dans la base de donnee et retourne une liste de tuple contenant
        les valeurs de chaque champ ou NONE si non trouvé."""
        requetesql = """SELECT * FROM exemplaires WHERE codebar = ? """
        param = self.codebar_champ.get(),
        return lecture(requetesql, param)

    def idexemp_checkemprunt(self):
        """Methode qui renvoie l'etat d'emprunt du livre en booléen."""
        requetesql = """SELECT emprunt FROM exemplaires WHERE codebar = ? """
        param = self.codebar_champ.get(),
        emprunt = lecture(requetesql, param)
        return bool(emprunt[0][0])

    def check_prolongement(self):
        """Methode qui renvoie l'eat du prolongement du livre en booléen."""
        requetesql = """SELECT prolongement FROM relation WHERE id_exemplaire = ? """
        param = self.codebar_champ.get(),
        emprunt = lecture(requetesql, param)
        return bool(emprunt[0][0])

    # -----------Methode pour selectionner un lecteur ---------
    def get_lecteur(self):
        """Methode qui recherche dans la table lecteurs un numero etudiant, l'affecte a l'attribut "id_lecteur"
        et la liste des exemplaires qu'il a emprunté en affichant les avertissements, a condition que
        le lecteur existe dans la base de données.
        """
        v = msg2.askinteger('Saisie', 'Entrer un numero etudiant', parent=self.master)
        # enregistrement de la saisie dans une variable
        self.id_lecteur.set(v)  # affectation de la saisie a l'attribut
        if (self.exist_idLect() != []):  # si le lecteur a été trouvé,
            if (self.idlect_checkSuspension() is not None):  # on affiche des avertissements si necessaire
                msg.showinfo('Information', "Attention, le lecteur est suspendu ", parent=self.master)
            if (len(self.idlect_checkemprunt()) >= 5):
                msg.showinfo('Information', "Attention, limite d'emprunt atteinte ", parent=self.master)
            self.liste_d_emprunt = self.idlect_checkemprunt()  # affectation de la liste des emprunt
            print(self.liste_d_emprunt)
            requetesql = """SELECT nom FROM lecteurs WHERE num_etudiant = ? """
            param = self.numetu_champ.get(),
            self.nom.set(lecture(requetesql, param)[0][0])
            requetesql = """SELECT prenom FROM lecteurs WHERE num_etudiant = ? """
            param = self.numetu_champ.get(),
            self.prenom.set(lecture(requetesql,param)[0][0])  # affectation des attributs nom prenom
        else:
            msg.showinfo('Information', "Lecteur introuvable !", parent=self.master)
            self.id_lecteur.set('')  # supression du numero etudiant
            self.master.destroy()  # fermeture de la fenetre

    # -----------Methode pour effectuer un emprunt ---------
    def enregistrer_emprunt(self):
        """Methode qui recherche dans la table exemplaires un codebar et procede a l'emprunt, a condition qu'il ne soit 
        pas emprunté, que le lecteur concerné ne soit pas suspendu et n'ait pas atteint sa limite d'emprunt.
        """
        if (self.idlect_checkSuspension() is None):  # si le lecteur n'est pas suspendu
            if (len(self.idlect_checkemprunt()) < 5):  # si le lecteur n'a pas atteint sa limite d'emprunt
                if (self.exist_idexemp() != []):  # si l'exemplaire existe
                    if (self.idexemp_checkemprunt() is False):  # si l'exemplaire n'est pas emprunté
                        requetesql = """UPDATE exemplaires SET emprunt = 1 WHERE codebar = ? """
                        param = self.codebar_champ.get(),
                        ecriture(requetesql, param)  # changement du statut du livre
                        self.date_emprunt = datetime.date.today()  # attribution de la date du jour
                        self.date_retour = datetime.date.today() + datetime.timedelta(6)
                        # calcul attribution de la date de retour
                        requetesql = """INSERT INTO relation(date_emprunt, date_retour, id_lecteur, id_exemplaire) 
                        VALUES(?,?,?,?)"""
                        param = self.date_emprunt, self.date_retour, self.numetu_champ.get(), self.codebar_champ.get(),
                        ecriture(requetesql, param)  # ajout d'une entrée dans la table relation
                        self.liste_d_emprunt = self.idlect_checkemprunt()  # Màj de l'attribut liste d'emprunt
                        print('exemplaire emprunté')

                        # ---------------- affichage des informations sur l'emprunt ------------------------
                        requetesql = """SELECT * FROM relation WHERE id_exemplaire = ?"""
                        param = self.codebar_champ.get(),
                        relat = lecture(requetesql, param)
                        date_e, date_r, numetu = relat[0][0], relat[0][1], relat[0][2]

                        requetesql = """SELECT nom, prenom FROM lecteurs WHERE num_etudiant = ?"""
                        param = numetu,
                        info_lect = lecture(requetesql, param)
                        nom, prenom = info_lect[0][0], info_lect[0][1]

                        requetesql = """SELECT exemp_isbn FROM exemplaires WHERE codebar = ?"""
                        param = self.codebar_champ.get(),
                        isbn_ex = lecture(requetesql, param)
                        requetesql = """SELECT titre, auteur FROM infos_documents WHERE isbn = ?"""
                        param = isbn_ex[0][0],
                        info_exemp = lecture(requetesql, param)
                        titre, auteur = info_exemp[0][0], info_exemp[0][1]
                        self.logemprunt.config(state="normal")  # on active le log pour pouvoir le modifier
                        self.logemprunt.insert(tk.END, "--------\nTitre : " + titre + "| Auteur : " + auteur +
                                               "| Emprunteur : " + nom + '_' + prenom + "| durée : " + date_e +
                                               " --> " + date_r + "\nExemplaire emprunté")
                        self.logemprunt.config(state="disabled")  # infos inséré : on desactive la modification du log
                    else:
                        msg.showerror('Impossible', "Exemplaire deja emprunté", parent=self.master)
                else:
                    msg.showerror('Impossible', "Exemplaire introuvable !", parent=self.master)
                    self.id_exemplaire.set('')  # supression du codebar
            else:
                msg.showerror('Impossible', "Limite d'emprunt atteinte !", parent=self.master)
        else:
            msg.showerror('Impossible', "Lecteur suspendu non autorisé a emprunter!", parent=self.master)

    # -----------Methode pour effectuer un prolongement ---------
    def prolongement(self):
        """Methode qui effectue un prolongement de six jour sur l'exemplaire designé
        """
        if (self.codebar_champ.get() == ''):  # si aucune saisie
            msg.showinfo('Erreur', "Veuillez specifier un codebar ", parent=self.master)
            return  # problem sur la verif de l'existence de l'emprunt par rapport au lecteur

        if (self.idlect_checkSuspension() is None):  # si le lecteur n'est pas suspendu
            if (self.idexemp_checkemprunt() is True):  # si l'exemplaire est emprunté
                if (self.check_prolongement() is False):  # si l'exemplaire n'a pas deja été prolongé
                    requetesql = """UPDATE relation SET prolongement = 1 WHERE id_exemplaire = ? """
                    param = self.codebar_champ.get(),
                    ecriture(requetesql, param)  # requetesql pour changement de statut du prolongement
                    self.date_retour = dt.datetime(int(self.date_retour[0:4]), int(self.date_retour[5:7]),
                                                   int(self.date_retour[8:10])) + dt.timedelta(6)
                    # calcul & attribution de la nouvelle date de retour.
                    requetesql = """UPDATE relation SET date_retour = ? WHERE id_exemplaire = ? """
                    param = self.date_retour, self.codebar_champ.get(),
                    ecriture(requetesql, param)  # requetesql ajout d'un champ
                    self.logemprunt.config(state="normal")
                    self.logemprunt.insert(tk.END,
                                           "--------\nProlongement effectué")
                    self.logemprunt.config(state="disabled")
                else:
                    msg.showerror('Impossible', "un seul prolongement par emprunt autorisé", parent=self.master)
            else:
                msg.showerror('Impossible', "exemplaire non emprunté", parent=self.master)
        else:
            msg.showerror('Impossible', "Lecteur suspendu non autorisé a prolonger!", parent=self.master)

    def lister_emprunt(self):
        """methode pour afficher la liste des documents """
        self.liste_d_emprunt = self.idlect_checkemprunt()  # mise a jour de la liste
        self.logemprunt.config(state="normal")
        numero = 1  # numero du document dans la liste
        self.logemprunt.insert(tk.END, "----Liste d'emprunt----\n") # insertion de texte en-tête
        for i in self.liste_d_emprunt:  # pour chaque document de la liste
            print(i)
            requetesql = """SELECT exemp_isbn FROM exemplaires WHERE codebar = ?"""
            param = i[3],
            isbn_ex = lecture(requetesql, param)
            requetesql = """SELECT titre, auteur FROM infos_documents WHERE isbn = ?"""
            param = isbn_ex[0][0],
            info_exemp = lecture(requetesql, param)
            titre, auteur = info_exemp[0][0], info_exemp[0][1]  # recuperation des informations et ajout dans le log
            self.logemprunt.insert(tk.END, str(numero)+" - Titre : " + titre + "| Auteur : " + auteur +
                                   "| durée : " + i[0] + " --> " + i[1] + "\n")
            numero+=1

        self.logemprunt.config(state="disabled")
