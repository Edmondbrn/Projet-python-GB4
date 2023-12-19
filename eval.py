def count_aa(Seq):
    dico = {}
    for aa in Seq:
        if aa not in dico.keys():
            dico[aa] = 1
        else:
            dico[aa] += 1
    return dico

stri = "Bonjour je m'appelle Gabite"
print(stri.split())
def ouverture():
    try:
        fh = open(skjeugfczieugfh, "r")
    except: 
        return None, "tege", "égd"
    else:
        return 'Bien ouej'

def verif(seq):
    a = True
    for i in range(len(seq)):
        if seq[i] == "X" or seq[i] == "-":
            a = False
            print(i)
    if a:
        print("Motif ok")
        


print(ouverture())



prot = "MKLPY        KAK    YY"
prot = prot.replace(" ","")
print(prot)
seq = prot[-6:]
print(seq)
occurence = count_aa(prot)
print(occurence)