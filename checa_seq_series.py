
for i,n in enumerate(seq):
    try:
        if n+1!=seq[i+1]:
            print(n)
    except IndexError:
        print(n)