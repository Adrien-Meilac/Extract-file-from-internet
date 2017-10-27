# -*- coding: utf-8 -*-
# Fichier CreationStatistiques.py (fichier supplémentaire, non utilisé dans le main)
# contient les fonctions qui retraitent les documents et fournissent des statistiques dans des fichiers

import VarGlobale as vg
import Arborescence as arb
import IOfichier as io
import os
import xlsxwriter 

def types_sont_dedans(id_EPN, anneeRef):
    '''Cherche à savoir si dans un répertoire, les types recherchés sont bien dedans (version 1 uniquement)
        *args : id_EPN : identifiant dans le site
                anneeRef : année dont on veut fournir l'analyse (Attention, stockée comme un entier)
        *out : F_est_dedans : liste de 14 variable qui indique le statut de chacun des documents recherchés (variable globale) en txt puis en pdf
    '''
    p = len(vg.type_recherches)
    F_est_dedans = ["Non existant"] * (p * 2)
    (F, _) = arb.liste_sous_chemin(vg.adresseSauvegardeRep + '/' + id_EPN)
    for f in F:
        (fname, ext) = os.path.splitext(f)
        L = fname.split("_")
        if ext == ".pdf" and len(L) == 3: # Si le fichier est un pdf et que la nomenclature est lisible :
            [_, ftype, annee] = L
            if annee == str(anneeRef):
                for k in range(p):
                    if ftype == vg.type_recherches[k]:
                        (Bouverture, Btexte) = io.pdf_non_vide(vg.adresseSauvegardeRep + '/' + id_EPN + '/' + f)
                        if Bouverture == False:
                            F_est_dedans[k + p] = "Corrompu"
                        else:
                            if Btexte == False:
                                F_est_dedans[k + p] = "Image"
                            else :
                                F_est_dedans[k + p] = "Texte"
        if ext == ".txt" and len(L) == 3: # Si le fichier est un txt et que la nomenclature est lisible :
             [_, ftype, annee] = L
             if annee == str(anneeRef):
                for k in range(p):
                    if ftype == vg.type_recherches[k]:
                        F_est_dedans[k] = "Existant"
    return F_est_dedans
    
def stat_F_est_dedans(F_est_dedans):
    '''Calcule des statistiques sur les fichiers
        *args : F_est_dedans : la liste pour un EPN des différents états des fichiers recherchés (d'après les variables globales)
        *out : fichier_plat_NE : nombre de fichier txt manquant
               img : nombre de fichier images
               corrompu : nombre de fichiers corrompus
    '''
    p = len(vg.type_recherches)
    fichier_plat_NE = 0
    img = 0 
    corrompu = 0
    pdf_NE = 0 
    pdf_notT_txt_NE = 0
    pdf_img_txt_NE = 0
    pdf_corr_txt_NE = 0
    pdf_NE_txt_NE = 0
    pdf_notT_txt_NE_sauf_bal = 0
    pdf_img_txt_NE_sauf_bal = 0
    pdf_corr_txt_NE_sauf_bal = 0
    pdf_NE_txt_NE_sauf_bal = 0
    for k in range(p):
        if F_est_dedans[k] == "Non existant" :
            fichier_plat_NE += 1
            if vg.abreviation[k] == "BAL05A0":
                if F_est_dedans[k] == "Non existant" and F_est_dedans[k + p] != "Texte":
                    pdf_notT_txt_NE += 1
                    if F_est_dedans[k + p] == "Image":
                        pdf_img_txt_NE += 1
                    elif F_est_dedans[k + p] == "Corrompu":
                        pdf_corr_txt_NE += 1
                    elif F_est_dedans[k + p] == "Non existant":
                        pdf_NE_txt_NE += 1
            else:
                if F_est_dedans[k] == "Non existant" and F_est_dedans[k + p] != "Texte":
                    pdf_notT_txt_NE += 1
                    pdf_notT_txt_NE_sauf_bal += 1
                    if F_est_dedans[k + p] == "Image":
                        pdf_img_txt_NE += 1
                        pdf_img_txt_NE_sauf_bal += 1
                    elif F_est_dedans[k + p] == "Corrompu":
                        pdf_corr_txt_NE_sauf_bal += 1
                        pdf_corr_txt_NE += 1
                    elif F_est_dedans[k + p] == "Non existant":
                        pdf_NE_txt_NE_sauf_bal += 1
                        pdf_NE_txt_NE += 1
    for k in range(p, 2 * p):
        if F_est_dedans[k] == "Image":
            img += 1    
        elif F_est_dedans[k] == "Corrompu":
            corrompu += 1  
        elif F_est_dedans[k] == "Non existant":
            pdf_NE += 1
    return [fichier_plat_NE, img, corrompu, pdf_NE, pdf_notT_txt_NE, pdf_img_txt_NE, pdf_corr_txt_NE, pdf_NE_txt_NE, pdf_notT_txt_NE_sauf_bal, pdf_img_txt_NE_sauf_bal, pdf_corr_txt_NE_sauf_bal, pdf_NE_txt_NE_sauf_bal]
                                 
             
def analyse_sellement(anneeRef):
    '''Réalisation des calculs sur tout les comptables pour une année donnée (dans les dossiers de chargement, il peut y avoir plusieurs années)
        *args : anneeRef : entier
        * out : None
    '''
    workbook = xlsxwriter.Workbook(vg.adresseSauvegardeRep + "/" + "Analyse_sellement_comptes_" + str(anneeRef) +".xlsx") #Création d'un fichier excel
    T_sell = io.lire_csv("./", "Liste_comptes_selles")
    n = len(T_sell)
    worksheet = workbook.add_worksheet("Statistiques") # Création de la feuille de statistique
    bold = workbook.add_format({'bold': True}) # Création du format gras des cases
    legende = ["Identifiant de l'EPN","Nom de l'EPN",
               "txt_CR","txt_BILAN","txt_SPE1","txt_SPE2","txt_BAL","txt_BAL05A","txt_ABE","txt_TEF",
               "pdf_CR","pdf_BILAN","pdf_SPE1","pdf_SPE2","pdf_BAL","pdf_BAL05A","pdf_ABE","pdf_TEF",
               "Nombre fichier txt manquant","Nombre fichiers pdfs images", "Nombre fichiers pdfs corrompus", "Nombre de fichiers pdf manquants", "Nombre de fichiers ayant une erreur grave",
               "Nombre fichier pdf image avec txt manquant", "Nombre fichier pdf corrompus avec txt manquant", "Nombre fichier pdf manquant avec txt manquant","Nombre de fichiers ayant une erreur grave (sans compter BAL05A)",
               "Nombre fichier pdf image avec txt manquant (sans compter BAL05A)", "Nombre fichier pdf corrompus avec txt manquant (sans compter BAL05A)", "Nombre fichier pdf manquant avec txt manquant (sans compter BAL05A)"
               ]
    for j in range(len(legende)): # Ecriture de la légende
        worksheet.write(0, j, legende[j])
    for i in range(n):
        if len(T_sell[i]) >= 2:
            id_EPN = T_sell[i][0]
            print(id_EPN)
            nom_EPN = T_sell[i][1]
            F = types_sont_dedans(id_EPN, anneeRef)
            S = stat_F_est_dedans(F)
            ligne = [id_EPN, nom_EPN] + F + S
            for j in range(len(ligne)):
                if j >= len(ligne) - 4:
                    worksheet.write(i + 1, j, ligne[j], bold) # Les statistiques sont mises en gras
                else:
                    worksheet.write(i + 1, j, ligne[j]) # les données autres sont écrites normalement
    workbook.close()
    return
    
