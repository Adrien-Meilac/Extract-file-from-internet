# -*- coding: utf-8 -*-
# Fichiedr renommage.py
# Contient les fonctions qui renomment les fichiers une fois qu'ils sont dans les répertoires


import Arborescence as arb
import IOfichier as io
import VarGlobale as vg
import os
import shutil

def liste_nomenclature(rep):
    '''Permet d'afficher les différentes catégories disponibles dans tous les CSV qui contiennent l'architecture des pages web'''
    (F, R) = arb.liste_sous_chemin(rep)
    L = []
    for f in F:
        print(f)
        (fname, ext) = os.path.splitext(f)
        T = io.lire_csv(rep, fname)
        for t in T:
            if t[0] != '' and not( t[0] in L):
                L.append(t[0])
    return L
               

def indice_sup_mot(phrase, mot):
    '''Permet de trouver la premiere occurence d'une phrase dans un mot et renvoit le nombre correspondant à l'indice du caractère après le mot
        * args : phrase, mot : deux string
        * out : un entier
    '''
    for k in range(len(phrase)- len(mot) + 1):
       if mot == phrase[k:k + len(mot)]:
           return k + len(mot)
          

def renommage(repStruct, repFile, lien = "C:/Users/ameilac/Downloads", noprint = False):
    '''Renomme les fichiers en lisant le csv associé
        *args : repertoire contenant les csv, repertoire contenant les repertoires des idEPN
        *out : None
    '''
    All_struct = []
    (F, R) = arb.liste_sous_chemin(repStruct)
    for f in F:
        (fname, ext) = os.path.splitext(f)
        [idEPN, annee] = fname.split("_")
        print(idEPN)
        if not os.path.exists(repFile + '/' + idEPN): # Création du dossier pour le compte d'identifiant id_EPN
                os.mkdir(repFile + '/' + idEPN)
        T = io.lire_csv(repStruct, fname)
        for t in T:
            if len(t) >= 4:
                contient_un_fichier = False
                if len(t[-2]) > 0:
                    a = indice_sup_mot(t[-2], "fic=")
                    t[-2] = t[-2][a:]
                    contient_un_fichier = True
                if len(t[-1]) > 0:
                    b = indice_sup_mot(t[-1], "https://pass.cp.finances.ader.gouv.fr/epn_gip/demat/fichier-pdf-scelle-")
                    t[-1] = t[-1][b:]
                    contient_un_fichier = True
                if contient_un_fichier:
                    All_struct.append([idEPN, annee] + t)
    n = len(All_struct)
    print("Toute la structure est lue, elle contient "+ str(n) + " lignes")
    (F, R) = arb.liste_sous_chemin(lien)
    for f in F:
        k = 0
        (fname, ext) = os.path.splitext(f)
        ext = ext.lower()
        if ext == '.pdf' :
            k = -1
        elif ext == '.txt':
            k = -2
        if k < 0 :
            est_renomme = False
            for i in range(n):
                ligne = All_struct[i]
                if ligne[k] == fname:
                    [idEPN, annee, categorie, code1, code2] = ligne[:5]
                    for j in range(len(vg.nom_reel)):
                        if vg.nom_reel[j] == categorie:
                            compteur = 0
                            while not est_renomme:
                                g = idEPN + '_' + vg.abreviation[j] + '_' + code1 + '_' + code2 + '_' + str(compteur) + '_' + annee + ext
                                if not os.path.isfile(repFile + '/' + idEPN + '/' + g):
                                    shutil.move(lien + '/' + f, repFile + '/' + idEPN + '/' + g)
                                    print(repFile + '/' + idEPN + '/' + g)
                                    est_renomme = True
                                else:
                                         compteur += 1 
                            break
                    break
    return