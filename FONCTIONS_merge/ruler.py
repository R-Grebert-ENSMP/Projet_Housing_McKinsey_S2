import numpy as np
from colorama import Fore, Style

class Ruler():




    def __init__(self, seq1, seq2):
        self.seq1 = seq1
        self.seq2 = seq2
        self.distance = Ruler.compute(self)[4]



    def compute(self):

        '''
        On va d'abord créer une matrice des scores de différents chemins correspondant aux différentes possibilités et une matrice correspondant aux chemins, selon l'algorithme de Needleman.
        Ensuite on procèdera au traceback en partant  du coin inférieur gauche pour remonter et on obtiendra ainsi le meilleur chemin.

        '''

        CoutD = 1 #Cout de déplacement
        CoutR = 1 #Cout de remplacement
        seq1 = self.seq1
        seq2 = self.seq2
        l1, l2 = len( seq1 ), len( seq2 )
        ScoreM = np.zeros((l1+1 ,l2+1))
        PathM = np.zeros((l1+1 ,l2+1), object)

        for i in range( 1 , l1 + 1 ):
            ScoreM[i][0] = i*CoutD
            PathM[i][0] =  'up'
        for i in range( 1 , l2 + 1):
            ScoreM[0][i] = i*CoutD
            PathM[0][i] = 'left'


        for i in range(1, l1 + 1 ):

            for j in range(1, l2 + 1 ):

                if seq1[i-1]  == seq2[j-1]:
                    new = 0

                elif seq1[i-1]  != seq2[j-1]:
                    new = CoutR

                d, u, l = ScoreM[i-1][j-1] + new,  CoutD + ScoreM[i-1][j], CoutD + ScoreM[i][j-1]
                ScoreM[i,j] = min(d,u,l)

                if min(d,u,l) == u :
                    PathM[i][j] = 'up'

                if min(d,u,l) ==  d:
                    PathM[i][j] = 'diag'

                if min(d,u,l) == l :
                    PathM[i][j] = 'left'

        distance = ScoreM[l1][l2]

        Best =[PathM[l1][l2]]
        x,y = l1,l2
        CoordBest =[[x,y]]
        a = PathM[x][y]

        while a!= PathM[0][0]:
            if a == 'diag':
                x,y = x-1, y-1
            if a == 'left':
                x,y = x,y-1
            if a == 'up' :
                x,y = x-1,y
            a = PathM[x][y]
            CoordBest.insert(0,[x,y])
            Best.insert(0,a)




        return PathM, ScoreM, Best, CoordBest, ScoreM[l1][l2]




    def red_text(text):
        return f"{Fore.RED}{text}{Style.RESET_ALL}"





    def report(self):

        def red_text(text):
            return f"{Fore.RED}{text}{Style.RESET_ALL}"

        seq1 = self.seq1
        seq2 = self.seq2

        A = Ruler.compute(self)[2]  #on reprend le chemin issu du traceback
        l = len(A)
        R1 = []
        R2 = []
        c1,c2=0,0

        for i in range(1, l):

            if A[i] == 'diag':
                if seq1[i-1-c1] == seq2[i-1-c2]:
                    R1.append(seq1[i-1-c1])
                    R2.append(seq2[i-1-c2])
                if seq1[i-1-c1]!= seq2[i-1-c2]:
                    R1.append(red_text(seq1[i-1-c1]))
                    R2.append(red_text(seq2[i-1-c2]))

            if A[i] == 'up':
                R1.append(seq1[i-1-c1])
                R2.append(red_text("-"))
                c2+=1

            if A[i] == 'left':
                R1.append(red_text("-"))
                R2.append(seq2[i-1-c2])
                c1+=1

        #print(''.join(R1), '\n',''.join(R2))
        return (''.join(R1),''.join(R2))
        #return()



test1 = 'abcdef'
test2 = 'abfkf'
#
# ruler= Ruler(test1, test2)
# len(ruler.seq1)
# Ruler.compute(ruler)
#print(ruler.distance)

#Ruler.report(ruler)
#print(Ruler.compute(ruler)[0], Ruler.compute(ruler)[1], Ruler.compute(ruler)[2])
#print(''.join(Ruler.report(ruler)[0]), '\n', ''.join(Ruler.report(ruler)[1]))