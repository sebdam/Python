from enums import NumberFormat

import re

def translate(nb: str, to: str) -> str :
    format = read_number_format(nb)
    destination = read_number_format(to)
    number = read_number(nb)
    if(number == ''):
        raise Exception(f"Invalid number '{nb}' for format '{format.name}'")
    
    #print(number, format, destination)

    ret = number_vers(number,format,destination)
    return ret if ret != None else "Error during translation"

def number_vers(nb: str, origine: NumberFormat, destination: NumberFormat) -> str | None :
    if destination == NumberFormat.binaire :
        return bin(vers_decimal(nb, origine.value))
    elif destination == NumberFormat.octal :
        return oct(vers_decimal(nb, origine.value))
    elif destination == NumberFormat.decimal :
        return str(vers_decimal(nb, origine.value))
    elif destination == NumberFormat.hexadecimal :
        return hex(vers_decimal(nb, origine.value))
    else:
        print('Unsuported destination format', destination)

def vers_decimal(nb: str, base: int) -> int:
    
    if(base>36 or base<2): #bases entre 2 et 36 (10+26 lettres de l'alphabet)
        raise Exception(f"Base {base} invalide")
    
    #prend en argument un chaine de caractère, nombre, et sa base (binaire, octale, décimale, etc...), et retourne un entier convertie en decimal
    nb_decimal =  0     #le nombre décimal final
    rang = len(nb)-1    #le rang du chiffre le + à gauche
                        #c'est le nb de caracteres de la chaine - 1, et le plus a droite c'est 0
    for n in nb:        #pour chaque caractere du nombre en partant du rang le plus élevé, le plus a gauche
        nombre = n
        valide_nombre(n,base) #valide la cohérence du nombre saisi en fonction de son format
        if(base > 10):
            nombre = convert_over_than_base10_to_dec(n) #au dessus de base 10 il y a des lettres
        valeur_rang = int(nombre)*(base**rang)  #c'est le nombre * (base puissance le rang)
        nb_decimal += valeur_rang               #on additionne la valeur de chaque rang
        rang = rang - 1                         #faut penser à changer de rang a chaque tour
        
    return nb_decimal

def valide_nombre(nombre: str, base: int):

    if(base <= 10 and (int(nombre) >= base or int(nombre)<0)) :
        raise Exception(f"Invalid caracter '{nombre}' for base '{base}'")
    if(base > 10 and not(nombre >= '0' and nombre <= '9') and not(nombre >= 'a' and nombre <= chr(ord('a') + base-11)) and not(nombre >= 'A' and nombre <= chr(ord('A') + base-11)) ) :
        raise Exception(f"Invalid caracter '{nombre}' for base '{base}'")
    

def convert_over_than_base10_to_dec(n: str) -> str:
    if n >= '0' and n <= '9' :
        return n
    return str(ord(n.capitalize()[0]) - ord('A') + 10) #A=10, B=11, etc..

def read_number_format(number : str) -> NumberFormat:
    if number.startswith('b') or number.startswith('B') or number.startswith('0b') :
        return NumberFormat.binaire
    
    if number.startswith('t') or number.startswith('T') or number.startswith('0t') :
        return NumberFormat.ternaire
    
    if number.startswith('q') or number.startswith('Q') or number.startswith('0q') :
        return NumberFormat.base4
    if number.startswith('c') or number.startswith('C') or number.startswith('0c') :
        return NumberFormat.base5
    if number.startswith('s') or number.startswith('S') or number.startswith('0s') :
        return NumberFormat.base6
    if number.startswith('e') or number.startswith('E') or number.startswith('0e') :
        return NumberFormat.base7
    if number.startswith('o') or number.startswith('O') or number.startswith('0o')  :
        return NumberFormat.octal
    if number.startswith('n') or number.startswith('N') or number.startswith('0n') :
        return NumberFormat.base9
    

    if number.startswith('o') or number.startswith('O') or number.startswith('0o') :
        return NumberFormat.base11
    if number.startswith('z') or number.startswith('Z') or number.startswith('0z') :
        return NumberFormat.duodecimal
    if number.startswith('r') or number.startswith('R') or number.startswith('0r') :
        return NumberFormat.base13
    if number.startswith('u') or number.startswith('U') or number.startswith('0u') :
        return NumberFormat.base14
    if number.startswith('a') or number.startswith('A') or number.startswith('0a') :
        return NumberFormat.base15
    
    if number.startswith('x') or number.startswith('X') or number.startswith('0x')  :
        return NumberFormat.hexadecimal
    
    return NumberFormat.decimal

def read_number(number : str) -> str:
    if(re.search("[a-zA-Z]+",number) == None):
        #si pas de présence de lettre on part sur du décimal sans avoir a retirer le prefix (il n'y en a pas)
        return number
    elif number.startswith('0'):
        #on garde tous les caracters sauf les deux premiers (de 2 à la fin car les deux premiers sont 0 et 1)
        return number[2:]
    else:
        #on garde tous les caracters sauf le premier (de 1 à la fin car le premier est 0)
        return number[1:]