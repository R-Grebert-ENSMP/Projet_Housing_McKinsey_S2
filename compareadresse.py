import sys
import numpy as np
import jellyfish
#import nltk
#from nltk.corpus import stopwords


#test1 = 'GEN LEMONNIER'
#test2= "du GÃ©nÃ©ral Lemonnier"


def normalisation(string):
    #remplace les mauvais caractères de la table valeurfoncière
    oldaccent = ['Ã©','Ã¨','Ã´','Ã¢','Ã»',"Ãª"]
    newaccent = ['e','e','o','a','u','e']
    for i in range(len(oldaccent)):
        string = str.replace(string, oldaccent[i], newaccent[i])
    string = string.lower()
    oldabr = ["'"," de ", " du "," de la "," des ", " d'", " de l'"," les "," le "," la ", "general","place","impasse","docteur","saint","route","boulevard","avenue","allee","sentier","chemin","lotissement","passage","promenade"]
    newabr = [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','gen','pl',"imp","doc","st","ret","bd","av","all","sen","che","lot","pas","prom"]
    for i in range(len(oldabr)):
        string = str.replace(string, oldabr[i], newabr[i])
    return string

#def deletewords(string):
    #supprime les mots tels que "de" "la" "du"... pour comparer plus facilement
    sw = list(stopwords.words('french'))
    listwords = str.split(string)
    i = 0
    while i < len(listwords):
        if listwords[i] in sw :
            del listwords[i]
        else : 
            i += 1
    string = " ".join(listwords)
    return string

#def normalisation_adresse(voie) : 
    voie = accent(voie)
    voie = voie.lower()
    voie = deletewords(voie)
    return voie

def compare(num1, type1, voie1, num2, type2, voie2):
    voie1 = normalisation(" " + voie1) #normalise l'écriture, minuscule sans accent, sans apostrophe, sans stopwords
    voie2 = normalisation(" " + voie2)
    distance = jellyfish.jaro_distance(voie1, voie2)
    if num1==num2 and type1==type2 and distance > 0.9 : #possibilité de rajouter une sélection sur la distance minimale
        return True
    else :
        return False

#print(compare(4, 'rue', test1 , 4, 'rue', test2))

#distance = jellyfish.jaro_distance(normalisation(" " + test1), normalisation(" " + test2))
#print(normalisation(" " + test1),normalisation(" " + test2),distance)