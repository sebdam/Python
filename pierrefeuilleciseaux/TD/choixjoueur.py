from enum import Enum

class choix(Enum):
    Pierre  =1
    Feuille =2
    Ciseaux =3

def choixJoueur():

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

votreChoix = choixJoueur()
print("Vous avez choisis : ",votreChoix.name)