# -*- coding: utf-8 -*-
# Fichier VarGlobale.py
# Contient les variables globales nécéssaires au code

import os
import time

annee_actuelle = time.gmtime().tm_year
annee_reference = 2016 # première année dont on a les resultats

path = "C:\\Users\\ameilac\\AppData\\Local\\Mozilla Firefox" #Localisation de geckodriver

os.environ["PATH"] += path + ";" # Ajout aux chemins systèmes

identifiant = "cedot-xt" # identifiant de la session
motDePasse = "vn4Vg0wp" # mot de passe de la session

url_login = "https://pass.cp.finances.ader.gouv.fr/portail/ader" # lien d'entrée sur le site

adresseSauvegardeRep = "./" + "Comptes_selles"    # adresse de sauvegarde des répertoires
adresseSauvegardeStruct = "./" + "liste_fichiers" # adresse de sauvegarde des structures de pages pour le renommage

if not os.path.exists(adresseSauvegardeStruct):
    os.mkdir(adresseSauvegardeStruct)
if not os.path.exists(adresseSauvegardeRep):
    os.mkdir(adresseSauvegardeRep)
    
type_recherches = ["CR","BILAN","SPE1","SPE2","BAL","ABE","TEF"] # type des documents qu'on va étudier

nom_reel = ["Compte de résultat de l'exercice",
 'Bilan',
 'Annexe des comptes annuels',
 'Etat de l’évolution de la situation patrimoniale en droit constaté (Tableau 1)',
 'Etat de l’évolution de la situation patrimoniale en droit constaté (Tableau 2)',
 'Balance définitive des comptes (état au format PDF)',
 'Balance définitive des comptes de rang 07, niveau détaillé',
 'Balance définitive des comptes de rang 05, niveau détaillé',
 'Balance des comptes des valeurs inactives',
 'Etat de développement des soldes des comptes d’immobilisation (classe 2) et des comptes de tiers (classe 4)',
 'Délibération de l’organe délibérant relative aux comptes financiers',
 'Rapport établi par le commissaire aux comptes',
 "Etat prévu par l’article 212 du décret du 7 novembre 2012 : observations de l'agent comptable",
 'Procès verbal de caisse et de portefeuille',
 'Tableau des autorisations budgétaires en AE et CP, recettes et solde budgétaire',
 'Tableau des autorisations budgétaires en AE et CP , spécifique aux EPST',
 'Tableau d’équilibre financier',
 'Budget initial de l’organisme : délibération de l’organe délibérant',
 'Budgets rectificatifs de l’organisme : délibérations de l’organe délibérant',
 'Rapport de gestion établi par l’ordonnateur pour l’exercice écoulé',
 'Dossier de réquisition de l’exercice écoulé',
 'Convention de contrôle allégé en partenariat',
 'Plan de contrôle hiérarchisé des dépenses',
 'Documents relatifs à la nomination de l’agent comptable lorsque sa nomination intervient entre deux transmissions de compte financier au juge des comptes',
 'Documents relatifs à la cessation de fonction de l’agent comptable au cours de l’exercice écoulé',
 'Copie de rapports d’audits financiers et comptables notifiés au cours de l’exercice',
 'Balance définitive des comptes de rang 07, niveau agrégé',
 'Balance définitive des comptes de rang 05, niveau agrégé',
 'Balance définitive des comptes de rang 07, niveau consolidé',
 'Balance définitive des comptes de rang 05, niveau consolidé']

abreviation = ["CR",
               "BILAN",
               "ANNEXE",
               "SPE1",
               "SPE2",
               "BAL",
               "BAL07D",
               "BAL05D",
               "BVI",
               "EDS",
               "DF",
               "CAC",
               "OAC",
               "PV",
               "ABE",
               "EPST",
               "TEF",
               "BI",
               "BR",
               "RG",
               "REQ",
               "CAP",
               "CHD",
               "NOMIN",
               "CESS",
               "RAF",
               "BAL07A",
               "BAL05A",
               "BAL07C",
               "BAL05C"]