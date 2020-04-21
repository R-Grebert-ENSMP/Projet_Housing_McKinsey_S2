master1 = pd.DataFrame({'A': ['a' ,2,'d'], 'B': ['X', 'Y', '12'], 'C': ['a', 3, 11]})

master2 = pd.DataFrame({'A': ['a' ,4,'d'], 'B': ['X', 'F', 12], 'D': ['à', 'T', 3], 'E': ['y', 5, '&']})
##
def merger(df1, df2, c_merger, c_compare):
    res = df1.copy()
    long_c_merger = len(c_merger)
    for i in c_merger:
        res[i] = np.NaN
    indexem_c_df2 = [2, 3] # Indice des colonnes à merge DANS df2
    indexem_c_res = [3, 4] # Indice des colonnes à merge DANS res
    # Ces listes d'indice sont nécessaires afin d'accéder aux bonnes colonnes dans numpy
    indexec_c_df1 = [0, 1] #indice des colonnes à comparer DANS df1
    indexec_c_df2 = [0, 1] #indice des colonnes à comparer DANS df2
    (a, b) = df1.shape
    (c, d) = df2.shape
    M1 = np.array(df1)
    M2 = np.array(df2) #On passe en numpy
    R = np.array(res)
    for i in range (a):
        for j in range (c):
            if [M1[i, p] for p in indexec_c_df1] == [M2[j, l] for l in indexec_c_df2]:
                for k in range (long_c_merger):
                    R[i, indexem_c_res[k]] = M2[j, indexem_c_df2[k]]
    return pd.DataFrame(R)