from collections import deque
'''INPUTUL SE REALIZEAZA IN URMATORUL FEL:
0           - STARE INITIALA
2           - NUMAR STARI FINALE
0           - STARE FINALA 1
5           - STARE FINALA 2
ab          - ALFABET
7           - NUMAR STARI
0 1 a
0 3 b
1 2 a
1 6 b
3 3 b
3 4 b
4 4 a
4 5 a
5 5 a
5 2 a
6 0 b
6 5 b
ULTIMA LINIE A FISIERULUI TXT VA FI ULTIMA TRANZITIE
'''
def citire_afn():
    f = open("AFN.txt","r")

    #stare initiala
    ns = f.readline().strip()

    #nr. stari finale si lista de stari finale
    nr_f = int(f.readline())
    fin = []
    for i in range(nr_f):
        fin.append(f.readline().strip())

    #alfabetul automatului
    alfabet = f.readline().strip()
    #numarul de caractere al alfabetului
    nr_c = len(alfabet)

    nr_stari = int(f.readline())

    tabel_afn = [["-" for i in range(nr_c)]for i in range(nr_stari)]

    #constructia tabelului functiei de tranzitie
    for line in f:
        line = line.strip()
        stare_s = int(line[0])
        stare_d = line[2]
        caracter = line[4]
        index_c = index_simbol(alfabet, caracter)
        if tabel_afn[stare_s][index_c] == "-":
            tabel_afn[stare_s][index_c] = stare_d
        else:
            tabel_afn[stare_s][index_c]+=stare_d

    f.close()

    #sortare
    for linie in tabel_afn:
        for i in range(len(linie)):
            linie[i] = "".join(sorted(linie[i]))


    return ns, nr_f, fin, alfabet, nr_stari, tabel_afn

def este_final(fin, stare):
    for c in stare:
        if c in fin:
            return 1
    return 0

def afn_in_afd(ns, nr_f, fin, alfabet, nr_stari, tabel_afn):
    coada = deque([ns])
    adaugat = [ns]

    #print(tabel_afn)

    #stari finale din afd
    fin_afd = []
    if ns in fin:
        fin_afd.append(ns)

    tabel_afd = []

    while len(coada) != 0:
        stare = coada.popleft()
        tabel_afd.append(["-" for x in range(len(alfabet)+1)])
        tabel_afd[-1][0] = stare
        if len(stare) == 1:
            for i in range(len(alfabet)):
                tabel_afd[-1][i+1] = tabel_afn[int(stare)][i]
                if tabel_afn[int(stare)][i] != "-" and tabel_afn[int(stare)][i] not in adaugat:
                    coada.append(tabel_afn[int(stare)][i])
                    adaugat.append(tabel_afn[int(stare)][i])
                    if este_final(fin, tabel_afn[int(stare)][i]):
                        fin_afd.append(tabel_afn[int(stare)][i])

        else:
            for i in range(len(alfabet)):
                noua_stare=""
                for c in stare:
                    if tabel_afn[int(c)][i] not in noua_stare and tabel_afn[int(c)][i] != "-":
                        noua_stare+=tabel_afn[int(c)][i]
                noua_stare = "".join(sorted(set(noua_stare)))
                if noua_stare != "":
                    tabel_afd[-1][i+1] = noua_stare
                    if noua_stare not in adaugat:
                        coada.append(noua_stare)
                        adaugat.append(noua_stare)
                        if este_final(fin, noua_stare):
                            fin_afd.append(noua_stare)
                else:
                    tabel_afd[-1][i+1] = "-"

    print("--------------------------------")
    for linie in tabel_afd:
        print("Q(" + linie[0] +")",end="")
        if linie[0] in fin_afd:
            print(" STARE FINALA")
        else:
            print()
        for i in range(len(alfabet)):
            print(alfabet[i],":",end="")
            if(linie[i+1] != "-"):
                print("Q("+linie[i+1]+")")
            else:
                print("---")


#obtinere index caracter din alfabet
def index_simbol(alfabet, caracter):
    return alfabet.index(caracter)

ns, nr_f, fin, alfabet, nr_stari, tabel_afn = citire_afn()
afn_in_afd(ns, nr_f, fin, alfabet, nr_stari, tabel_afn)

#stare initiala
#nr stari finale
#stare finala 1
#stare finala 2 etc
#alfabet
#numar stari
#tranzitie 1
#tranzitie 2 etc