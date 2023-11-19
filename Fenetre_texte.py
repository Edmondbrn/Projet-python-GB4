import tkinter as tk
from tkinter import scrolledtext

import urllib.request
import ssl
import sys
import platform

# print(platform.system(), platform.release(), platform.version())
# print(sys.version)
def importation_online(code):
    print("Recuperation d'une fiche PDB ")
    liste_fich = []
    try:
        context = ssl._create_unverified_context()
        u=urllib.request.urlopen("https://files.rcsb.org/view/"+code.upper()+".pdb", context=context)
        pdblines=u.readlines()
        u.close()
    except:
        return("Problème lors de la lecture du fichier: \n" + "https://files.rcsb.org/view/"+code.upper()+".pdb")
    else:
        for ligne in pdblines:
            liste_fich.append(ligne.decode("utf8").strip() + "\n")
            fichier = "".join(liste_fich)
        return fichier



# Fonction pour créer la fenêtre
# def Affiche_PDB(texte):
#     Fenetre_PDB = tk.Tk()
#     Fenetre_PDB.title("Fenêtre avec Texte")
    
#     # Zone de texte avec défilement
#     fenetre_texte = scrolledtext.ScrolledText(Fenetre_PDB, width=40, height=10, wrap=tk.WORD)
#     fenetre_texte.insert(tk.END, texte)
#     fenetre_texte.pack(expand=True, fill='both')
#     Fenetre_PDB.mainloop()

