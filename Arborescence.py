# -*- coding: utf-8 -*-
# Fichier Arborescence.py
# contient les fonctions qui facilitent l'accès à l'arborescence


import os 
import shutil # Pour déplacer des fichiers

def liste_sous_chemin(chemin_parent):
    '''Renvoit l'arborescence (au premier niveau uniquement)
        *args = chemin_parent : chemin dont on veut écrire l'aborescence
        *out = (fichier, repertoire) avec des liens sous forme de noms (chemin relatifs et non absolus)
    '''
    L = os.listdir(chemin_parent)
    F = [] # Stocke les liens des fichiers
    R = [] # Stocke les liens des repertoires
    for lien in L:
        if os.path.isfile(chemin_parent + "/" + lien): #teste si le lien est un fichier ou un répertoire
            F.append(lien)
        else :
            R.append(lien)
    return (F, R)    

    
def liste_pdf(chemin):
    '''Renvoit la liste des noms des fichiers pdf (avec extension)
        *ags = chemin : répertoire qui contient les pdfs
        *out = F : liste de string
        '''
    (F, _) = liste_sous_chemin(chemin)
    for i in reversed(range(len(F))):
        (fname, ext) = os.path.splitext(F[i]) # coupe le nom du fichier de l'extension
        if ext != ".pdf":
            del(F[i])
    return F
    
    
