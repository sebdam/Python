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

def partie(choixJoueur: int, choixOrdi: int) -> int:
    r=int(choixJoueur)-int(choixOrdi)
    if r==0 :
        return None
    elif r==-1 or r==2:
        return 2
    elif r==-2 or r==1:
        return 1

def jouerJanken() -> int:
    joueur = choixOrdi()
    ordi = choixOrdi()
    return partie(joueur.value,ordi.value)

nbTests = int(input("Entrez le nombre de tests à réaliser (1 à 10000) : "))
while nbTests <1 or nbTests>10000:
    nbTests = int(input("Non ! Entrez le nombre de tests à réaliser (1 à 10000) : "))

resultats = []
for i in range(1,nbTests+1) :
    resultats.append(jouerJanken())

nbNull=0
nbOrdi1=0
nbOrdi2=0
for resultat in resultats :
    if(resultat==1) :
        nbOrdi1+=1
    elif(resultat==2):
        nbOrdi2+=1
    else:
        nbNull+=1

print("Matchs null : ",nbNull,"/",len(resultats)," => ",(nbNull/len(resultats))*100,"%")
print("Ordi 1 : ",nbOrdi1,"/",len(resultats)," => ",(nbOrdi1/len(resultats))*100,"%")
print("Ordi 2 : ",nbOrdi2,"/",len(resultats)," => ",(nbOrdi2/len(resultats))*100,"%")