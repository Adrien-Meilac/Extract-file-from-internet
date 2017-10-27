# -*- coding: utf-8 -*-


import sqlite3
import VarGlobale as vg
import IOfichier as io
import os 
import Arborescence as arb

def base_fichier_SQL():
    '''Créer un inventaire des fichiers de l'arborescence des comptes sellés en SQL
    '''
    conn = sqlite3.connect('sellements.db')
    cursor = conn.cursor()
    Lcol = ["lien", "repertoire", "nom_fichier", "idEPN", "abreviation", "type_doc", "code_budgetaire", "compteur_unique", "annee", "extension", "etat"]
    cursor.execute("""DROP TABLE IF EXISTS sellements_comptes;""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sellements_comptes_par_fichier(
    lien TEXT PRIMARY KEY, {});""".format(" TEXT,".join(Lcol[1:])))
    conn.commit()
    (_, R) = arb.liste_sous_chemin(vg.adresseSauvegardeRep)
    for r in R:
        (F, _) = arb.liste_sous_chemin(vg.adresseSauvegardeRep + '/' + r)
        for f in F:
            print(vg.adresseSauvegardeRep + '/' + r + '/' + f)
            (fname, ext) = os.path.splitext(f)
            L = fname.split("_")
            ext = ext[1:]
            if ext == "pdf":
                (Bouverture, Btexte) = io.pdf_non_vide(vg.adresseSauvegardeRep + '/' + r + '/' + f)
                if Bouverture == False:
                    etat = "Corrompu"
                elif Bouverture == True and Btexte == True:
                    etat = "Lisible"
                elif Bouverture == "Problème intrinsèque":
                    etat = "Problème intrinsèque"
                else: 
                    etat = "Image"
            elif ext == "txt":
                etat = "Existant"
            if len(L) == 6:
                data = {"extension" : ext, "lien" : vg.adresseSauvegardeRep + '/' + r + '/' + f, "nom_fichier" : f, "repertoire": vg.adresseSauvegardeRep + '/' + r , "etat" : etat}
                for j in range(3, 9):
                    data[Lcol[j]] = L[j - 3]
                cursor.execute("""INSERT INTO sellements_comptes_par_fichier({0}) VALUES({1});""".format(", ".join(Lcol), ":" + ", :".join(Lcol)), data)
                conn.commit()
    conn.close()
    return 

def base_fichier_par_EPN_annee(annee):
    '''Crée une base SQL qui regarde ce que contient chaquez EPN d'une année donnée'''
    n = len(vg.abreviation)
    T_sell = io.lire_csv("./", "Liste_comptes_selles")
    del(T_sell[-1])
    conn = sqlite3.connect('sellements.db')
    cursor = conn.cursor()
    Lcol = ["idEPN", "nomEPN"]
    for i in range(n):
        for ext in ["txt","pdf"]:
            Lcol.append(ext + "_" + vg.abreviation[i])
    cursor.execute("""DROP TABLE IF EXISTS sellements_comptes_par_EPN_{};""".format(str(annee)))
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sellements_comptes_par_EPN_{}(
    idEPN TEXT PRIMARY KEY, {});""".format(str(annee), " TEXT,".join(Lcol[1:])))
    conn.commit()
    for j in range(len(T_sell)):
        print(T_sell[j][0])
        data = {"idEPN": T_sell[j][0], "nomEPN" : T_sell[j][1], "annee": str(annee)}
        for i in range(n):
            for ext in ["txt","pdf"]:
                data[ ext + "_" + vg.abreviation[i]] = "Non existant"
        L = cursor.execute("""SELECT abreviation, extension, etat FROM sellements_comptes_par_fichier WHERE idEPN = :idEPN AND annee = :annee""", data).fetchall()
        for (abrev, ext, etat) in L:
            data[ext + "_" + abrev] = etat
        cursor.execute("""INSERT INTO sellements_comptes_par_EPN_{2}({0}) VALUES({1});""".format(", ".join(Lcol), ":" + ", :".join(Lcol), str(annee)), data)
        conn.commit()
    conn.close()
    return 
 
base_fichier_SQL()
base_fichier_par_EPN_annee(2016)