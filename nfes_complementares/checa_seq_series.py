seq =()
for i, n in enumerate(seq):
    try:
        if n+1 != seq[i+1]:
            print(n)
    except IndexError:
        if(seq[-1]==n):
            print("OK")
        else:
            print('falhou em: '+str(n))
