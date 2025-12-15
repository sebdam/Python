from random import randint
from enum import Enum

class choix(Enum):
    Pierre  =1
    Feuille =2
    Ciseaux =3

def saisieNom():
    pseudo = str(input("Entrez votre pseudo : "))
    return pseudo

def choixOrdi() -> choix :
    a=randint(1,3)
    return choix(a)

def choixJoueur() -> choix :
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

def partie(choixJoueur: int, choixOrdi: int) -> int:
    r=int(choixJoueur)-int(choixOrdi)
    if r==0 :
        return None
    elif r==-1 or r==2:
        return 2
    elif r==-2 or r==1:
        return 1

def jouerJanken():
    joueur = choixJoueur()
    ordi = choixOrdi()
    resultat = partie(joueur.value,ordi.value)
    print("Vous avez choisis : ",joueur.name)
    print("L'ordi a choisis : ",ordi.name)

    msg = "gagné !"
    if not resultat :
        msg = "match null !"
    elif resultat == 2:
        msg = "perdu !"
    
    print("===================> RESULTAT : ",msg,"<===================")

pseudo = saisieNom()
print("Bienvenu ", pseudo, " !")

jouerJanken()