
seq = ['T', 'T', 'C', 'C', 'P', 'S', 'I', 'V', 'A', 'R', 'S', 'N', 'F', 'N', 'V', 'C', 'R', 'L', 'P', 'G', 'T', 'P', 'E', 'A', 'I', 'C', 'A', 'T', 'Y', 'T', 'G', 'C', 'I', 'I', 'I', 'P', 'G', 'A', 'T', 'C', 'P', 'G', 'D', 'Y', 'A', 'N']*15

if len(seq) > 80:
    for i in range(1, (len(seq)//80)+1):
        seq.insert(80*i +i-1 ,"\n")

print(seq)

seq = "".join(seq)
print(seq)
