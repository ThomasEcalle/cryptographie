# codex(B)=1
# Code erreur : -1
def codex(c):
    try:
        c = str(c)
        c = c[0].upper()
    except:
        return -1
    n = ord(c) - ord('A')
    if (n > 25 or n < 0): return -1
    return n


# xedoc(1)=B
# Code erreur : '?'
def xedoc(n):
    try:
        n = int(n)
    except:
        return '?'
    if (n > 25 or n < 0): return '?'
    return chr(n + ord('A'))


# paquet("ABCD", 2)={0:1, 1:203}
# Code erreur : dico vide
def paquet(txt, paq=1):
    try:
        txt = str(txt)
        paq = int(paq)
    except:
        return dict()
    if (paq < 0): return dict()

    res = dict()
    n = len(txt)
    i = 0
    nb_paq = -1
    while (i < n):
        if (i % paq == 0):
            nb_paq += 1
            res[nb_paq] = 0
        res[nb_paq] = res[nb_paq] * 100 + codex(txt[i])
        i += 1

    while (i % paq != 0):
        res[nb_paq] *= 100
        i += 1
    return res


# mod2base(2)=2526
# Code erreur : 26
def mod2base(paq=1):
    try:
        paq = int(paq)
    except:
        return mod2base()
    res = 0
    i = 0
    while (i < paq):
        res = 100 * res + 25
        i += 1
    return res + 1


# renvoie une chaine de caractère du chiffrement de cesar
# Code erreur : chaine vide
def Ecesar(txt, clef, paq=1):
    try:
        txt = str(txt)
        clef = int(clef)
        paq = int(paq)
    except:
        return ""
    X = paquet(txt, paq)
    x = len(X)
    mod = mod2base(paq)
    clef = clef % mod

    res = ""
    i = 0
    while (i < x):
        X[i] = (X[i] + clef) % mod
        if (paq == 1):
            res += xedoc(X[i])
        else:
            res += str(X[i])
            if (i < x - 1): res += '-'
        i += 1
    return res


# renvoie la chaine déchiffrée de cesar
# Code erreur : chaine vide
def Dcesar(txt, clef, paq=1):
    try:
        txt = str(txt)
        clef = int(clef)
        paq = int(paq)
    except:
        return ""

    if (paq == 1):
        X = paquet(txt)
    else:
        X0 = txt.split('-')
        n0 = len(X0)
        X = dict()
        i = 0
        while (i < n0):
            try:
                X[i] = int(X0[i])
            except:
                return ""
            i += 1

    x = len(X)
    mod = mod2base(paq)
    clef = clef % mod
    res = ""
    i = 0
    while (i < x):
        X[i] = (X[i] - clef) % mod
        if (paq == 1):
            tmp = xedoc(X[i])
            if (tmp == '?'): return ""
        else:
            tmp = ""
            j = 0
            while (j < paq):
                tmp2 = xedoc(X[i] % 100)
                if (tmp2 == '?'): return ""
                tmp = tmp2 + tmp
                X[i] = X[i] // 100
                j += 1
        res += tmp
        i += 1
    return res


# Attaque en brute force
def bruteforcecesar(txt, paq=1):
    try:
        txt = str(txt)
        paq = int(paq)
    except:
        print("L'attaque ne fonctionne pas")
        return

    mod = mod2base(paq)
    clef = 0
    clef_valide = 1
    while (clef < mod):
        att_txt = Dcesar(txt, clef, paq)
        if (att_txt != ""):
            print("#" + str(clef_valide) + " (" + str(clef) + ") :" + att_txt)
            clef_valide += 1
        clef += 1
    print(str(clef_valide) + " clefs valides testées")


# Gestion des caractère accentué
def Filtre1(txt):
    res = ""
    for c in txt:
        if c == 'à' or c == 'â' or c == 'ä':
            res = res + 'A'
        elif c == 'ç':
            res = res + 'C'
        elif c == 'é' or c == 'è' or c == 'ê' or c == 'ë':
            res = res + 'E'
        elif c == 'ï' or c == 'î' or c == 'ì':
            res = res + 'I'
        elif c == 'ö' or c == 'ò' or c == 'ô':
            res = res + 'O'
        elif c == 'û' or c == 'ü' or c == 'ù':
            res = res + 'U'
        elif c == '-' or c == ' ':
            res = res + ''
        else:
            res = res + c.upper()
    return res


# renvoie le tableau des mots (séparés par un \n) avec plus de 'sensibilité' caractères
def Filtre2(txt, sensibilite=3):
    txt2 = txt.split('\n')
    n = len(txt2)
    res = dict()
    i = 0
    cmpt = 0
    while i < n:
        if len(txt2[i]) >= sensibilite:
            res[cmpt] = txt2[i]
            cmpt += 1
        i += 1
    return res


# Renvoie la liste de tous les mots de la langue française de plus de 'sensibilité' caractere
def MonDico(sensibilite=3):
    fichier = open("dico.txt", "r")
    dictionnaire = fichier.read()
    fichier.close()
    return Filtre2(Filtre1(dictionnaire), sensibilite)


# Renvoie true si mot est dans phrase (A FAIRE)
def is_present(mot, phrase):
    return phrase.find(mot) != -1


# Renvoie le nombre de mot du dico présent dans la phrase (A FAIRE)
def pertinance(phrase, dico):
    res = 0
    for index in dico:
        if is_present(dico[index], phrase):
            res += 1
    return res


# Comme brute force mais en présentant les plus pertinants (A FAIRE)
def bruteforcecesar_dico(txt, paq=1, sensibilite=3):
    try:
        txt = str(txt)
        paq = int(paq)
        sensibilite = int(sensibilite)
    except:
        print("L'attaque ne fonctionne pas")
        return

    mod = mod2base(paq)
    clef = 0
    clef_valide = 1
    mostpertinentString = ""
    pertinenceMax = -1
    dico = MonDico(sensibilite)
    while clef < mod:
        att_txt = Dcesar(txt, clef, paq)
        if att_txt != "":
            p = pertinance(att_txt, dico)
            if p >= pertinenceMax:
                mostpertinentString = att_txt
                pertinenceMax = p
            clef_valide += 1
        clef += 1
        print("most pertinent sentence for the moment = " + mostpertinentString)

    print(str(clef_valide) + " clefs valides testées")
    print("\nmost pertinent solution = " + mostpertinentString + "\n")
    return


txt = "2138-523-1651-1650-712-1434-1834-2338-412-721-212-708"
bruteforcecesar_dico(txt, 2, 3)
