#prend une voie en e
import sys
import numpy as np
import jellyfish
import nltk
from nltk.corpus import stopwords

def accent(string):
    #remplace les mauvais caractère de la table valeurfoncière
    old = ['Ã©','Ã¨','Ã´','Ã¢','Ã»',"Ãª","'"]
    new = ['e','e','o','a','u','e',' ']
    for i in range(len(old)):
        string = str.replace(string, old[i], new[i])
    return string

def deletewords(string):
    #supprime les mots tels que "de" "la" "du"... pour conparer plus facilement
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

def normalisation_adresse(voie) :
    voie = accent(voie)
    voie = voie.lower()
    voie = deletewords(voie)
    return voie
