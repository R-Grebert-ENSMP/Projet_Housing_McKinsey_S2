import sys
import numpy as np
import jellyfish
import nltk
from nltk.corpus import stopwords


#test1 = 'GEN LEMONNIER'
#test2= "du GÃ©nÃ©ral Lemonnier"


def compare(num1, type1, voie1, num2, type2, voie2):
    voie1 = normalisation_adresse(voie1) #normalise l'écriture, minuscule sans accent, sans apostrophe, sans stopwords
    voie2 = normalisation_adresse(voie2)
    distance = jellyfish.jaro_distance(normalisation_adresse(voie1), normalisation_adresse(voie2))
    if num1==num2 and type1==type2 and distance > 0.8 : #possibilité de rajouter une sélection sur la distance minimale
        return True
    else :
        return False

#print(compare(4, 'rue', test1 , 4, 'rue', test2))






