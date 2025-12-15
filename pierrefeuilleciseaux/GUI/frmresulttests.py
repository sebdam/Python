from enum import Enum
from tkinter import *
from tkinter import ttk
from PIL import ImageTk,Image

import pierrefeuilleciseaux_module as jeux

class FrmResultTests():
    #########################################################################################
    #       Constructeur de la class FrmResultTests                                         #
    #########################################################################################
    def __init__(self, root : Tk, resultat) -> None:

        self.initImages()

        self.style = ttk.Style()
        self.style.map("C.TButton",
            foreground=[('pressed', 'black'), ('active', 'blue')],
            background=[('pressed', '!disabled', 'black'),('active', 'white')])

        root.grid_rowconfigure(0,weight=1)
        root.grid_columnconfigure(0,weight=1)

        #layer principale
        self.frame = Frame(root)
        self.frame.grid(column=0, row=0, sticky = "nsew")

        self.frame.rowconfigure(tuple(range(10)), weight=1)
        self.frame.columnconfigure(tuple(range(3)), weight=1)

        # composants

        ## Affichage des 3 images avec leur labels en dessous (nombre et ratio)
        lbl = Label(self.frame, text="Résultats")
        lbl.grid(column=0, columnspan=3, row=0, sticky="nsew")

        self.canvasPierre = Canvas(self.frame, bg="white", width = 120, height = 120)
        self.canvasPierre.grid(column=0, row=1, sticky="nsew")
        self.photoImagePierre = ImageTk.PhotoImage(self.imgPierre)
        self.canvasImgPierre = self.canvasPierre.create_image(0,0, anchor=NW, image=self.photoImagePierre)
        self.canvasPierre.bind("<Configure>", self.resizeCanvasPierre)

        lblPierres = Label(self.frame, 
            text=str(resultat["totalCount"][jeux.choix.Pierre]) + " (" +
                str(round((resultat["totalCount"][jeux.choix.Pierre]/resultat["parties"])*100,2)) + "%)")
        lblPierres.grid(column=0, row=2, sticky="nsew")

        self.canvasFeuille = Canvas(self.frame, bg="white", width = 120, height = 120)
        self.canvasFeuille.grid(column=1, row=1, sticky="nsew")
        self.photoImageFeuille = ImageTk.PhotoImage(self.imgFeuille)
        self.canvasImgFeuile = self.canvasFeuille.create_image(0,0, anchor=NW, image=self.photoImageFeuille)
        self.canvasFeuille.bind("<Configure>", self.resizeCanvasFeuille)

        lblFeuilles = Label(self.frame, 
            text=str(resultat["totalCount"][jeux.choix.Feuille]) + " (" +
                str(round((resultat["totalCount"][jeux.choix.Feuille]/resultat["parties"])*100,2)) + "%)")
        lblFeuilles.grid(column=1, row=2, sticky="nsew")

        self.canvasCiseaux = Canvas(self.frame, bg="white", width = 120, height = 120)
        self.canvasCiseaux.grid(column=2, row=1, sticky="nsew")
        self.photoImageCiseaux = ImageTk.PhotoImage(self.imgCiseaux)
        self.canvasImgCiseaux = self.canvasCiseaux.create_image(0,0, anchor=NW, image=self.photoImageCiseaux)
        self.canvasCiseaux.bind("<Configure>", self.resizeCanvasCiseaux)

        lblCiseaux = Label(self.frame, 
            text=str(resultat["totalCount"][jeux.choix.Ciseaux]) + " (" +
                str(round((resultat["totalCount"][jeux.choix.Ciseaux]/resultat["parties"])*100,2)) + "%)")
        lblCiseaux.grid(column=2, row=2, sticky="nsew")

        ## Affichage des 3 lignes de résultats pour l'ordi1, l'ordi2 et le match null (nombre et ratio et progessbar)
        ratio01 = resultat["1"]/resultat["parties"]
        lblO1 = Label(self.frame, text="Vistoires de l'ordi 1 :")
        lblO1.grid(column=0, columnspan=2, row=3, sticky="nsew")
        lblO1v = Label(self.frame, 
            text = str(resultat["1"]) + " (" + str(round(ratio01*100,2)) + "%)")
        lblO1v.grid(column=2, row=3, sticky="nsew")

        self.makeProgressBar(self.frame, 4, ratio01*100)

        ratio02 = resultat["2"]/resultat["parties"]
        lblO2 = Label(self.frame, text="Vistoires de l'ordi 2 :")
        lblO2.grid(column=0, columnspan=2, row=5, sticky="nsew")
        lblO2v = Label(self.frame, 
            text = str(resultat["2"]) + " (" + str(round(ratio02*100,2)) + "%)")
        lblO2v.grid(column=2, row=5, sticky="nsew")

        self.makeProgressBar(self.frame, 6, ratio02*100)

        ratioNull = resultat["null"]/resultat["parties"]
        lblNull = Label(self.frame, text="Parties ex eaquo :")
        lblNull.grid(column=0, columnspan=2, row=7, sticky="nsew")
        lblNullv = Label(self.frame, 
            text = str(resultat["null"]) + " (" + str(round(ratioNull*100,2)) + "%)")
        lblNullv.grid(column=2, row=7, sticky="nsew")
        
        self.makeProgressBar(self.frame, 8, ratioNull*100)

        btn = ttk.Button(self.frame, text ="Fermer", command = root.destroy, style="C.TButton")
        btn.grid(column=0, columnspan=3, row=9, pady=10)

        #parametrage de la form
        root.title('Résultats')
        root.geometry('400x400')

    #########################################################################################
    #       Initialisation des images                                                       #
    #########################################################################################
    def initImages(self) :
        self.imgPierre = Image.open("./Pierre.png")
        #print(self.imgPierre.mode)
        self.imgFeuille = Image.open("./Feuille.png")
        #print(self.imgFeuille.mode)
        self.imgCiseaux = Image.open("./Ciseaux.png")
        #print(self.imgCiseaux.mode)
    
    #########################################################################################
    #       Initialisation d'une progressbar                                                #
    #########################################################################################
    def makeProgressBar(self, frame:Frame, row:int, value) :
        progress = ttk.Progressbar(frame, orient=HORIZONTAL,mode="determinate")
        progress.grid(column=0,columnspan=3,row=row,sticky="nsew")
        progress["value"]=value

    #########################################################################################
    #       Evenement de redimenssionnement du canvas de la pierre                          #
    #########################################################################################
    def resizeCanvasPierre(self, event):
        img = self.imgPierre.resize(
            (event.width, event.height), Image.ANTIALIAS
        )
        self.photoImagePierre = ImageTk.PhotoImage(img)
        self.canvasPierre.itemconfig(self.canvasImgPierre, image=self.photoImagePierre)

    #########################################################################################
    #       Evenement de redimenssionnement du canvas de la feuille                         #
    #########################################################################################
    def resizeCanvasFeuille(self, event):
        img = self.imgFeuille.resize(
            (event.width, event.height), Image.ANTIALIAS
        )
        self.photoImageFeuille = ImageTk.PhotoImage(img)
        self.canvasFeuille.itemconfig(self.canvasImgFeuile, image=self.photoImageFeuille)
    
    #########################################################################################
    #       Evenement de redimenssionnement du canvas du ciseaux                            #
    #########################################################################################
    def resizeCanvasCiseaux(self, event):
        img = self.imgCiseaux.resize(
            (event.width, event.height), Image.ANTIALIAS
        )
        self.photoImageCiseaux = ImageTk.PhotoImage(img)
        self.canvasCiseaux.itemconfig(self.canvasImgCiseaux, image=self.photoImageCiseaux)