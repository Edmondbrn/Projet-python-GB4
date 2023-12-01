from string import ascii_letters
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import Fonction as F

sns.set_theme(style="white")

mat = F.matrice_contact(F.importation_online("1CRN"))
mat.columns = [x for x in range(1, mat.shape[1]+1)]
mat.index = [x for x in range(1, mat.shape[1]+1)]
mat = mat.astype(float)



# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(10, 8))

# Generate a custom diverging colormap

cmap = sns.color_palette("rainbow", as_cmap=True)


# Draw the heatmap with the mask and correct aspect ratio
max = np.max(np.max(mat))

sns.heatmap(mat , cmap=cmap, fmt=".2f", linewidths=.5, cbar_kws={"shrink": .75})

plt.show()




