# -*- coding: utf-8 -*-

import os

os.chdir("./")

import VarGlobale as vg
import IOinternet as ioi
import IOfichier as io
import Arborescence as arb
import Renommage as re
import CreationStatistiques as cs # utile pour générer des excels de résultats, mais j'ai préféré travailler avec SQL
import time
import BaseSQL as bs
## Etape 1 : Recupération des noms des comptes qu'on sauvegarde
#driver = ioi.ouverture_session_firefox()
#ioi.log_in_portail_ader(driver)
#T_sell = ioi.recuperation_compte_selles(driver)
#io.ecrire_csv("./", "Liste_comptes_selles", T_sell)
#driver.close()

# Etape 2 : Création d'un répertoire ou on sauvegarde les fichiers
#ioi.telechargement_multithreading(10)
   
## Etape 3 : Renommage à partir de la structure sauvegardée
#re.renommage(vg.adresseSauvegardeStruct, vg.adresseSauvegardeRep)    
#    
## Etape 4 : Création de statistique pour toutes les années
bs.base_fichier_SQL()  
bs.base_fichier_par_EPN_annee(2016)  

### A PASSER ABSOLUMENT POUR VERIFIER QU'ON A PAS OUBLIE DE FICHIER
def correction():
    ''' Indique les comptes non téléchargés'''
    chemin_parent = vg.adresseSauvegardeStruct
    (F, R) = arb.liste_sous_chemin(chemin_parent)
    T_sell = io.lire_csv("./", "Liste_comptes_selles")
    del(T_sell[-1])
    L = []
    for k in range(len(T_sell)):
        est_dedans = False
        for j in range(len(F)):
             (fname, ext) = os.path.splitext(F[j])
             if len(fname) >= 10 and T_sell[k][0] == fname[:10]:
                est_dedans = True
        if not est_dedans:
            L.append(T_sell[k][0])
    return L

def correction2():
    chemin_parent = vg.adresseSauvegardeStruct
    repFile = vg.adresseSauvegardeRep
    (F, R) = arb.liste_sous_chemin(chemin_parent)
    nb_fichier_attendu = 0
    D = []
    for f in F:
        (fname, ext) = os.path.splitext(f)
        [idEPN, annee] = fname.split("_")
        if ext == '.csv':
            T = io.lire_csv("./" + chemin_parent, fname)
            pdf = 0
            txt = 0
            for t in T:
                if len(t) > 3 :
                    if len(t[-1]) > 0:
                        [etat, code1, code2] = t[:3]
                        for j in range(len(vg.abreviation)):
                            if vg.nom_reel[j] == etat:
                                g = idEPN + '_' + vg.abreviation[j] + '_' + code1 + '_' + code2 + '_' + '0' + '_' + annee + '.pdf'
                                if not os.path.isfile(repFile + '/' + idEPN + '/' + g):
                                    print(g)
                                    D.append(g)
                                    break
                        pdf += 1
                    if len(t[-2]) > 0:
                        [etat, code1, code2] = t[:3]
                        for j in range(len(vg.abreviation)):
                            if vg.nom_reel[j] == etat:
                                g = idEPN + '_' + vg.abreviation[j] + '_' + code1 + '_' + code2 + '_' + '0' + '_' + annee + '.txt'
                                if not os.path.isfile(repFile + '/' + idEPN + '/' + g):
                                    print(g)
                                    D.append(g)
                                    break
                        txt += 1
            nb_fichier_attendu += pdf + txt
            if pdf + txt == 0:
                print("L'identifiant EPN " + fname + " semble anormal")
    return (nb_fichier_attendu, list(set(D)))
            
           

ioi.telechargement_basique(correction())
ioi.telechargement_basique(correction2()[1])