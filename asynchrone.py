#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 17:01:40 2020

@author: steve
"""

'''
     PARTIE 2
    ---------
    Il s’agit de réaliser la même chose en asynchrone, de façon à ce que les tâches
    du barman et du serveur s’entremêlent de façon à éviter les temps morts.
    Penser à adapter les temps d'attente pendant la prise de commande, la préparation
    des cocktails et le service pour mieux observer le traitement asynchrone'

'''

import asyncio,random,argparse


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
            if self.commandes != list():
                com = self.commandes.pop()
                print(f"[Serveur]  Je prends la commande de {com}")
                self.pic.embrocher(com)
                print(f"[Pic] post-it {com} embroché")
            
            else:
                print(end = "\n")
                print("[Serveur]  Il n'y a plus de commande à prendre")
                print("Plus de commande à prendre ")
                print(end= "\n")
                
        elif self.verb == "V":
            if self.commandes != list():
                com = self.commandes.pop()
                print(f"[Serveur]  Je prends la commande de {com}")
                self.pic.embrocher(com)
                print(f"[Pic] post-it {com} embroché")
                print(f"[Pic] état =  {self.pic.postits}")
                
            else:
                print(end = "\n")
                print("[Serveur]  Il n'y a plus de commande à prendre")
                print("Plus de commande à prendre ")
                print(end= "\n")   
        else:
            if self.commandes != list():
                com = self.commandes.pop()
                print(f"[Serveur]  Je prends la commande de {com}")
                self.pic.embrocher(com)
            
            else:
                print(end = "\n")
                print("[Serveur]  Il n'y a plus de commande à prendre")
                print(end= "\n")
        
        
    def servir(self):
        """ Prend un plateau sur le bar. """
        
        if self.verb == "v":
            if self.bar.plateaux != list():
                service = self.bar.evacuer()
                print(f"[Bar] {service} évacué")
                print(f"[Serveur]  Je sers {service}")
            else:
                print("[Bar] Bar est vide") # à vérifier
                print(end = "\n")
            
        elif self.verb == "V":
            if self.bar.plateaux != list():
                print(f"[Bar] état = {self.bar.plateaux}")
                service = self.bar.evacuer()
                print(f"[Bar] {service} évacué")
                print(f"[Serveur]  Je sers {service}")
            else:
                print(end = "\n")
                print(f"[Bar] état = {self.bar.plateaux}")
                print("[Bar] Bar est vide")
                print(end = "\n")
        else :
            if self.bar.plateaux != list():
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
            if self.pic.postits != list() :
                print(f"[Pic] état= {self.pic.postits}")
                preparation = self.pic.liberer()
                print(f"[Pic]  post-it {preparation} libéré ")
                print(f"[Barman]  Je commence la fabrication de {preparation}")
                print(f"[Barman]  Je termine la fabrication de {preparation}")
                self.bar.recevoir(preparation)
                print(f"[Bar] {preparation} reçu")
                
            else:
                print(end = "\n")
                print("[Pic] Pic est vide")
                print(end = "\n")
            
        elif self.verb == "V":
            if self.pic.postits != list() :
                print(f"[Pic] état= {self.pic.postits}")
                preparation = self.pic.liberer()
                print(f"[Pic]  post-it {preparation} libéré ")
                print(f"[Barman]  Je commence la fabrication de {preparation}")
                print(f"[Barman]  Je termine la fabrication de {preparation}")
                self.bar.recevoir(preparation)
                print(f"[Bar] {preparation} reçu")
                print(f"[Bar] état = {self.bar.plateaux}")
            else:
                print(end = "\n")
                print(f"[Pic] état = {self.pic.postits}")
                print("[Pic] Pic est vide")
                print(end = "\n")
            
        else :
            if self.pic.postits != list() :
                preparation = self.pic.liberer()
                print(f"[Barman]  Je commence la fabrication de {preparation}")
                print(f"[Barman]  Je termine la fabrication de {preparation}")
                self.bar.recevoir(preparation)
            else:
                print(end = "\n")
                

'''
    STRUCTURE DU PROGRAMME PRINCIPAL
    --------------------------------
    
    1. Créer les objets : un pic, un bar,un serveur, un barman
    2. Boucle sur le serveur pour prendre les commandes
    3. Boucle sur le barman pour préparer les différents cocktails commandés
    4. Boucle sur le serveur pour servir les cocktails préparés
    
    On se convient que :
        La prise de commande dure 0.5 sec
        La préparation d'un cocktail dure 1 sec
        Un client doit attendre 1.5 sec pour être servi

'''

class fonctionnement_du_bar():
    
    def __init__(self,commandes,pic,bar,serveur,barman,verbosite):
        self.commandes = commandes
        self.pic = pic
        self.bar = bar
        self.serveur = serveur
        self.barman = barman
        self.verbosite = verbosite
         
    async def commande(self):
        while self.commandes != list():
            await asyncio.sleep(1)
            self.serveur.prendre_commande()
        self.serveur.prendre_commande()
            
    async def prepare(self):
        for i in range(len(self.commandes)+1):
            await asyncio.sleep(1.2)
            self.barman.preparer()
        
    async def servir(self):
        for i in range(len(self.commandes)+1):
            await asyncio.sleep(1.5)
            self.serveur.servir()
 
    

if __name__ == '__main__' :

    aide1 = "La verbosité est soit minimale (-), soit moyenne (v) ou maximale (V) ."
    aide2 = " Écrivez n'importe quel caractère si vous voulez une verbosité minimale"
    
    parser = argparse.ArgumentParser()
    parser.add_argument("verbosite",help= aide1 + aide2)
    args = parser.parse_args()
    verbosite = args.verbosite
    loop = asyncio.get_event_loop()
    
    if verbosite:
        cocktails = list()
        print(end = "\n")
        path = "cocktails.txt"
        for line in open(path, "r"):
            for coc in line.split(","): cocktails.append(coc)
        commandes = [random.choice(cocktails) for i in range(10)]
        pic = Pic(list(), list())
        bar = Bar(list(), list())
        
        print("cocktails " , end= "/")
        for cocktail in cocktails:
            print("  ",cocktail , end = "")
        print(end = "\n")
        
        print(end = "\n")
        print("Voici les cocktails commandés :")
        print(end = "\n")
        for commande in commandes:
            print(commande,"   ", end = "")
        print(end = "\n")
        
        print(end = "\n")
        print("[Barman]   Prêt pour le service !")
        print("[Serveur]  Prêt pour le service !")
        print(end = "\n")
        
        serveur= Serveur(pic,bar,commandes,verbosite)
        barman = Barman(pic,bar,verbosite)
        fonct = fonctionnement_du_bar(commandes,pic,bar,serveur,barman,verbosite)
        activite = asyncio.wait([fonct.commande(), fonct.prepare() ,fonct.servir()])
        loop.run_until_complete(activite)
        loop.close()
        
    else:
        verbosite = "-"
        serveur= Serveur(pic,bar,commandes,verbosite)
        barman = Barman(pic,bar,verbosite)
        fonct = fonctionnement_du_bar(commandes,pic,bar,serveur,barman,verbosite)
        activite = asyncio.wait([fonct.commande(), fonct.prepare(), fonct.servir()])
        loop.run_until_complete(activite)
        loop.close()

    print(end = "\n")