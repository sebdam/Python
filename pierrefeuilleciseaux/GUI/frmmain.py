from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from frmresultjeux import FrmResultJeux
from frmresulttests import FrmResultTests

import pierrefeuilleciseaux_module as jeux

class FrmMain():

    #########################################################################################
    #       Constructeur de la class FrmMain                                                #
    #########################################################################################
    def __init__(self, root : Tk) -> None:

        self.root = root

        self.style = ttk.Style()
        self.style.map("C.TButton",
            foreground=[('pressed', 'black'), ('active', 'blue')],
            background=[('pressed', '!disabled', 'black'),('active', 'white')])

        root.grid_rowconfigure(0,weight=1)
        root.grid_columnconfigure(0,weight=1)

        #layer principale
        self.frame = Frame(root)
        self.frame.grid(column=0, row=0, sticky = "nsew")

        self.frame.rowconfigure(tuple(range(4)), weight=1)
        self.frame.columnconfigure(tuple(range(3)), weight=1)

        #composants
        lbl = Label(self.frame, text="Bienvenue pour jouer à pierre feuille ciseaux !")
        lbl.grid(column=0, columnspan=3, row=0, sticky="nsew")

        lblJeux = Label(self.frame, text="Choisis pour jouer :")
        lblJeux.grid(column=0, row=1, sticky="nse")

        self.comboChoix = ttk.Combobox(self.frame)
        self.comboChoix['values'] = [jeux.choix.Pierre.name,jeux.choix.Feuille.name,jeux.choix.Ciseaux.name]
        self.comboChoix['state'] = 'readonly'
        self.comboChoix.grid(column=1,row=1)

        btnPlay = ttk.Button(self.frame, text ="Jouer", command = self.playBtnCallback, style="C.TButton")
        btnPlay.grid(column=2, row=1, sticky="e", padx=10, pady=10)

        lblTest = Label(self.frame, text="Nombre de tests à réaliser :")
        lblTest.grid(column=0, row=2, sticky="nse")

        self.entryTests = Entry(self.frame)
        self.entryTests.grid(column=1,row=2)

        btnTest = ttk.Button(self.frame, text ="Tester", command = self.testBtnCallback, style="C.TButton")
        btnTest.grid(column=2, row=2, sticky="e", padx=10, pady=10)

        btn = ttk.Button(self.frame, text ="Quit", command = root.destroy, style="C.TButton")
        btn.grid(column=2, row=3, sticky="se", padx=10, pady=10)

        #affichage de la form
        root.title('Pierre Feuille Ciseaux !')
        root.geometry('600x300')
        self.frame.mainloop()

    #########################################################################################
    #       Callback du bouton Test                                                         #
    #########################################################################################
    def testBtnCallback(self) ->None:
        entry = self.entryTests.get()
        if not entry or not int(entry) :
            messagebox.showerror("Erreur", "Vous devez entrer le nombre de tests à résliser (en chiffres)!")
        
        result = self.test(int(entry))

        resultroot = Toplevel()
        FrmResultTests(resultroot, result)
        resultroot.transient(self.root)
        resultroot.grab_set()
        self.root.wait_window(resultroot)

    #########################################################################################
    #       Callback du bouton Jouer                                                        #
    #########################################################################################
    def playBtnCallback(self) ->None:
        selected = self.comboChoix.get()
        if not selected :
            messagebox.showerror("Erreur", "Vous devez choisir ce que vous voulez jouer!")
        
        entry = jeux.choix[selected]
        if not entry :
            messagebox.showerror("Erreur", "Vous devez choisir ce que vous voulez jouer!")
        
        result = self.play(entry)

        resultroot = Toplevel()
        FrmResultJeux(resultroot, result)
        resultroot.transient(self.root)
        resultroot.grab_set()
        self.root.wait_window(resultroot)

    #########################################################################################
    #       Méthode de Test                                                                 #
    #########################################################################################
    def test(self, nbTests:int):
        nbNull=0
        nbOrdi1=0
        nbOrdi2=0

        count = {
            jeux.choix.Pierre:0,
            jeux.choix.Feuille:0,
            jeux.choix.Ciseaux:0
        }

        for i in range(1,nbTests+1) :
            joueur = jeux.choixOrdi()
            count[joueur]+=1
            ordi = jeux.choixOrdi()
            count[ordi]+=1

            resultat = jeux.partie(joueur.value,ordi.value)
            if(resultat==1) :
                nbOrdi1+=1
            elif(resultat==2):
                nbOrdi2+=1
            else:
                nbNull+=1
        
        return {
            "1":nbOrdi1,
            "2":nbOrdi2,
            "null":nbNull,
            "parties":nbTests,
            "totalCount":count
        }

    #########################################################################################
    #       Méthode de jeux                                                                 #
    #########################################################################################
    def play(self, joueur:jeux.choix):
        ordi = jeux.choixOrdi()
        resultat = jeux.partie(joueur.value,ordi.value)

        return {
            "choixJoueur":joueur,
            "choixOrdi":ordi,
            "resultat":resultat
        }