def partie(choixJoueur, choixOrdi):
    r=choixJoueur-choixOrdi
    if r==0 :
        return None
    elif r==-1 or r==2:
        return 2
    elif r==-2 or r==1:
        return 1

print("partie(1,1) = ", partie(1,1))
print("partie(1,2) = ", partie(1,2))
print("partie(1,3) = ", partie(1,3))
print("partie(2,1) = ", partie(2,1))
print("partie(2,2) = ", partie(2,2))
print("partie(2,3) = ", partie(2,3))
print("partie(3,1) = ", partie(3,1))
print("partie(3,2) = ", partie(3,2))
print("partie(3,3) = ", partie(3,3))