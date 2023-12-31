#!python3
import urllib.request
import ssl
import sys
import platform

print(platform.system(), platform.release(), platform.version())
print(sys.version)

url = "http://files.rcsb.org/view/1CRN.pdb"
try:
    context = ssl._create_unverified_context()
    u=urllib.request.urlopen(url, context=context)
    pdblines=u.readlines()
    u.close()
except:
    print("Problem lors de la lecture du fichier")
else:
    for ligne in pdblines:
        #print(ligne)
        print(ligne.decode("utf8").strip())

    
