import pandas as pd
import numpy as np

# Créer un DataFrame avec des zéros sur la diagonale et des valeurs au-dessus
donnees = {'A': [0, 1, 2, 3],
           'B': [0, 0, 4, 5],
           'C': [0, 0, 0, 6],
           'D': [0, 0, 0, 0]}

df = pd.DataFrame(donnees)

print("DataFrame d'origine :")
print(df)

# Extraire la partie triangulaire supérieure de la matrice
tri_sup = np.triu(df.values, k=1)

# Ajouter la partie triangulaire supérieure à sa transposée
df_symetrique = pd.DataFrame(tri_sup + tri_sup.T, columns=df.columns, index=df.index)

print("\nDataFrame symétrique :")
print(df_symetrique)
