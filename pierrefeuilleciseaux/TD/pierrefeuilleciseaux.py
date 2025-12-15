from random import choice
from enum import Enum
import os
import numpy as np

#########################################################################################
#       Parametres globaux                                                              #
#########################################################################################
nbTestsMin = 1
nbTestsMax = 10000


#########################################################################################
#       Méthode permettant de vider la console                                          #
#########################################################################################

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

#########################################################################################
#       Entités : objet qui représente la pierre, la feuille ou le ciseau               #
#       Ca permet de créer son propre type représentant la pierre, feuille ou le ciseau #
#########################################################################################

class choix(Enum):
    Pierre  =1 # la pierre vaudra 1 (int) partout
    Feuille =2 # la feuille vaudra 2 partout
    Ciseaux =3 # le ciseau vaudra 3 partout

#########################################################################################
#       Méthode de saisie du pseudo                                                     #
#########################################################################################

def saisieNom():
    pseudo = str(input("Entrez votre pseudo : "))
    return pseudo

#########################################################################################
#       Méthode de choix pour le joueur                                                 #
#       - si pourOrdi == true, le choix est fait au hasard                              #
#########################################################################################

def choixJoueur(pourOrdi = False) -> choix :
    
    if pourOrdi:
        #return choice([choix.Pierre, choix.Feuille, choix.Ciseaux])
        return choix(rng.integers(1,4))

    listeChoix = ""
    for unchoix in choix:
        if not listeChoix :
            listeChoix += str(unchoix.value) + " => " + unchoix.name
        else :
            listeChoix += " ou " + str(unchoix.value) + " => " + unchoix.name

    n=int(input("Que voulez vous jouer ("+listeChoix+") :"))
    while n!=1 and n!=2 and n!=3:
        n=int(input("Non ! vous devez choisir "+listeChoix+" ! Faites votre choix :"))
    return choix(n)


#########################################################################################
#       Méthode de dénouement d'une partie                                              #
#       On lui passe le choix de chaque joueur et elle renvoie le N° du gagnant         #
#       ou None en cas de match null                                                    #
#########################################################################################

def partie(choixJoueur: int, choixOrdi: int) -> int:
    r=int(choixJoueur)-int(choixOrdi)
    if r==0 :
        return None
    elif r==-1 or r==2:
        return 2
    elif r==-2 or r==1:
        return 1

#########################################################################################
#       Méthode de déroulement d'un partie complette :                                  #
#        - si en mode test : choix du premier joueur fait comme celui de l'ordi         #
#        - choix de l'ordi                                                              #
#        - dénouement                                                                   #
#        - si PAS mode test : impréssion du résultat                                    #
#       Renvoie le résultat : N° du gagnant ou None si match null                       # 
#########################################################################################

def jouerJanken(test = False) -> int:
    joueur = choixJoueur(test)
    ordi = choixJoueur(True)

    resultat = partie(joueur.value,ordi.value)
    if test==False:
        print("Vous avez choisis : ",joueur.name)
        print("L'ordi a choisis : ",ordi.name)

        msg = "gagné !"
        if not resultat :
            msg = "match null !"
        elif resultat == 2:
            msg = "perdu !"
    
        print("===================> RESULTAT : ",msg,"<===================")

    return resultat

#########################################################################################
#       Méthode de test d'une partie complette :                                        #
#        - choix du nombre de partie de test à réaliser                                 #
#        - exécution des parties de tests                                               #
#        - calcul et impréssion des stats                                               # 
#########################################################################################

def test():
    nbTests = int(input("Entrez le nombre de tests à réaliser ("+str(nbTestsMin)+" à "+str(nbTestsMax)+") : "))
    while nbTests <nbTestsMin or nbTests>nbTestsMax:
        nbTests = int(input("Non ! Entrez le nombre de tests à réaliser ("+str(nbTestsMin)+" à "+str(nbTestsMax)+") : "))

    nbNull=0
    nbOrdi1=0
    nbOrdi2=0

    for i in range(1,nbTests+1) :
        resultat = jouerJanken(True)
        if(resultat==1) :
            nbOrdi1+=1
        elif(resultat==2):
            nbOrdi2+=1
        else:
            nbNull+=1
    
    print("Matchs null : ",nbNull,"/",nbTests," => ", round((nbNull/nbTests)*100,2),"%")
    print("Ordi 1      : ",nbOrdi1,"/",nbTests," => ",round((nbOrdi1/nbTests)*100,2),"%")
    print("Ordi 2      : ",nbOrdi2,"/",nbTests," => ",round((nbOrdi2/nbTests)*100,2),"%")

#########################################################################################
#       Branche principale (main)                                                       #
#########################################################################################

#initialisation du moteur de nombres aléatoires de numpy
rng = np.random.default_rng(12345)

pseudo = saisieNom()
print("Bienvenu ", pseudo, " !")

while 1 :
    mode = input(pseudo + " : que voulez vous faire ? Jouer (j), lancer des tests (t) ou quitter (q) : ")
    while(mode!="j" and mode!="t" and mode!="q") :
        mode = input("Non " + pseudo + " : que voulez vous faire ? Jouer (j), lancer des tests (t) ou quitter (q) : ")
        
    if mode=="j" :
        jouerJanken()
        #pour faire une pause aprés le jeux
        input("->> Tapper une touche pour continuer <<-")
        cls()
    elif mode=="t":
        test()
        #pour faire une pause aprés le test
        input("->> Tapper une touche pour continuer <<-")
        cls()
    else :
        cls()
        exit()