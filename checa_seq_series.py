seq1 = []
seq2 = []

import subprocess

def sendmessage(message):
    subprocess.Popen(['notify-send', message])
    return

with open('nNFE_atual.log', 'r') as f:
    #exemplo line serie1: SÉRIE 1: 3943, nfe original:35221146364058000115550010000017911035692790 []
    #exemplo line serie2: SÉRIE 2: 42601 nfe original:35221046364058000115550020000060871685858158 []


    for line in f.readlines():
        if line.startswith('SÉRIE 1: '):
            seq1.append(int(line.split()[2]))
        elif line.startswith('SÉRIE 2: '):
            seq2.append(int(line.split()[2]))


for i, n in enumerate(seq1):
    try:
        if n+1 != seq1[i+1]:
            print(n)
    except IndexError:
        if(seq1[-1]==n):
            print("OK")
            sendmessage("Sequencia 1 OK")
        else:
            print('falhou em: '+str(n))
            sendmessage("Sequencia falhou em "+str(n))

for i, n in enumerate(seq2):
    try:
        if n+1 != seq2[i+1]:
            print(n)
    except IndexError:
        if(seq2[-1]==n):
            print("OK")
            sendmessage("Sequencia 2 OK")
        else:
            print('falhou em: '+str(n))
            sendmessage("Sequencia falhou em "+str(n))
