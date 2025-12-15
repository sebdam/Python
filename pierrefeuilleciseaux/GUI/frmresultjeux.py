from enum import Enum
from tkinter import *
from tkinter import ttk
from PIL import ImageTk,Image

import pierrefeuilleciseaux_module as jeux

class FrmResultJeux():
    #########################################################################################
    #       Constructeur de la class FrmResultJeux                                          #
    #########################################################################################
    def __init__(self, root : Tk, resultat) -> None:

        self.initImages(resultat)

        self.style = ttk.Style()
        self.style.map("C.TButton",
            foreground=[('pressed', 'black'), ('active', 'blue')],
            background=[('pressed', '!disabled', 'black'),('active', 'white')])

        root.grid_rowconfigure(0,weight=1)
        root.grid_columnconfigure(0,weight=1)

        #layer principale
        self.frame = Frame(root)
        self.frame.grid(column=0, row=0, sticky = "nsew")

        self.frame.rowconfigure(tuple(range(5)), weight=1)
        self.frame.columnconfigure(tuple(range(2)), weight=1)

        #composants
        lbl = Label(self.frame, text="Résultats")
        lbl.grid(column=0, columnspan=2, row=0, sticky="nsew")

        lblJoueur = Label(self.frame, text="Vous")
        lblJoueur.grid(column=0, row=1, sticky="nsew")
        
        lblOrdi = Label(self.frame, text="L'ordi")
        lblOrdi.grid(column=1, row=1, sticky="nsew")

        self.canvasJoueur = Canvas(self.frame, bg="white", width = 120, height = 120)
        self.canvasJoueur.grid(column=0, row=2, sticky="nsew")
        self.photoImageJoueur = ImageTk.PhotoImage(self.imgJoueur)
        self.canvasImgJoueur = self.canvasJoueur.create_image(0,0, anchor=NW, image=self.photoImageJoueur)
        self.canvasJoueur.bind("<Configure>", self.resizeCanvasJoueur)

        self.canvasOrdi = Canvas(self.frame, bg="white", width = 120, height = 120)
        self.canvasOrdi.grid(column=1, row=2, sticky="nsew")
        self.photoImageOrdi = ImageTk.PhotoImage(self.imgOrdi)
        self.canvasImgOrdi = self.canvasOrdi.create_image(0,0, anchor=NW, image=self.photoImageOrdi)
        self.canvasOrdi.bind("<Configure>", self.resizeCanvasOrdi)

        textLblRes = "Gagné !"
        if resultat["resultat"] == None :
            textLblRes = "Ex aequo !"
        elif resultat["resultat"] == 2 :
            textLblRes = "Perdus !"
        lblRes = Label(self.frame, text=textLblRes)
        lblRes.grid(column=0, columnspan=2, row=3, sticky="nsew")

        btn = ttk.Button(self.frame, text ="Fermer", command = root.destroy, style="C.TButton")
        btn.grid(column=0, columnspan=2, row=4, pady=10)

        #parametrage de la form
        root.title('Résultats')
        root.geometry('300x300')

    #########################################################################################
    #       Initialisation des images                                                       #
    #########################################################################################
    def initImages(self, resultat) :
        self.imgPierre = Image.open("./Pierre.png")
        #print(self.imgPierre.mode)
        self.imgFeuille = Image.open("./Feuille.png")
        #print(self.imgFeuille.mode)
        self.imgCiseaux = Image.open("./Ciseaux.png")
        #print(self.imgCiseaux.mode)

        if resultat["choixJoueur"] == jeux.choix.Pierre :
            self.imgJoueur = self.imgPierre
        elif resultat["choixJoueur"] == jeux.choix.Feuille :
            self.imgJoueur = self.imgFeuille
        elif resultat["choixJoueur"] == jeux.choix.Ciseaux :
            self.imgJoueur = self.imgCiseaux

        if resultat["choixOrdi"] == jeux.choix.Pierre :
            self.imgOrdi = self.imgPierre
        elif resultat["choixOrdi"] == jeux.choix.Feuille :
            self.imgOrdi = self.imgFeuille
        elif resultat["choixOrdi"] == jeux.choix.Ciseaux :
            self.imgOrdi = self.imgCiseaux
    
    #########################################################################################
    #       Evenement de redimenssionnement du canvas du joueur                             #
    #########################################################################################
    def resizeCanvasJoueur(self, event):
        img = self.imgJoueur.resize(
            (event.width, event.height), Image.ANTIALIAS
        )
        self.photoImageJoueur = ImageTk.PhotoImage(img)
        self.canvasJoueur.itemconfig(self.canvasImgJoueur, image=self.photoImageJoueur)

    #########################################################################################
    #       Evenement de redimenssionnement du canvas de l'ordi                             #
    #########################################################################################
    def resizeCanvasOrdi(self, event):
        img = self.imgOrdi.resize(
            (event.width, event.height), Image.ANTIALIAS
        )
        self.photoImageOrdi = ImageTk.PhotoImage(img)
        self.canvasOrdi.itemconfig(self.canvasImgOrdi, image=self.photoImageOrdi)