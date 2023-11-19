import pandas as pd
import matplotlib.pyplot as plt

# Exemple de données
data = {'AA': ['A', 'C', 'D', 'E', 'F'],
        'Frequency': [10, 15, 5, 20, 12]}

df = pd.DataFrame(data)

# Définir les couleurs
couleur = ['blue', 'green', 'red', 'cyan', 'magenta']

# Créer le graphique
ax = df.plot(x='AA', kind='bar', figsize=(20, 6), color=couleur, edgecolor='black')

# Ajouter des annotations avec les coordonnées
for i, bar in enumerate(ax.patches):
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f'{height}',
        ha='center',
        va='bottom' if height >= 0 else 'top',  # ajuster la position du texte en fonction de la hauteur de la barre
        color='black',  # couleur du texte
        fontsize=10,  # taille de la police
        fontweight='bold'  # poids de la police
    )

# Étiqueter les axes et le titre
plt.xlabel('Acides Aminés')
plt.ylabel('Fréquence')
plt.title('Fréquences des Acides Aminés dans la Séquence Protéique')
plt.legend()
plt.show()
