#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 12:22:02 2020

@author: steve
"""

'''
    PARTIE 1 - QUESTION 2
    ---------------------
    Mettre en place un niveau de verbosité variable pour les messages envoyés.
    Ainsi, pour faciliter la compréhension des enchainements ou pour debuguer,
    les tâches pourront être plus ou moins explicitées en fonction de ce niveau
    de verbosité.

'''


import threading,random,argparse


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
    def __init__(self,pic,bar,commandes,verb):
        self.pic = pic
        self.bar = bar
        self.commandes = commandes
        self.verb = verb
        
        
    def prendre_commande(self):
        """ Prend une commande et embroche un post-it. """
        
        if self.verb == "v":
            while self.commandes != list():
                com = self.commandes.pop()
                print(f"[Serveur]  Je prends la commande de {com}")
                self.pic.embrocher(com)
                print(f"[Pic] post-it {com} embroché")
            
            print(end = "\n")
            print("[Serveur]  Il n'y a plus de commande à prendre")
            print("Plus de commande à prendre ")
            print(end = "\n")
                
        elif self.verb == "V":
            while self.commandes != list():
                com = self.commandes.pop()
                print(f"[Serveur]  Je prends la commande de {com}")
                self.pic.embrocher(com)
                print(f"[Pic] post-it {com} embroché")
                print(f"[Pic] état =  {self.pic.postits}")
                
            print(end = "\n")    
            print("[Serveur]  Il n'y a plus de commande à prendre")
            print("Plus de commande à prendre ")
            print(end= "\n")
            
        else:
            while self.commandes != list():
                com = self.commandes.pop()
                print(f"[Serveur]  Je prends la commande de {com}")
                self.pic.embrocher(com)
            
            print(end = "\n")
            print("[Serveur]  Il n'y a plus de commande à prendre")
            print(end= "\n")
        
        
    def servir(self):
        """ Prend un plateau sur le bar. """
        
        if self.verb == "v":
            while self.bar.plateaux != list():
                service = self.bar.evacuer()
                print(f"[Bar] {service} évacué")
                print(f"[Serveur]  Je sers {service}")
                
            print(end = "\n")
            print("[Bar] Bar est vide")
            print(end = "\n")
            
        elif self.verb == "V":
            while self.bar.plateaux != list():
                print(f"[Bar] état = {self.bar.plateaux}")
                service = self.bar.evacuer()
                print(f"[Bar] {service} évacué")
                print(f"[Serveur]  Je sers {service}")
                
            print(end = "\n")
            print(f"[Bar] état = {self.bar.plateaux}")
            print("[Bar] Bar est vide")
            print(end = "\n")

        else :
            while self.bar.plateaux != list():
                service = self.bar.evacuer()
                print(f"[Serveur]  Je sers {service}")

class Barman:
    def __init__(self,pic,bar,verb):
        self.pic = pic
        self.bar = bar
        self.verb = verb
        
    def preparer(self):
        """ Prend un post-it, prépare la commande et la dépose sur le bar. """
        
        
        if self.verb == "v":
            while self.pic.postits != list() :
                print(f"[Pic] état= {self.pic.postits}")
                preparation = self.pic.liberer()
                print(f"[Pic]  post-it {preparation} libéré ")
                print(f"[Barman]  Je commence la fabrication de {preparation}")
                self.bar.recevoir(preparation)
                print(f"[Barman]  Je termine la fabrication de {preparation}")
                print(f"[Bar] {preparation} reçu")
                
            print(end = "\n")
            print("[Pic] Pic est vide")
            print(end = "\n")
            
        elif self.verb == "V":
            while self.pic.postits != list() :
                print(f"[Pic] état= {self.pic.postits}")
                preparation = self.pic.liberer()
                print(f"[Pic]  post-it {preparation} libéré ")
                print(f"[Barman]  Je commence la fabrication de {preparation}")
                self.bar.recevoir(preparation)
                print(f"[Barman]  Je termine la fabrication de {preparation}")
                print(f"[Bar] {preparation} reçu")
                print(f"[Bar] état = {self.bar.plateaux}")
                
            print(end = "\n")
            print(f"[Pic] état = {self.pic.postits}")
            print("[Pic] Pic est vide")
            print(end = "\n")
            
        else :
            while self.pic.postits != list() :
                preparation = self.pic.liberer()
                print(f"[Barman]  Je commence la fabrication de {preparation}")
                self.bar.recevoir(preparation)
                print(f"[Barman]  Je termine la fabrication de {preparation}")
            print(end = "\n")


class activite(threading.Thread):
    
    def __init__(self,coc,com,pic,bar,ser,barm,v1,v2,v3,verb):
        self.cocktails = coc
        self.commandes = com
        self.pic = pic
        self.bar = bar
        self.serveur = ser
        self.barman = barm
        self.verrou1 = v1
        self.verrou2 = v2
        self.verrou3 = v3
        self.verb = verb
        
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
    
    1. Créer les objets : un pic, un bar,un serveur, un barman
    2. Boucle sur le serveur pour prendre les commandes
    3. Boucle pour les préparations
    4. Boucle pour les services
    
'''


if __name__ == '__main__' :
    
    aide1 = "La verbosité est soit minimale (-), soit moyenne (v) ou maximale (V) ." 
    aide2 = " Écrivez n'importe quel caractère si vous voulez une verbosité minimale" 
    
    parser = argparse.ArgumentParser()
    parser.add_argument("verbosite",help = aide1 + aide2)
    args = parser.parse_args()
    verbosite = args.verbosite
    
    if verbosite:
        cocktails = list()
        print(end = "\n")
        try:
            print("Les cocktails s'i vous plaît !!!" ,end = "\n")
            for line in open(input("Tapez cocktails.txt pour voir les cocktails disponibles ... "), "r"):
                for coc in line.split(","): cocktails.append(coc)
            commandes = [random.choice(cocktails) for i in range(10)]
            pic = Pic(list(), list())
            bar = Bar(list(), list())
            
            
            v1 = threading.Lock()
            v2 = threading.Lock()
            v3 = threading.Lock()
            
            print(end = "\n")
            print("cocktails " , end= "/")
            for cocktail in cocktails:
                print("   ",cocktail , end = "")
            print(end = "\n")
            
            print(end = "\n")
            print("[Barman]   Prêt pour le service !")
            print("[Serveur]  Prêt pour le service !")
            print(end = "\n")
            serveur= Serveur(pic,bar,commandes,verbosite)
            barman = Barman(pic,bar,verbosite)
            ActiviteDuBar = activite(cocktails,commandes,pic,bar,serveur,
                          barman,v1,v2,v3,verbosite)
            ActiviteDuBar.start()
            ActiviteDuBar.join()
        except FileNotFoundError:
            print("Le fichier contenant les cocktails est inexistant")
            print(end = "\n")
    else:
        verbosite = "-"
        pic = Pic(list(), list())
        bar = Bar(list(), list())
        serveur= Serveur(pic,bar,commandes,verbosite)
        barman = Barman(pic,bar,verbosite)
        ActiviteDuBar = activite(cocktails,commandes,pic,bar,serveur,
                      barman,v1,v2,v3,verbosite)
        ActiviteDuBar.start()
        ActiviteDuBar.join()
    print(end = "\n")