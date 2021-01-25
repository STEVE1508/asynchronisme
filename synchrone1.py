#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 04:50:07 2020

@author: steve
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 20:39:10 2020

@author: steve
"""


'''
    PARTIE 1 - QUESTION 1
    ---------------------
    Il s’agit de réaliser la version synchrone, dans laquelle les traitements
    sont classiquement des fonctions ininterruptibles.

'''


import threading,random

class Accessoire():
    def __init__(self, postits, plateaux):
        self.postits = postits
        self.plateaux = plateaux
        
 
    
class Pic(Accessoire):
    """ Un pic peut embrocher un post-it par-dessus les post-it déjà présents
        et libérer le dernier embroché. """
    def embrocher(self,postit):
        self.postits.append(postit)
        
    def liberer(self):
        postit = self.postits.pop()
        return postit
    

class Bar(Accessoire):
    """ Un bar peut recevoir des plateaux, et évacuer le dernier reçu """
    def recevoir(self,plateau):
        self.plateaux.append(plateau)
        
    def evacuer(self):
        plateau = self.plateaux.pop()
        return plateau
    

class Serveur:
    def __init__(self,pic,bar,commandes):
        self.pic = pic
        self.bar = bar
        self.commandes = commandes
        
    def prendre_commande(self):
        """ Prend une commande et embroche un post-it. """
           
        while self.commandes != list():
            com = self.commandes.pop()
            print(f"[Serveur]  Je prends la commande de {com}")
            self.pic.embrocher(com)
            
        print("[Serveur]  Il n'y a plus de commande à prendre")
        print(end= "\n")
    def servir(self):
        """ Prend un plateau sur le bar. """
        while self.bar.plateaux != list():
            service = self.bar.evacuer()
            print(f"[Serveur]  Je sers {service}")

class Barman:
    def __init__(self,pic,bar):
        self.pic = pic
        self.bar = bar
        
    def preparer(self):
        """ Prend un post-it, prépare la commande et la dépose sur le bar. """
        while self.pic.postits != list() :
            preparation = self.pic.liberer()
            print(f"[Barman]  Je commence la fabrication de {preparation}")
            self.bar.recevoir(preparation)
            print(f"[Barman]  Je termine la fabrication de {preparation}")
        print(end = "\n")


class activite(threading.Thread):
    
    def __init__(self,coc,com,pic,bar,ser,barm,v1,v2,v3):
        self.cocktails = coc
        self.commandes = com
        self.pic = pic
        self.bar = bar
        self.serveur = ser
        self.barman = barm
        self.verrou1 = v1
        self.verrou2 = v2
        self.verrou3 = v3
        
        threading.Thread.__init__(self)

    def run(self):

        self.verrou1.acquire()
        self.serveur.prendre_commande()
        self.verrou1.release()
        
        self.verrou2.acquire()
        self.barman.preparer()
        self.verrou2.release()
        
        self.verrou3.acquire()
        self.serveur.servir()
        self.verrou3.release()
    
'''
    STRUCTURE DU PROGRAMME PRINCIPAL 
    --------------------------------
    
    1. Créer les objets :Un pic, un bar,un serveur, un barman
    2. Boucle sur le serveur pour prendre les commandes
    3. Boucle pour les préparations
    4. Boucle pour les services
    
'''


if __name__ == '__main__' :
    
    cocktails = list()
    print(end = "\n")
    print("Les cocktails s'il vous plaît !!!" ,end = "\n")
    for line in open(input("Tapez cocktails.txt pour voir les cocktails disponibles ... "), "r"):
        for coc in line.split(","): cocktails.append(coc)
        
    print(end = "\n")
    commandes = [random.choice(cocktails) for i in range(10)]
    pic = Pic(list(), list())
    bar = Bar(list(), list())
    serveur= Serveur(pic,bar,commandes)
    barman = Barman(pic,bar)
    
    # Les verrous
    
    v1 = threading.Lock()
    v2 = threading.Lock()
    v3 = threading.Lock()
    
    
    print("cocktails disponibles " , end= ":")
    for cocktail in cocktails:
        print("     ",cocktail , end = "")
    print(end = "\n")
    
    print(end = "\n")
    print("[Barman]   Prêt pour le service !")
    print("[Serveur]  Prêt pour le service !")
    print(end = "\n")
    
    ActiviteDuBar = activite(cocktails,commandes,pic,bar,serveur,barman,v1,v2,v3)
    ActiviteDuBar.start()
    ActiviteDuBar.join()
    print(end = "\n")