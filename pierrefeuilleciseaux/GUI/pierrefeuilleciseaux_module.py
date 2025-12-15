from enum import Enum
import numpy as np

rng = np.random.default_rng(12345)

#########################################################################################
#       Parametres globaux                                                              #
#########################################################################################
nbTestsMin = 1
nbTestsMax = 10000
silent = True

#########################################################################################
#       Entités : objet qui représente la pierre, la feuille ou le ciseau               #
#       Ca permet de créer son propre type représentant la pierre, feuille ou le ciseau #
#########################################################################################

class choix(Enum):
    Pierre  =1 # la pierre vaudra 1 (int) partout
    Feuille =2 # la feuille vaudra 2 partout
    Ciseaux =3 # le ciseau vaudra 3 partout

#########################################################################################
#       Méthode de choix pour l'ordi                                                    #
#       - si pourOrdi == true, le choix est fait au hasard                              #
#########################################################################################

def choixOrdi() -> choix :
    return choix(rng.integers(1,4))

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