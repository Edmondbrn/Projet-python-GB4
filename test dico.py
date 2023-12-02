from string import ascii_letters
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import Fonction as F


mat = F.matrice_contact(F.importation_online("1CRN"))
mat.columns = [x for x in range(1, mat.shape[1]+1)]
mat.index = [x for x in range(1, mat.shape[1]+1)]
mat = mat.astype(float)

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(10, 8))

# Generate a custom diverging colormap

cmap = sns.color_palette("rainbow", as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
contour = plt.contourf(mat, levels=8, cmap=cmap, alpha=1)
# Ajouter une nouvelle barre de couleur pour le tracé de contour
cbar_contour = plt.colorbar(contour, ax=ax, orientation="vertical", shrink=0.75)
plt.xlabel("Index des acides aminés")
plt.ylabel("Index des acides aminés")
plt.title("Heatmap de la distance des acides aminés dans l'espace")
plt.show()


import numpy as np
import matplotlib.pyplot as plt

# Créer des données de démonstration
data = np.random.random((10, 10))

# Créer une heatmap avec colorbar utilisant la colormap 'cividis'
heatmap = plt.imshow(data, cmap='rainbow')
colorbar = plt.colorbar(heatmap)

# Ajouter un titre à la colorbar
colorbar.set_label('Titre de la Colorbar', rotation=270, labelpad=15)

# Afficher la figure
plt.show()
