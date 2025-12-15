from random import randint
from enum import Enum

class choix(Enum):
    Pierre  =1
    Feuille =2
    Ciseaux =3

def choixOrdi():
    a=randint(1,3)
    return choix(a)

leChoixOrdi = choixOrdi()
print("L'ordi a choisis : ",leChoixOrdi.name)