# -*- coding: utf-8 -*-
# Fichier IOinternet.py
# contient les fonctions qui permettent d'accéder à internet


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from copy import deepcopy
import VarGlobale as vg
import threading
import time
import IOfichier as io


def ouverture_session_firefox():
    '''Permet de créer une session firefox avec les paramètres par défaut qui permettent de sauvegarder les fichiers sans bloquer
        *args : None
        *out : driver : session geckodriver
    '''
    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.download.manager.showWhenStarting",False)
    fp.set_preference("browser.download.panel.shown", False)
    fp.set_preference("browser.helperApps.neverAsk.openFile","text/*,application/text,application/vnd.ms-excel,application/pdf,application/vnd.adobe.xfdf,application/vnd.fdf,application/vnd.adobe.xdp+xml")
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/*,application/text,application/vnd.ms-excel,application/pdf,application/vnd.adobe.xfdf,application/vnd.fdf,application/vnd.adobe.xdp+xml")
    fp.set_preference("plugin.disable_full_page_plugin_for_types","text/*,application/text,application/vnd.ms-excel,application/pdf,application/vnd.adobe.xfdf,application/vnd.fdf,application/vnd.adobe.xdp+xml")
    fp.set_preference("pdfjs.disabled", True)  
    driver = webdriver.Firefox(firefox_profile=fp) # Ouverture de la session firefox
    return driver
    
    
def log_in_portail_ader(driver, noprint = False):
    '''Fonction qui permet de se connecter au site de la DGFIP
        *args : driver : la session firefox sur laquelle on se connecte
                url_log : lien html vers le portail de connection (mis dans variables globales)
                ide : identifiant (mis dans les variables globales)
                mdp : mot de passe (mis dans les variables globales)
    '''
    if not noprint:
        print("Connection à " + vg.url_login)
    driver.get(vg.url_login)
    driver.find_element_by_name("identifiant").send_keys(vg.identifiant, Keys.ARROW_DOWN)
    driver.find_element_by_name("secret").send_keys(vg.motDePasse, Keys.ARROW_DOWN)
    driver.find_element_by_name("apply").click()
    if not noprint:
        print("Connecté à la session")
    return 
    
    
def recuperation_compte_selles(driver, noprint = False):
    '''Fonction qui va fournir la liste des comptes sellés
        *args : driver : session sur laquelle on effectue l'opération
                noprint : boléen qui permet d'avoir un affichage des différentes opérations en cours
        *out : T : tableau des comptes sellés
    Attention, pour pouvoir accéder aux autres pages du site, il faut au moins avoir utilisé une fois la première instruction
    '''
    driver.get("https://pass.cp.finances.ader.gouv.fr/epn_gip/")
    driver.get("https://pass.cp.finances.ader.gouv.fr/epn_gip/demat/listeEnveloppes")
    driver.find_element_by_name("DataTables_Table_1_length").send_keys("Tous")
    T = []
    for i in range(106):  # 106 = nombre de pages qu'on parcours (on clique sur le bouton suivant à chaque fois en fait, donc on a besoin d'une condition d'arrêt)
        if not noprint:    
            print("Parcours de la page " + str(i+1))
        table_id = driver.find_element_by_id("DataTables_Table_1").find_elements_by_tag_name("td")
        T.extend(recup_table_texte(table_id, 5)) # retranscription du tableau avec des colonnes (il y a 5 colonnes dans le site)
        driver.find_element_by_id("DataTables_Table_1_next").click() 
    return T 
    
    
def recuperation_document_compte(driver, id_EPN):
    '''Permet de récupérer les documents concernant un compte particulier
        *args: driver : session firefox sur laquelle on effectue l'opération
               id_EPN : identifiant EPN du compte
        *out : None
    '''
    driver.get("https://pass.cp.finances.ader.gouv.fr/epn_gip/demat/compteFinancier?idEPN=" + id_EPN)
    time.sleep(2) # On peut baisser le temps d'attente à 1.5 mais il se peut qu'il ne voye rien si la page n'a pas fini de charger
    for i in range(0, vg.annee_actuelle - vg.annee_reference + 1): # Prévu pour lorsqu'il y aura plusieurs années, télécharge jusqu'à l'année de référence
        try :
            Lien = []
            elmt = driver.find_element_by_id("ui-id-{}".format(i+1))
            year = elmt.text.split(" ")[1] 
            elmt.click()
            table_id = driver.find_element_by_id("DataTables_Table_{}".format(i+1)).find_elements_by_tag_name("tr") # On cherche les lignes
            for k in range(1, len(table_id)):
                element = table_id[k].find_elements_by_tag_name("td") # On divise chaque ligne en colonne
                ligne = [element[0].text, element[1].text, element[2].text]
                for j in range(len(element) - 2, len(element)): # et sur les deux dernieres colonnes on essaye de voir si on a des fichiers
                    try :
                        element[j].find_element_by_tag_name('img').click() # Lance le téléchargement des fichiers
                        ligne.append(element[j].find_element_by_tag_name("a").get_attribute("href")) # Prend le lien html du fichier sous forme de texte
                    except:
                        pass
                        ligne.append("")
                Lien.append(ligne)
            io.ecrire_csv(vg.adresseSauvegardeStruct, id_EPN + '_' + year, Lien) # Sauvegarde de la structure des répertoires dans un csv
        except:
            break
    return
                
    
def recup_table_texte(table, nb_colonne):    
    '''Transforme une liste en tableau avec les dimensions données, ça évite d'avoir à faire recalculer deux fois le driver
        *args: tableau : liste
               nb_colonne : nombre de colonne
        * Tableau : liste de listes (les listes ayant une longueur égale au nombre de colonnes)
    '''
    T = []
    for i in range(len(table)//nb_colonne):
        ligne = []
        for j in range(nb_colonne):
            ligne.append(table[nb_colonne * i + j].text)
        ligne = deepcopy(ligne) # Evite qu'il y ait des problèmes de passage par référence
        T.append(ligne)
    return T
    
    
def telechargement_basique(D):
    '''Effectue les processus de téléchargement dans une fenêtre
        *args : id_EPN : pour aller sur la page où on doit faire le chargement    
    '''
    driver = ouverture_session_firefox()
    log_in_portail_ader(driver)
    driver.get("https://pass.cp.finances.ader.gouv.fr/epn_gip/") # Obligatoire pour ne pas que la connexion expire
    driver.get("https://pass.cp.finances.ader.gouv.fr/epn_gip/demat/listeEnveloppes") # Obligatoire pour ne pas que la connexion expire
    for id_EPN in D:
        print("Téléchargement des documents de " + id_EPN)
        recuperation_document_compte(driver, id_EPN)
        driver.get("https://pass.cp.finances.ader.gouv.fr/epn_gip/demat/listeEnveloppes")
    time.sleep(10)
    driver.close()
    return

    
def telechargement_multithreading(n):
    ''' Télécharge n pages en même temps, parfois, il se peut qu'il y ait des oublis par rapport au temps de chargement des pages si on descend en dessous de 2 secondes, dans ce cas
    il faut vérifier quels sont les répertoires non vides, et les télécharger via un algorithme, cette option de correction reste toujours plus rapide que l'option à un seul thread
        *args : None
        *out : None
    '''
    T_sell = io.lire_csv("./", "Liste_comptes_selles")
    T_thread = []
    for i in range(n):
        D = [T_sell[j][0] for j in range(i, len(T_sell), n)]
        t = threading.Thread(target=telechargement_basique, args = (D,))
        T_thread.append(t)
        T_thread[-1].start()
        time.sleep(2) # Pour éviter que plusieurs thread accèdent au même fichier en même temps
    est_termine = False
    while not est_termine:
        est_termine = True
        for t in T_thread:
            if t.is_alive():
                est_termine = False
                break
        time.sleep(4)
    return
   
    
def telechargement_unithreading():
    ''' Télécharge les pages une à une, fiable mais lent
        *args : None
        *out : None
    '''
    driver = ouverture_session_firefox()
    log_in_portail_ader(driver)
    driver.get("https://pass.cp.finances.ader.gouv.fr/epn_gip/")
    driver.get("https://pass.cp.finances.ader.gouv.fr/epn_gip/demat/listeEnveloppes")
    T_sell = io.lire_csv("./", "Liste_comptes_selles")
    del(T_sell[-1])
    for compte_sell in T_sell:
        print("Téléchargement de " + compte_sell[0])
        recuperation_document_compte(driver, compte_sell[0])
    return
