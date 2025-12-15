def vers_decimal(nb: str, base: int) -> int:
    
    if(base>9):
        raise Exception(f"Base {base} invalide")
    
    #prend en argument un chaine de caractère, nombre, et sa base (binaire, octale, décimale, etc...), et retourne un entier convertie en decimal
    nb_decimal =  0     #le nombre décimal final
    rang = len(nb)-1    #le rang du chiffre le + à gauche
                        #c'est le nb de caracteres de la chaine - 1, et le plus a droite c'est 0
    for n in nb:        #pour chaque caractere du nombre en partant du rang le plus élevé, le plus a gauche
        nombre = n
        if(int(n)>=base): #valide la cohérence du nombre saisi en fonction de sa base, en base n on a le droit a tous les chifres de 0 a n-1
            raise Exception(f"Caractere {n} impossible pour la base {base}")

        valeur_rang = int(nombre)*(base**rang)  #c'est le nombre * (base puissance le rang)
        nb_decimal += valeur_rang               #on additionne la valeur de chaque rang
        rang = rang - 1                         #faut penser à changer de rang a chaque tour
        
    return nb_decimal

if __name__ == "__main__":
    print(vers_decimal("17",8)) # 17 en octal
    print(vers_decimal("10101",2)) # 10101 en binaire
    print(vers_decimal("1021",2)) # 2 pas valide en binaire
