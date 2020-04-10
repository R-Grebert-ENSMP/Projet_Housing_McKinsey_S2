import sys
from ruler import Ruler
import numpy as np


#test1 = 'ARBRE'
#test2= "du GÃ©nÃ©ral Lemonnier"
#ruler=Ruler(test1.lower(),test2.lower())
#print(ruler.distance)

def accent(string):
    #remplace les mauvais caractère de la table valeurfoncière
    old = ['Ã©','Ã¨','Ã´','Ã¢','Ã»',"'"]
    new = ['e','e','o','a','u',' ']
    for i in range(len(old)):
        string = str.replace(string, old[i], new[i])
    return string

def compare(num1, type1, voie1, num2, type2, voie2):
    voie1 = accent(voie1).lower() #normalise l'écriture, minuscule sans accent, sans apostrophe
    voie2 = accent(voie2).lower()
    l1, l2 = len(voie1), len(voie2)
    marge= 1
    ruler = Ruler(voie1.lower(), voie2.lower())
    if num1==num2 and type1==type2 and ruler.distance <= abs(l1-l2) + marge : #possibilité de rajouter une sélection sur la distance minimale
        return True
    else : 
        return False

#print(compare(4, 'rue', test1, 4, 'rue', test2))
